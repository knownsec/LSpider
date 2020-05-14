#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: spider.py
@time: 2020/3/12 15:54
@desc:
'''

import time
import datetime
import traceback
import threading
import json
from queue import Queue, Empty
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from utils.LReq import LReq
from utils.log import logger
from utils.base import get_new_scan_id, get_now_scan_id
from utils.base import check_target

from core.htmlparser import html_parser
from core.urlparser import url_parser
from core.threadingpool import ThreadPool
from core.rabbitmqhandler import RabbitmqHandler

from LSpider.settings import LIMIT_DEEP, IS_OPEN_RABBITMQ

from web.spider.models import UrlTable, SubDomainList
from web.index.models import ScanTask

from web.spider.controller.prescan import PrescanCore


class SpiderCoreBackend:
    """
    spider 守护线程
    """
    def __init__(self):
        # 任务与线程分发
        self.target_list = Queue()
        self.threadpool = ThreadPool()

        # rabbitmq init
        if IS_OPEN_RABBITMQ:
            self.rabbitmq_handler = RabbitmqHandler()

        t = threading.Thread(target=self.init_scan)
        t.start()
        time.sleep(3)

        # 如果队列为空，那么直接跳出
        if IS_OPEN_RABBITMQ and not self.rabbitmq_handler.get_scan_ready_count():
            logger.info("[Spider Core] Spider Target Queue is empty.")
            return

        if not IS_OPEN_RABBITMQ and self.target_list.empty():
            logger.info("[Spider Core] Spider Target Queue is empty.")
            return

        self.scan_id = get_new_scan_id()

        if IS_OPEN_RABBITMQ:
            left_tasks = self.rabbitmq_handler.get_scan_ready_count()
        else:
            left_tasks = self.target_list.qsize()

        logger.info("[Spider Main] Spider id {} Start...now {} targets left.".format(self.scan_id, left_tasks))

        # 获取线程池然后分发信息对象
        # 当有空闲线程时才继续
        for i in range(self.threadpool.get_free_num()):
            spidercore = SpiderCore(self.target_list)
            logger.debug("[Spider Core] New Thread {} for Spider Core.".format(i))

            if IS_OPEN_RABBITMQ:
                self.threadpool.new(spidercore.scancore)
            else:
                self.threadpool.new(spidercore.scan_for_queue)
            time.sleep(0.5)

        self.threadpool.wait_all_thread()

    def init_scan(self):

        tasklist = ScanTask.objects.filter(is_active=True)

        for task in tasklist:
            lastscantime = datetime.datetime.strptime(str(task.last_scan_time)[:19], "%Y-%m-%d %H:%M:%S")
            nowtime = datetime.datetime.now()
            target_cookies = ""

            if lastscantime:
                if (nowtime - lastscantime).days > 30:
                    # 1 mouth
                    targets = check_target(task.target)
                    target_type = task.target_type
                    target_cookies = task.cookies

                    for target in targets:

                        if IS_OPEN_RABBITMQ:
                            self.rabbitmq_handler.new_scan_target(json.dumps({'url': target, 'type': target_type, 'cookies': target_cookies, 'deep': 0}))
                        else:
                            self.target_list.put({'url': target, 'type': target_type, 'cookies': target_cookies, 'deep': 0})

                        # subdomain scan
                        domain = urlparse(target).netloc

                        if domain:
                            PrescanCore().start(domain)

                    # 重设扫描时间
                    task.last_scan_time = nowtime
                    task.save()

                    # 每次只读一个任务，在一个任务后退出重启
                    break

            SubDomainlist = SubDomainList.objects.filter()
            subdomainid = 1

            for subdomain in SubDomainlist:
                lastscantime = datetime.datetime.strptime(str(subdomain.lastscan)[:19], "%Y-%m-%d %H:%M:%S")
                nowtime = datetime.datetime.now()

                if lastscantime:
                    if (nowtime - lastscantime).days > 30:

                        # 子域名目标一次只读取50个，多了下次
                        # subdomainid += 1
                        # if subdomainid > 50:
                        #     break

                        # 1 mouth
                        target = subdomain.subdomain

                        if IS_OPEN_RABBITMQ:
                            self.rabbitmq_handler.new_scan_target(json.dumps({'url': "http://"+target, 'type': 'link', 'cookies': target_cookies, 'deep': 0}))
                        else:
                            self.target_list.put(
                                {'url': "http://"+target, 'type': 'link', 'cookies': target_cookies, 'deep': 0})

                        # 重设扫描时间
                        subdomain.lastscan = nowtime
                        subdomain.save()


class SpiderCore:
    """
    spider core thread
    """

    def __init__(self, target=Queue()):

        # rabbitmq init
        if IS_OPEN_RABBITMQ:
            self.rabbitmq_handler = RabbitmqHandler()

        # self.target = target
        self.target_list = target

        self.req = LReq(is_chrome=True)
        self.scan_id = get_now_scan_id()
        self.i = 1

    def scancore(self):
        # start
        logger.info("[Scan Core] Scan Task start:>")
        self.rabbitmq_handler.start_scan_target(self.scan_task_distribute)

    def scan_task_distribute(self, channel, method, header, message):

        self.i += 1
        if self.i > 10000:
            channel.basic_cancel(channel, nowait=False)
            # after target list finish
            self.req.close_driver()
            return False

        # 确认收到消息
        channel.basic_ack(delivery_tag=method.delivery_tag)

        try:
            # 获取任务信息
            task = json.loads(message)

            self.scan(task)
        except json.decoder.JSONDecodeError:
            task = eval(message)

            self.scan(task)
        except:
            # 任务启动错误则把任务重新插回去
            self.rabbitmq_handler.new_scan_target(message)
            time.sleep(0.5)
            return False

    def scan_for_queue(self):

        i = 0

        while not self.target_list.empty() or i < 30:
            try:
                target = self.target_list.get(False)

                self.scan(target)

            except KeyboardInterrupt:
                logger.error("[Scan] Stop Scaning.")
                self.req.close_driver()
                exit(0)

            except Empty:
                i += 1
                time.sleep(1)

            except:
                logger.warning('[Scan] something error, {}'.format(traceback.format_exc()))
                raise


    def scan(self, target):
        i = 0

        try:
            # sleep
            time.sleep(self.req.get_timeout())

            # target = self.target_list.get(False)
            content = False

            if target['type'] == 'link':
                content = self.req.get(target['url'], 'RespByChrome', 0, target['cookies'])

            if target['type'] == 'js':
                content = self.req.get(target['url'], 'Resp', 0, target['cookies'])

            if not content:
                return

            backend_cookies = target['cookies']

            result_list = html_parser(content)
            result_list = url_parser(target['url'], result_list, target['deep'], backend_cookies)

            # 继续把链接加入列表
            for target in result_list:

                # save to rabbitmq
                if IS_OPEN_RABBITMQ:
                    self.rabbitmq_handler.new_scan_target(json.dumps(target))
                else:
                    self.target_list.put(target)

                if target['deep'] > LIMIT_DEEP:
                    continue

                # self.target_list.put(target)

        except KeyboardInterrupt:
            logger.error("[Scan] Stop Scaning.")
            self.req.close_driver()
            exit(0)

        except Empty:
            i += 1
            time.sleep(1)

        except:
            logger.warning('[Scan] something error, {}'.format(traceback.format_exc()))
            raise

