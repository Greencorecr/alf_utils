'''
Código común entre utilitarios para alfresco
'''
import base64

USER = 'admin'
PASSWD = 'admin'
USERPASS = USER + ':' + PASSWD
encoded_u = base64.b64encode(USERPASS.encode()).decode()
headers = {"Authorization" : "Basic %s" % encoded_u,
        "Accept" : "application/json" }
