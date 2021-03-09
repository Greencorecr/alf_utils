#!/bin/env bash

chown -R alfresco:alfresco /opt/alfresco/alf_data
chown -R alfresco:alfresco /opt/alfresco/logs/
chown -R alfresco:alfresco /opt/alfresco/logs/solr6
chmod -R 755 /opt/alfresco/alf_data
chmod -R 2755 /opt/alfresco/alf_data/solr6/{content,models,index,solrhome}
chmod -R 2755 /opt/alfresco/logs/solr6
