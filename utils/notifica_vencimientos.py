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

HOSTNAME = '10.42.25.237'
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
#TIME_DIVIDER = 60/60/24/30

# Años
TIME_DIVIDER = 60/60/24/30/12

# Minutos, para pruebas
#TIME_DIVIDER = 60

CONFIG_DOC = "892c9e2d-ab8c-4b83-b0af-f14b4375b079"

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
    print(result)

descarga_csv()

with open('vencimientos.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        URL = 'http://' + HOSTNAME + URLAPI + row['nodeId'] + '/children'
        response = requests.get(URL,headers=alflib.headers)
        parent_dir = json.loads(response.text)
        for subdir in parent_dir['list']['entries']:
            URL = 'http://' + HOSTNAME + URLAPI + subdir['entry']['id'] + '/children'
            response = requests.get(URL,headers=alflib.headers)
            leaf_files = json.loads(response.text)
            if leaf_files['list']['pagination']['count'] > 0:
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
                        link = LINKTOP + leaf_file['entry']['id']
                        f_name = leaf_file['entry']['name']
                        f_id = leaf_file['entry']['id']
                        message = MESSAGETOP + f_name + MESSAGEMID + LINKTOP + f_id
                        #print(message)
                        envia_correo_verificacion(row['correo'], message)
