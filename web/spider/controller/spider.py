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
from pika import exceptions as pika_exceptions
from queue import Queue, Empty
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from utils.LReq import LReq
from utils.log import logger
from utils.base import get_new_scan_id, get_now_scan_id
from utils.base import check_target

from core.htmlparser import html_parser
from core.urlparser import url_parser, checkbanlist
from core.threadingpool import ThreadPool
from core.rabbitmqhandler import RabbitmqHandler
from core.domainauthcheck import check_login_or_get_cookie

from LSpider.settings import LIMIT_DEEP, IS_OPEN_RABBITMQ
from LSpider.settings import IS_OPEN_CHROME_PROXY, CHROME_PROXY

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
        self.emergency_target_list = Queue()
        self.threadpool = ThreadPool()

        # rabbitmq init
        if IS_OPEN_RABBITMQ:
            self.rabbitmq_handler = RabbitmqHandler()

        t = threading.Thread(target=self.init_scan)
        t.start()
        time.sleep(3)

        # 如果队列为空，那么直接跳出
        if IS_OPEN_RABBITMQ:
            if not self.rabbitmq_handler.get_scan_ready_count() and not self.rabbitmq_handler.get_emergency_scan_ready_count():
                logger.info("[Spider Core] Spider Target Queue is empty.")
                return

        if not IS_OPEN_RABBITMQ and self.target_list.empty():
            logger.info("[Spider Core] Spider Target Queue is empty.")
            return

        self.scan_id = get_new_scan_id()

        if IS_OPEN_RABBITMQ:
            left_tasks = self.rabbitmq_handler.get_scan_ready_count()
            left_emergency_tasks = self.rabbitmq_handler.get_emergency_scan_ready_count()
        else:
            left_tasks = self.target_list.qsize()
            left_emergency_tasks = self.emergency_target_list.qsize()

        logger.info("[Spider Main] Spider id {} Start...now {} targets left.".format(self.scan_id, left_tasks))
        logger.info("[Spider Main] Emergency Task left {} targets.".format(left_emergency_tasks))

        # 获取线程池然后分发信息对象
        # 当有空闲线程时才继续
        i = 0

        # 启动2个线程用于紧急任务
        while i < 2:
            i += 1
            spidercore = SpiderCore(self.emergency_target_list)

            logger.debug("[Spider Core] New Thread {} for Spider Core.".format(i))

            if IS_OPEN_RABBITMQ:
                self.threadpool.new(spidercore.scancore, args=(True,))
            else:
                self.threadpool.new(spidercore.scan_for_queue)
            time.sleep(0.5)

        while 1:
            while self.threadpool.get_free_num():

                if i > 100:
                    logger.warning("[Spider Core] More than 100 thread init. stop new Thread.")
                    self.threadpool.wait_all_thread()
                    break

                else:
                    i += 1
                    spidercore = SpiderCore(self.target_list)

                    logger.debug("[Spider Core] New Thread {} for Spider Core.".format(i))

                    if IS_OPEN_RABBITMQ:
                        self.threadpool.new(spidercore.scancore)
                    else:
                        self.threadpool.new(spidercore.scan_for_queue)
                    time.sleep(0.5)

            # self.threadpool.wait_all_thread()
            time.sleep(1)

    def init_scan(self):

        tasklist = ScanTask.objects.filter(is_active=True, is_finished=False)
        new_task = False
        target_cookies = ""
        task_is_emergency = False

        for task in tasklist:
            lastscantime = datetime.datetime.strptime(str(task.last_scan_time)[:19], "%Y-%m-%d %H:%M:%S")
            nowtime = datetime.datetime.now()

            # if lastscantime:
                # if (nowtime - lastscantime).days > 90:
                # 3 mouth
                # 暂时改为单次扫描，每个任务标记并只扫描一次

            targets = check_target(task.target)
            target_type = task.target_type
            target_cookies = task.cookies
            task_is_emergency = task.is_emergency

            # 重设扫描时间
            task.last_scan_time = nowtime
            task.is_emergency = False
            task.is_finished = True
            task.save()

            for target in targets:

                if IS_OPEN_RABBITMQ:
                    if task_is_emergency:
                        self.rabbitmq_handler.new_emergency_scan_target(
                            json.dumps({'url': target, 'type': target_type, 'cookies': target_cookies, 'deep': 0}))
                    else:
                        self.rabbitmq_handler.new_scan_target(json.dumps({'url': target, 'type': target_type, 'cookies': target_cookies, 'deep': 0}))
                else:
                    self.target_list.put({'url': target, 'type': target_type, 'cookies': target_cookies, 'deep': 0})

                # subdomain scan
                domain = urlparse(target).netloc

                if domain:
                    PrescanCore().start(domain, is_emergency=task.is_emergency)

            # 每次只读一个任务，在一个任务后退出重启
            # 紧急任务不影响到普通任务
            if task_is_emergency:
                new_task = False
            else:
                new_task = True

            if new_task:
                # 每次只读一个任务，在一个任务后退出重启
                break

        logger.debug("[INIT Scan] Target init success.")

        subdomainlist = SubDomainList.objects.filter(is_finished=False)

        for subdomain in subdomainlist:
            lastscantime = datetime.datetime.strptime(str(subdomain.lastscan)[:19], "%Y-%m-%d %H:%M:%S")
            nowtime = datetime.datetime.now()

            if lastscantime:
                # if (nowtime - lastscantime).days > 30:

                # 1 mouth
                target = subdomain.subdomain.strip()

                if IS_OPEN_RABBITMQ:
                    if subdomain.is_emergency:
                        self.rabbitmq_handler.new_emergency_scan_target(json.dumps(
                            {'url': "http://" + target, 'type': 'link', 'cookies': target_cookies, 'deep': 0}))
                        self.rabbitmq_handler.new_emergency_scan_target(json.dumps(
                            {'url': "https://" + target, 'type': 'link', 'cookies': target_cookies, 'deep': 0}))

                    else:
                        self.rabbitmq_handler.new_scan_target(json.dumps({'url': "http://"+target, 'type': 'link', 'cookies': target_cookies, 'deep': 0}))
                        self.rabbitmq_handler.new_scan_target(json.dumps(
                            {'url': "https://" + target, 'type': 'link', 'cookies': target_cookies, 'deep': 0}))
                else:
                    self.target_list.put(
                        {'url': "http://"+target, 'type': 'link', 'cookies': target_cookies, 'deep': 0})
                    self.target_list.put(
                        {'url': "https://" + target, 'type': 'link', 'cookies': target_cookies, 'deep': 0})

                # 重设扫描时间
                subdomain.lastscan = nowtime
                subdomain.is_finished = True
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

    def scancore(self, is_emergency=False):
        # start
        if is_emergency:
            logger.info("[Scan Core] Emergency Scan Task start:>")
            self.rabbitmq_handler.start_emergency_scan_target(self.scan_emergency_task_distribute)
        else:
            logger.info("[Scan Core] Scan Task start:>")
            self.rabbitmq_handler.start_scan_target(self.scan_task_distribute)

    def scan_task_distribute(self, channel, method, header, message):

        # self.i += 1
        # if self.i > 10000:
        #     channel.basic_cancel(channel, nowait=False)
        #     # after target list finish
        #     self.req.close_driver()
        #     return False

        # 确认收到消息
        channel.basic_ack(delivery_tag=method.delivery_tag)

        try:
            # 获取任务信息
            task = json.loads(message)

            if checkbanlist(task['url']):
                logger.debug(("[Scan] ban domain exist...continue"))
                return False

            self.scan(task)
        except json.decoder.JSONDecodeError:
            task = eval(message)

            if checkbanlist(task['url']):
                logger.debug(("[Scan] ban domain exist...continue"))
                return False

            self.scan(task)

        except:
            # 任务启动错误则把任务重新插回去
            self.rabbitmq_handler.new_scan_target(message)
            time.sleep(0.5)
            return False

    def scan_emergency_task_distribute(self, channel, method, header, message):

        # self.i += 1
        # if self.i > 10000:
        #     channel.basic_cancel(channel, nowait=False)
        #     # after target list finish
        #     self.req.close_driver()
        #     return False

        # 确认收到消息
        channel.basic_ack(delivery_tag=method.delivery_tag)

        try:
            # 获取任务信息
            task = json.loads(message)

            if checkbanlist(task['url']):
                logger.debug(("[Scan] ban domain exist...continue"))
                return False

            self.scan(task, is_emergency=True)
        except json.decoder.JSONDecodeError:
            task = eval(message)

            if checkbanlist(task['url']):
                logger.debug(("[Scan] ban domain exist...continue"))
                return False

            self.scan(task, is_emergency=True)

        except:
            # 任务启动错误则把任务重新插回去
            self.rabbitmq_handler.new_emergency_scan_target(message)
            time.sleep(0.5)
            return False

    def scan_for_queue(self):

        i = 0

        while not self.target_list.empty() or i < 30:
            try:
                target = self.target_list.get(False)

                if checkbanlist(target['url']):
                    logger.debug(("[Scan] ban domain exist...continue"))
                    continue

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

    def scan(self, target, is_emergency=False):
        i = 0

        try:
            # sleep
            time.sleep(self.req.get_timeout())

            # target = self.target_list.get(False)
            code = -1
            content = False
            backend_cookies = ""
            title = ""

            if target['type'] == 'link':
                code, content, title = self.req.get(target['url'], 'RespByChrome', 0, target['cookies'])

            if target['type'] == 'js':
                code, content, title = self.req.get(target['url'], 'Resp', 0, target['cookies'])

            if code == -1:
                return

            if code == 2:
                # 代表这个页面需要登录
                backend_cookies = check_login_or_get_cookie(target['url'])

                # 任务塞到加急队列中
                new_target = target
                new_target['cookies'] = backend_cookies

                self.rabbitmq_handler.new_emergency_scan_target(json.dumps(new_target))

                return
            else:
                backend_cookies = target['cookies']

                # 如果为deep=0
                # 那么记录title
                if target['deep'] == 0:
                    domain = urlparse(target['url']).netloc

                    sd = SubDomainList.objects.filter(subdomain=domain).first()
                    sd.title = title
                    sd.save()

            result_list = html_parser(content)
            result_list = url_parser(target['url'], result_list, target['deep'], backend_cookies)

            # 继续把链接加入列表
            for target in result_list:

                if target['deep'] > LIMIT_DEEP:
                    continue

                # save to rabbitmq
                if IS_OPEN_RABBITMQ:
                    if is_emergency:
                        self.rabbitmq_handler.new_emergency_scan_target(json.dumps(target))
                    else:
                        self.rabbitmq_handler.new_scan_target(json.dumps(target))
                else:
                    self.target_list.put(target)

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

