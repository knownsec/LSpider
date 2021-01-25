Mysql配置

值得注意的是，如果django版本变化，这部分配置可能发生变化
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

<del>Chrome访问到的文件储存位置</del>已废弃，默认下载到/dev/null
```
CHROME_DOWNLOAD_PATH = '/tmp/lspider'
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

Chrome Headless配置，将被动扫描器的代理填写在这里，建议开启
```
# proxy for chrome headless
IS_OPEN_CHROME_PROXY = True
CHROME_PROXY = '127.0.0.1:7777'
```

Hackerone 账号配置，只有配置完成之后才可以使用Hackerone爬虫
```
# for hackerone
HACKERONE_USERNAME = ""
HACKERONE_PASSWORD = ""
```

是否开启微信推送（配合webhook）,相关配置是推送到企业微信小程序的。

其中，debug为传送一些debug信息的配置，WECHAT_NOTICE为传输结果的配置。

其中各个配置可以参考企业微信小程序处id
```
# loghander
LOGHANDER_IS_OPEN_WEIXIN = False

# for weixin
WECHAT_NOTICE = {
    'corp_id': ' ',
    'secret': ' ',
    'agent_id': ' ',
}

WECHAT_NOTICE_DEBUG = {
    'corp_id': ' ',
    'secret': ' ',
    'agent_id': ' ',
}
```

如果开启这个配置，Chrome webdriver 会以非headless的模式启动，便于调试环境
```
# for test 
IS_TEST_ENVIRONMENT = False
```
