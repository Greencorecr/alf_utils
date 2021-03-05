#!/bin/env bash

cd /tmp  
wget https://github.com/Greencorecr/alf_utils/raw/main/fixperms/template.tar.xz
tar xJvf template.tar.xz
cd /opt/alfresco
find . -print -exec chown --reference=/tmp/alfresco-perms/{} {} \; 2> /dev/null
