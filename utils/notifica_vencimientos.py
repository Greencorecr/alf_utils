'''
Tarea programada para notificar de vencimientos de documentos.
Lee de un archivo CSV (ver examples/) las reglas a ejecutar, y la lista de de directorios padre
'''

import csv
import json
import datetime
import dateutil.parser
import requests
import pytz
import alflib

HOSTNAME = '172.20.1.4'
URLAPI = ':8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/'

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
                    file_time = dateutil.parser.parse(leaf_file['entry']['modifiedAt'])
                    now = datetime.datetime.now(pytz.utc)
                    file_stale = int((now-file_time).seconds/60)
                    if file_stale > int(meses):
                        print('''Email text ''' +
                        leaf_file['entry']['name'], " min:" +
                        str(file_stale) + " Email: " + row['correo'])
