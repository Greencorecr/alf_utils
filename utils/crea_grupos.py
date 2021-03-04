'''
Utilitario para crear grupos dependiendo de ciertos parámetros
'''

import base64
import json
import requests
import re

URL = 'http://172.20.1.4:8080/alfresco/api/-default-/public/alfresco/versions/1/groups'

SUBGRUPOS = ["Recepción", "Elaboración", "Gestionar", "Expediente", "Firmador", "Archivar"]

USER = 'admin'
PASSWD = 'admin'
USERPASS = USER + ':' + PASSWD
encoded_u = base64.b64encode(USERPASS.encode()).decode()
headers = {"Authorization" : "Basic %s" % encoded_u,
        "Accept" : "application/json" }
response = requests.get(URL,headers=headers)
groups = json.loads(response.text)
#{'entry': {'isRoot': True, 'displayName': 'SITE_ADMINISTRATORS',
# 'id': 'GROUP_SITE_ADMINISTRATORS'}}
for group in groups['list']['entries']:
    #print(group['entry']['displayName'])
    new_string = re.sub('\n', '', group['entry']['displayName'])
    result = re.split('-', new_string)
    if len(result[0]) == 3:
        if len(result)==2:
            for newgrp in SUBGRUPOS:
                print("Creando grupo llamado: " + result[0] + "-" + result[1] + "-" + newgrp)
        else:
            if len(result)==3:
                for newgrp in SUBGRUPOS:
                    print("Creando grupo llamado: " + result[0] + "-" + result[1] + '-' + result[2] + "-" + newgrp)
