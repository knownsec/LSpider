#!/bin/bash

kill -2 $(ps aux | grep SpiderCoreBackendStart|grep -v grep|awk '{print $2}')
sleep 1
kiil -9 $(ps aux | grep chrome|grep -v grep|awk '{print $2}')
kiil -9 $(ps aux | grep SpiderCoreBackendStart|grep -v grep|awk '{print $2}')

#kill -2 $(ps aux | grep xray |grep -v grep|awk '{print $2}')

chown www:www /home/wwwroot/default/xray/r*
#kill -2 $(ps aux | grep w13scan |grep -v grep|awk '{print $2}')