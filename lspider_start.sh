#!/bin/bash

while :
do
    if [ $(ps aux | grep SpiderCoreBackendStart|grep -v grep|wc -l) -eq 0 ];then
        echo "start"
        nohup /usr/bin/python3 /home/ubuntu/lorexxar/LSpider/manage.py SpiderCoreBackendStart 2>&1 &

    fi
    sleep 600
done
