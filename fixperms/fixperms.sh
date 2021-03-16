#!/bin/env bash

apt-get -qy install wkhtmltopdf
if [ ! -L /usr/local/bin/wkhtmltopdf ]; then
  ln -s /usr/bin/wkhtmltopdf /usr/local/bin/
fi

cd /tmp  
wget https://github.com/Greencorecr/alf_utils/raw/main/fixperms/template.tar.xz
tar xJf template.tar.xz
cd /opt/alfresco
find . -print -exec chown --reference=/tmp/alfresco-perms/{} {} \; 2> /dev/null
find . -print -exec chmod --reference=/tmp/alfresco-perms/{} {} \; 2> /dev/null
find /opt/alfresco -uid 109 -exec echo chown alfresco:alfresco {} \;
rm -r /tmp/alfresco-perms /tmp/template.tar.xz

chown -R alfresco:alfresco /opt/alfresco/alf_data
chown -R alfresco:alfresco /opt/alfresco/logs/
chown -R alfresco:alfresco /opt/alfresco/logs/solr6
chmod -R 755 /opt/alfresco/alf_data
chmod -R 2755 /opt/alfresco/alf_data/solr6/{content,models,index,solrhome}
chmod -R 2755 /opt/alfresco/logs/solr6
