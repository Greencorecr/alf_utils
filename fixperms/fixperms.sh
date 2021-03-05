#!/bin/env bash

#cd /tmp  
#wget https://github.com/Greencorecr/alf_utils/raw/main/fixperms/template.tar.xz
#tar xJf template.tar.xz
#cd /opt/alfresco
#find . -print -exec chown --reference=/tmp/alfresco-perms/{} {} \; 2> /dev/null
chown -R alfresco:alfresco /opt/alfresco/alf_data
chown -R alfresco:alfresco /opt/alfresco/logs/

