'''
Utilitario para crear grupo
'''

import json
import re
import requests
import alflib

URL = 'http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/groups'

string="GrupoPrueba"

print("Creando grupo llamado: ", string)
post_data='{"id": "' + string + '", "displayName": "' + string + '"}'
response = requests.post(URL, data=post_data, headers=alflib.headers)
print(response.text)
