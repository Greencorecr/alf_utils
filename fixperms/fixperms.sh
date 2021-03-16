#!/bin/env bash

apt-get -qy install wkhtmltopdf
if [ ! -L /usr/local/bin/wkhtmltopdf ]; then
  ln -s /usr/bin/wkhtmltopdf /usr/local/bin/
fi

cd /tmp  
wget -q https://github.com/Greencorecr/alf_utils/raw/main/fixperms/template.tar.xz
tar xJf template.tar.xz
cd /opt/alfresco
find . -print -exec chown -f --reference=/tmp/alfresco-perms/{} {} 2>/dev/null \; 2>&1 > /dev/null
find . -print -exec chmod -f --reference=/tmp/alfresco-perms/{} {} 2>/dev/null \; 2>&1 > /dev/null
find /opt/alfresco -uid 109 -exec chown -f alfresco:alfresco {} 2>/dev/null \; 2>&1 > /dev/null
rm -r /tmp/alfresco-perms /tmp/template.tar.xz

chown -f -R alfresco:alfresco /opt/alfresco/alf_data
chown -f -R alfresco:alfresco /opt/alfresco/logs/
chown -f -R alfresco:alfresco /opt/alfresco/logs/solr6
chmod -f -R 755 /opt/alfresco/alf_data
chmod -f -R 2755 /opt/alfresco/alf_data/solr6/{content,models,index,solrhome}
chmod -f -R 2755 /opt/alfresco/logs/solr6
