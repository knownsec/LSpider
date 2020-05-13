#!/bin/bash

while :
do
    if [ $(ps aux | grep SpiderCoreBackendStart|grep -v grep|wc -l) -eq 0 ];then
        echo "start"
        /usr/bin/python3 /home/ubuntu/lorexxar/LSpider/manage.py SpiderCoreBackendStart
    fi
    sleep 100
done
