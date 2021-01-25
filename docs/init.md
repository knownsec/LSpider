# 初始化文档

爬虫配置指南，本文列举了xray配合搭建指南

# 配置xray

1、 上传xray，添加执行权限
2、 glone poc

```bash
git clone https://github.com/chaitin/xray.git
```

3、配置启动脚本

```bash
./xray_linux_amd64 webscan --listen 127.0.0.1:7777 --html-output /home/wwwroot/default/xray/a.html
```

# 安装Mysql以及RabbitMQ

由于LSpider没有设计专门的管理界面，所以建议使用LNMP配套环境，使用phpmyadmin管理任务

安装步骤可以参考

- [LNMP](https://lnmp.org/)
- [PHPstudy](https://www.xp.cn/)

当然，你使用原生的Nginx+PHP+Mysql+数据库管理界面也完全可以。

RabbitMQ建议安装在另外的机器上，安装RabbitMQ之前需要先安装Erlang环境

具体可以参考
[https://www.rabbitmq.com/download.html](https://www.rabbitmq.com/download.html)

LSipder的配置与下面的配置文件相当即可。

# 配置LSpider

## 下载LSpider

```
git clone https://github.com/LoRexxar/LSpider.git
```

## 修改配置文件

```
cp LSpider/settings.py.bak LSpider/settings.py
```

并配置其中的rabbitmq、mysql等配置

## 配置环境

```
python3 -m pip install -r requirement.txt
```

如果mysqlclient无法安装，还需要提前安装

```
sudo apt-get install libmysqlclient-dev
```

## 同步数据库配置

```
python3 manage.py makemigrations
python3 manage.py migrate
```

数据库配置可能有版本问题，需要适配合适django和python版本

## 配置chrome headless

```
sudo wget http://www.linuxidc.com/files/repo/google-chrome.list -P /etc/apt/sources.list.d/

wget -q -O - https://dl.google.com/linux/linux_signing_key.pub  | sudo apt-key add -

sudo apt-get update

sudo apt-get install google-chrome-stable
```

看一下chrome的版本

```bash
lorexxar@instance-1:~/lorexxar/lspider/LSpider$ google-chrome --version
Google Chrome 81.0.4044.138 
```

去官网下载对应版本的webdriver放在bin目录下

[https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

修改名字
```bash
mv bin/chromedriver bin/chromedriver_linux64

```

chromedriver的名字需要符合
```
linux   chromedriver_linux64
windows chromedriver_win32.exe
mac     chromedriver_mac64
```

