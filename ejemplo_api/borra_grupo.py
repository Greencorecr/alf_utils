'''
Utilitario para borrar grupo
'''

import requests
import alflib

URL = 'http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/groups/GROUP_GrupoPrueba'

borrado = requests.delete(URL, headers=alflib.headers)
print(borrado.text)
