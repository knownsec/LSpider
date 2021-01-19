#!/bin/bash

kill -2 $(ps aux | grep SpiderCoreBackendStart|grep -v grep|awk '{print $2}')
sleep 3
kill -9 $(ps aux | grep SpiderCoreBackendStart|grep -v grep|awk '{print $2}')
kill -9 $(ps aux | grep chrome|grep -v grep|awk '{print $2}')


chown www:www /home/wwwroot/default/xray/r*