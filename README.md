# LSpider

LSpider - 一个为被动扫描器定制的前端爬虫

# 什么是LSpider?

一款为被动扫描器而生的前端爬虫~

由Chrome Headless、LSpider主控、Mysql数据库、RabbitMQ、被动扫描器5部分组合而成。

(1) 建立在Chrome Headless基础上，将模拟点击和触发事件作为核心原理，通过设置代理将流量导出到被动扫描器。

(2) 通过内置任务+子域名api来进行发散式的爬取，目的经可能的触发对应目标域的流量。

(3) 通过RabbitMQ来进行任务管理，支持大量线程同时任务。

(4) 智能填充表单，提交表单等。

(5) 通过一些方式智能判断登录框，并反馈给使用者，使用者可以通过添加cookie的方式来完成登录。

(6) 定制了相应的Webhook接口，以供Webhook统计发送到微信。

(7) 内置了Hackerone、bugcrowd爬虫，提供账号的情况下可以一键获取某个目标的所有范围。

### 为什么选择LSpider?

LSpider是专门为被动扫描器定制的爬虫，许多功能都是为被动扫描器而服务的。

建立在RabbitMQ的任务管理系统相当稳定，可以长期在无人监管的情况下进行发散式的爬取。

### LSpider的最佳实践是什么？

**服务器1（2c4g以上）**: Nginx + Mysql + Mysql管理界面（phpmyadmin）

将被动扫描器的输出位置设置为web路径下，这样可以通过Web同时管理结果以及任务。

LSpider部署5线程以上，设置代理连接被动扫描器（被动扫描器可以设置专门的漏扫代理）

**服务器2**（非必要，但如果部署在服务器1，那么就需要更好的配置）：RabbitMQ

# Usage

[安装&使用](./docs/init.md)

你可以通过下面的命令来测试是否安装成功

```
python3 manage.py SpiderCoreBackendStart --test
```

**值得注意的是，以下脚本可能会涉及到项目路径影响，使用前请修改相应的配置**

启动LSpider webhook（默认端口2062）

```
./lspider_webhook.sh
```

启动LSpider
```
./lspider_start.sh
```

完全关闭LSpider
```
./lspider_stop.sh
```

启动被动扫描器
```
./xray.sh
```

# 一些关键的配置

Mysql配置
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'LSpider',
        'USER': 'root',
        'PASSWORD': 'lspider123!@#',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB;SET NAMES utf8mb4',
            'charset': 'utf8mb4',
        }
    }
}
```

LIMIT_DEEP为爬虫深度，即从目标开始直到第几层不再继续
THREADPOOL_MAX_THREAD_NUM 线程池数量
```
LIMIT_DEEP = 2
THREADPOOL_MAX_THREAD_NUM = 5
```

RabbitMQ配置，值得注意的是，建议使用RabbitMQ，因为基于队列的任务管理非常容易爆内存，无法解决。
```
# rabbitmq
RABBITMQ_IP = ""
RABBITMQ_PORT = ""
RABBITMQ_USERNAME = ""
RABBITMQ_PASSWORD = ""
RABBITMQ_VHOST = ""

# wheather open rabbitmq
IS_OPEN_RABBITMQ = True
```

Chrome Headless配置，将被动扫描器的代理填写在这里
```
# proxy for chrome headless
IS_OPEN_CHROME_PROXY = False
CHROME_PROXY = '127.0.0.1:7777'
```

Hackerone 账号配置
```
# for hackerone
HACKERONE_USERNAME = ""
HACKERONE_PASSWORD = ""
```

是否开启微信推送（配合webhook）,相关配置是推送到企业微信小程序的。
```
# loghander
LOGHANDER_IS_OPEN_WEIXIN = False

# for weixin
WECHAT_NOTICE = {
    'corp_id': ' ',
    'secret': ' ',
    'agent_id': ' ',
}
```

# 404StarLink
![](https://github.com/knownsec/404StarLink-Project/raw/master/logo.png)

LSpider 是 404Team [星链计划](https://github.com/knownsec/404StarLink-Project)中的一环，如果对LSpider有任何疑问又或是想要找小伙伴交流，可以参考星链计划的加群方式。

- [https://github.com/knownsec/404StarLink-Project#community](https://github.com/knownsec/404StarLink-Project#community)
