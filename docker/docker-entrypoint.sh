#!/bin/sh

#wait mysql & rabbitmq statup
sleep 20

mysql -u$MYSQL_USER -p$MYSQL_PASSWORD -h$MYSQL_HOST -P $MYSQL_PORT -e "CREATE DATABASE $MYSQL_DBName;"

python3 manage.py makemigrations
python3 manage.py migrate

sed -i 's/\/bin\/bash/\/bin\/sh/g'  lspider_webhook.sh
sed -i 's/\/bin\/bash/\/bin\/sh/g'  lspider_start.sh

nohup ./lspider_webhook.sh &
nohup ./lspider_start.sh &
./xray.sh