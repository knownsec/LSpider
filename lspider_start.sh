#!/bin/bash

while :
do
    if [ $(ps aux | grep SpiderCoreBackendStart|grep -v grep|wc -l) -eq 0 ];then
        echo "start"
        chmod 644 $(cd "$(dirname "$0")";pwd)/vuls/*
        python3 $(cd "$(dirname "$0")";pwd)/manage.py SpiderCoreBackendStart
    fi
    sleep 100
done
