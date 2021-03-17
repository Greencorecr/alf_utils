'''
Tarea programada para notificar de vencimientos de documentos.
Lee de un archivo CSV (ver examples/) las reglas a ejecutar, y la lista de de directorios padre
'''

import base64
import csv
import json
import requests
import datetime
import dateutil.parser
import pytz

USER = 'admin'
PASSWD = 'admin'
USERPASS = USER + ':' + PASSWD
encoded_u = base64.b64encode(USERPASS.encode()).decode()
headers = {"Authorization" : "Basic %s" % encoded_u,
        "Accept" : "application/json" }

HOSTNAME = '172.20.1.4'

with open('vencimientos.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #print(row['nodeId'], row['correo'])
        URL = 'http://' + HOSTNAME + ':8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/' + row['nodeId'] + '/children'
        #print(URL)
        response = requests.get(URL,headers=headers)
        parent_dir = json.loads(response.text)
        #print(parent_dir)

        for subdir in parent_dir['list']['entries']:
            URL = 'http://' + HOSTNAME + ':8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/' + subdir['entry']['id'] + '/children'
            response = requests.get(URL,headers=headers)
            leaf_files = json.loads(response.text)
            if leaf_files['list']['pagination']['count'] > 0:
                meses = row[subdir['entry']['name'].lower()]
                #print("Meses: " + meses, subdir['entry']['name'])
                for leaf_file in leaf_files['list']['entries']:
                    file_time = dateutil.parser.parse(leaf_file['entry']['modifiedAt'])
                    now = datetime.datetime.now(pytz.utc)
                    file_stale = int((now-file_time).seconds/60)
                    if file_stale > int(meses):
                        print(leaf_file['entry']['name'], leaf_file['entry']['modifiedAt'] + " min-ago: " +str(file_stale))
