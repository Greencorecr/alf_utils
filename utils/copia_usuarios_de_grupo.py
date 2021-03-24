'''
Busca los usuarios que pertenecen a OLDGRP y los agrega en NEWGRP
'''

import json
import requests
import alflib

HOST = '10.42.25.183'

OLDGRP = 'GROUP_DRI-CTE-CARTOGRAFIA_CATASTRAL'
NEWGRP = 'GROUP_DRI-CTE-CATASTRAL-TECNICO_CARTOGRAFIA_CATASTRAL'
URL_API = ':8080/alfresco/api/-default-/public/alfresco/versions/1/'

URL = 'http://' + HOST + URL_API + 'groups/' + OLDGRP + '/members'
response = requests.get(URL,headers=alflib.headers)
old_group = json.loads(response.text)

for user in old_group['list']['entries']:
    print(user['entry']['displayName'])
    post_data='{"id": "' + user['entry']['id'] + '", "memberType": "PERSON"}'
    URL = 'http://' + HOST + URL_API + 'groups/' + NEWGRP + '/members'
    response = requests.post(URL, data=post_data, headers=alflib.headers)
    #print(response.text)
