#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: threadingpool.py
@time: 2020/4/7 14:30
@desc:
'''


import time
import threading
import traceback

from LSpider.settings import THREADPOOL_MAX_THREAD_NUM
from utils.log import logger


class ThreadPool:
    """
    造一个线程池轮子
    """
    def __init__(self):

        self.max_thread_num = THREADPOOL_MAX_THREAD_NUM

        self.alive_thread_num = 0
        self.alive_thread_list = []

    def new(self, function, args=()):
        """
        新建线程
        :return:
        """
        # 检查存活线程
        self.check_status()

        if self.alive_thread_num < self.max_thread_num:

            # 先更新锁死
            self.alive_thread_num += 1

            try:
                t = threading.Thread(target=function, args=args)
                t.start()
                logger.debug("[ThreadPool] New Thread for function {} and args {}".format(str(function), args))

            except:
                logger.warning("[ThreadPool] Thread {} for function {} adn args {}. error: {}".format(t.name, function, args, traceback.format_exc()))
                self.alive_thread_num -= 1
                return False

            # 更新信息
            self.alive_thread_list.append(t)

            return True
        else:
            return False

    def check_status(self):
        """
        检查当前列表中的所有线程
        :return:
        """
        if self.alive_thread_num == 0:
            return True

        for t in self.alive_thread_list:
            if not t.is_alive():
                self.alive_thread_list.remove(t)
                self.alive_thread_num -= 1

        return True

    def get_free_num(self):
        """
        检查存活线程
        """
        self.check_status()

        return self.max_thread_num - self.alive_thread_num

    def wait_all_thread(self):
        """
        阻塞等待
        """
        for t in self.alive_thread_list:
            t.join()
