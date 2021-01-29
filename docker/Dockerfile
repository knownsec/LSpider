#FROM ubuntu:16.04

FROM python:3.7.9-alpine3.12

Label author "qboy0000<2006qgw@163.com>"

#COPY dist/floodlight /root/floodlight

ENV XARY 1.7.0
ENV PYTHON3 3.7.9
ENV CHROMEDRIVER_VERSION 88.0.4324.96

# RUN sed -i 's/http:\/\/archive.ubuntu.com/http:\/\/mirrors.huaweicloud.com/g' /etc/apt/sources.list && \
#     sed -i 's/http:\/\/security.ubuntu.com/http:\/\/mirrors.huaweicloud.com/g' /etc/apt/sources.list && \
#     apt-get update && \

COPY ./requirement.txt /tmp/

RUN set -x && sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk update && \
# GM+8
# set time zone
	apk add --no-cache tzdata && \
	echo "Asia/Shanghai" > /etc/timezone && \
	cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
	# dpkg-reconfigure -f noninteractive tzdata && \
    apk add --no-cache musl-dev linux-headers  git wget curl unzip mysql-client mariadb-dev make gcc chromium chromium-chromedriver && \

# update python3 to 3.7
    # wget https://www.python.org/ftp/python/$PYTHON3/Python-$PYTHON3.tar.xz -O /tmp/Python-$PYTHON3.tar.xz && \
    # cd /tmp && tar -xvf Python-$PYTHON3.tar.xz && cd Python-$PYTHON3 && ./configure && make && make install && \

    git clone --depth 1 https://github.com/knownsec/LSpider.git /opt/LSpider && \

    cd /opt/LSpider/ && \
    pip3 install -r /tmp/requirement.txt -i https://mirrors.aliyun.com/pypi/simple && \

    wget https://download.xray.cool/xray/$XARY/xray_linux_amd64.zip -O /tmp/xray_linux_amd64.zip && \
    mkdir -p /opt/xray && \
    unzip /tmp/xray_linux_amd64.zip -d /opt/xray && \

    # wget http://npm.taobao.org/mirrors/chromedriver/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -O /tmp/chromedriver_linux64.zip && \
    # mkdir /opt/LSpider/bin && \
    # unzip /tmp/chromedriver_linux64.zip -d /usr/bin && \
    # mv /usr/bin/chromedriver /usr/bin/chromedriver_linux64 && \

    rm -rf /tmp/* && \
    apk del make gcc git

WORKDIR /opt/LSpider/
COPY ./docker-entrypoint.sh /opt/LSpider/docker-entrypoint.sh
COPY ./settings.py /opt/LSpider/LSpider/settings.py 
COPY ./xray.sh /opt/LSpider/xray.sh
COPY ./chromeheadless.py /opt/LSpider/core/

RUN chmod a+x /opt/LSpider/docker-entrypoint.sh && \
    chmod a+x /opt/LSpider/*.sh

EXPOSE 2062

CMD /opt/LSpider/docker-entrypoint.sh