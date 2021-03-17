'''
Utilitario para crear grupos dependiendo de ciertos parámetros
'''

import json
import re
import requests
import alflib

URL = 'http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/groups'

SUBGRUPOS = ["Recepción", "Elaboración", "Gestionar", "Expediente", "Firmador", "Archivar"]
EXCEPCIONES = ["CHOFER", "SECRETARIA"]

response = requests.get(URL,headers=alflib.headers)
groups = json.loads(response.text)
#{'entry': {'isRoot': True, 'displayName': 'SITE_ADMINISTRATORS',
# 'id': 'GROUP_SITE_ADMINISTRATORS'}}
for group in groups['list']['entries']:
    #print(group['entry']['displayName'])
    new_string = re.sub('\n', '', group['entry']['displayName'])
    result = re.split('-', new_string)
    if len(result[0]) == 3 and result[len(result)-1] not in EXCEPCIONES: # ABC- in pattern
        if len(result)==2:  # ABC-DEF-palabra
            for newgrp in SUBGRUPOS:
                string=result[0] + "-" + result[1] + '-' + newgrp
                print("Creando grupo llamado: ", string)
                post_data='{"id": "' + string + '", "displayName": "' + string + '"}'
                #response = requests.post(URL, data=post_data, headers=alflib.headers)
                #print(response.text)
        else:
            if len(result)==3: # ABC-DEF-HIG-Palabra
                for newgrp in SUBGRUPOS:
                    string=result[0] + "-" + result[1] + '-' + result[2] + "-" + newgrp
                    print("Creando grupo llamado: ", string)
                    post_data='{"id": "' + string + '", "displayName": "' + string + '"}'
                    #response = requests.post(URL, data=post_data, headers=alflib.headers)
                    #print(response.text)
