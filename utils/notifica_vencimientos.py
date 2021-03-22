'''
Tarea programada para notificar de vencimientos de documentos.
Lee de un archivo CSV (ver examples/) las reglas a ejecutar, y la lista de de directorios padre
'''

import csv
import json
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
                    file_stale = float((now-file_time).seconds/60/60/24/30)
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
