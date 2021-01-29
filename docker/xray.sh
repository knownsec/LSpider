#!/bin/sh

while :
do
    if [ $(ps aux | grep xray_linux_amd64|grep -v grep|wc -l) -eq 0 ];then
        echo "start"
        /opt/xray/xray_linux_amd64 webscan --listen 127.0.0.1:7777 --html-output /opt/xray/r__datetime__.html
    fi
    sleep 10
done
