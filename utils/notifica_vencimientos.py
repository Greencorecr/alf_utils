'''
Tarea programada para notificar de vencimientos de documentos.
Lee de un archivo CSV (ver examples/) las reglas a ejecutar, y la lista de de directorios padre
'''

import csv
import json
import os
import datetime
import smtplib
import dateutil.parser
import requests
import pytz

import alflib

#HOSTNAME = '10.42.25.183'
HOSTNAME = 'localhost'
URLAPI = ':8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/'

DOCLINK = ':8080/share/page/site/rncr/document-details?nodeRef=workspace://SpacesStore/'
LINKTOP = 'http://' + HOSTNAME + DOCLINK

MESSAGEFROM = """From: Gestor Documental <pruebagestordocumentalrn@rnp.go.cr>
To: """

MESSAGETOP = """Subject: Vencimiento de documento

El documento de nombre: """


MESSAGEMID=""", se encuentra vencido.

Realice click en este enlace para atenderlo.

"""
# Meses
#TIME_DIVIDER = 60*60*24*30

# Años
TIME_DIVIDER = 60*60*24*30*12

# Minutos, para pruebas
#TIME_DIVIDER = 60

CONFIG_DOC = "49c93d95-9fab-4f2e-9bbd-7861ddc804b0" # RefId del documento "vencimientos.csv"

def envia_correo_verificacion(receiver, send_message):
    '''
    Función para enviar correos con mensaje específico
    de notificación de vencimiento de documento.
    '''
    sender = 'pruebagestordocumentalrn@rnp.go.cr'
    try:
        smtp_obj = smtplib.SMTP('localhost',1025)
        smtp_obj.sendmail(sender, receiver, send_message.encode("utf8"))
        #print ("Successfully sent email")
    except ValueError:
        print ("Error: unable to send email")

#debug#def envia_correo_verificacion(receiver, send_message):
#debug#    '''
#debug#    Función para enviar correos con mensaje específico
#debug#    de notificación de vencimiento de documento.
#debug#    '''
#debug#    sender = 'pruebagestordocumentalrn@rnp.go.cr'
#debug#    print(receiver, send_message)

def descarga_csv():
    '''
    Aquí borramos el CSV si existe, y lo descargamos de alfresco, usando el
    id de documento definido en CONFIG_DOC
    '''
    curl_opts1 = 'curl -s -X GET --output vencimientos.csv '
    url_api = '/alfresco/api/-default-/public/alfresco/versions/1/'
    auth = ' -H "Authorization: Basic YWRtaW46YWRtaW4=" '
    url = 'http://' + HOSTNAME + ':8080' + url_api + 'nodes/' + CONFIG_DOC + '/content'
    curl_cmd = curl_opts1 + auth + url
    result = os.popen(curl_cmd).read()


def procesa_padre(padre):
    '''
    Cuando encontramos en el CSV, un directorio padre para procesar, llamamos a esta función.
    Se encarga de navegar la estructura de hijos, y ver si los hijos existen como columnas en el CSV
    '''
    url = 'http://' + HOSTNAME + URLAPI + row['padre'] + '/children'
    response = requests.get(url,headers=alflib.headers)
    parent_dir = json.loads(response.text)
    #print(parent_dir)
    for subdir in parent_dir['list']['entries']:
        url = 'http://' + HOSTNAME + URLAPI + subdir['entry']['id'] + '/children'
        response = requests.get(url,headers=alflib.headers)
        leaf_files = json.loads(response.text)
        #print(leaf_files['list']['pagination']['count'])
        if leaf_files['list']['pagination']['count'] > 0:
            try:
                meses = row[subdir['entry']['name'].lower()]
                for leaf_file in leaf_files['list']['entries']:
                    #print(leaf_file)
                    file_time = dateutil.parser.parse(leaf_file['entry']['modifiedAt'])
                    now = datetime.datetime.now(pytz.utc)
                    file_stale = float((now-file_time).seconds/TIME_DIVIDER)
                    if file_stale > float(meses):
                        #print('''Email text ''' +
                        #leaf_file['entry']['name'], " min:" +
                        #str(file_stale) + " Email: " + row['correo'])
                        f_name = leaf_file['entry']['name']
                        f_id = leaf_file['entry']['id']
                        message = MESSAGETOP + f_name + MESSAGEMID + LINKTOP + f_id
                        #print(message)
                        envia_correo_verificacion(row['correo'], message)
            except KeyError:
                if subdir['entry']['id'] != padre:
                    #print("acceso limitado", subdir['entry']['id'])
                    url = 'http://' + HOSTNAME + URLAPI + subdir['entry']['id'] + '/children'
                    response = requests.get(url,headers=alflib.headers)
                    parent_dir = json.loads(response.text)
                    #print(parent_dir)
                    for subdir in parent_dir['list']['entries']:
                        url = 'http://' + HOSTNAME + URLAPI + subdir['entry']['id'] + '/children'
                        response = requests.get(url,headers=alflib.headers)
                        leaf_files = json.loads(response.text)
                        #print(leaf_files['list']['pagination']['count'])
                        if leaf_files['list']['pagination']['count'] > 0 :
                            try:
                                meses = row[subdir['entry']['name'].lower()]
                                for leaf_file in leaf_files['list']['entries']:
                                    #print(leaf_file)
                                    file_time = dateutil.parser.parse(leaf_file['entry']['modifiedAt'])
                                    now = datetime.datetime.now(pytz.utc)
                                    file_stale = float((now-file_time).seconds/TIME_DIVIDER)
                                    if file_stale > float(meses):
                                        #print('''Email text ''' +
                                        #leaf_file['entry']['name'], " min:" +
                                        #str(file_stale) + " Email: " + row['correo'])
                                        f_name = leaf_file['entry']['name']
                                        f_id = leaf_file['entry']['id']
                                        message = MESSAGETOP + f_name + MESSAGEMID + LINKTOP + f_id
                                        #print(message)
                                        envia_correo_verificacion(row['correo'], message)
                            except KeyError:
                                print("Nombre de directorio no presente en columnas de csv: ", subdir['entry']['name'].lower())


# main

descarga_csv()

with open('vencimientos.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['padre'])
        procesa_padre(row['padre'])
