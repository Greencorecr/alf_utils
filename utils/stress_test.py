'''
Valida si un servidor está corriendo a velocidades nominales para Alfresco
'''

import time
import os
import json
import random

HOST = '10.42.25.237'
NODE_URL = 'nodes/-root-/children'
URL = 'http://' + HOST + ':8080/alfresco/api/-default-/public/alfresco/versions/1/' + NODE_URL
CURL_OPTS1 = ' -X POST -F filedata=@./testfile -F "nodeType=cm:content" -F "cm:title=My text" '
CURL_OPTS2 = ' -F "cm:description=My text document description" -F "relativePath=My Folder" '
AUTH = ' -H "Authorization: Basic YWRtaW46YWRtaW4=" '

print("Prueba de subida. Subiendo un archivo de 50MiB, 25 veces")
test_start_time = time.time()

for _ in range(1, 25):
    start_time = time.time()
    RAND = str(random.randint(0, 10000))
    CURL_CMD = 'curl -s -F "name=somefile' + RAND +'.txt" ' + CURL_OPTS1 + CURL_OPTS2 + AUTH + URL
    result = os.popen(CURL_CMD).read()
    test_time = time.time() - start_time
    if test_time > 5:
        print("--- %s seconds ---" % test_time)
    else:
        print("OK")
test_test_time = time.time() - test_start_time
print("--- Test %s seconds ---" % test_test_time)

last_file = json.loads(result)


CURL_OPTS1 = 'curl -s -X GET --output /dev/null '
URL = 'http://10.42.25.237:8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/' + last_file['entry']['id'] + '/content'
print("Prueba de bajada. Descargando el archivo recién subido, de 50MiB, 25 veces")
test_start_time = time.time()

for _ in range(1, 25):
    start_time = time.time()
    RAND = str(random.randint(0, 10000))
    CURL_CMD = CURL_OPTS1 + AUTH + URL
    result = os.popen(CURL_CMD).read()
    test_time = time.time() - start_time
    if test_time > 5:
        print("--- %s seconds ---" % test_time)
    else:
        print("OK")
test_test_time = time.time() - test_start_time
print("--- Test %s seconds ---" % test_test_time)


