#!/bin/bash

# Crea archivo de cron
cat << EOF | sudo tee /etc/cron.d/vencimientos

SHELL=/usr/bin/bash
# Revisamos vencimiento de documentos
0 6 * * * alfresco /usr/bin/python3 /opt/alfresco/notifica_vencimientos.py

EOF
