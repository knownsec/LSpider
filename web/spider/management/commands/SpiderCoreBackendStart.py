#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: SpiderCoreBackendStart.py
@time: 2020/4/7 15:34
@desc:
'''

from django.core.management.base import BaseCommand
from web.spider.controller.spider import SpiderCoreBackend, SpiderCore

from utils.log import logger

import sys
import traceback
from queue import Queue, Empty


class Command(BaseCommand):
    help = 'test for spider backend'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--test', dest='test', action='store_true', default=False,
                            help='start for test')

    def handle(self, *args, **options):

        try:
            if not options['test']:
                SpiderCoreBackend()
            else:
                logger.info('[Spider] start test spider.')

                test_target_list = Queue()
                test_target_list.put({'url': "http://testphp.vulnweb.com", 'type': 'link', 'cookies': "_ga=GA1.2.625143521.1587463803; _gid=GA1.2.589830344.1587463803; language=zh-cn; _gat_UA-4118503-39=1; opref=source%3D(direct)%26medium%3Ddoc%26campaign%3D(direct)%26referrer%3D%26site%3Dopera_com%26sub%3D; _ym_uid=1587614813659891361; _ym_d=1587614813; _uetsid=_uetbcf63337-11c5-4738-b21e-f9270baad634; _ym_isad=1; _ym_visorc_43507159=b; _gat=1; csrftoken=mpEVjxTOaora5AQQUmWgE5sYIi4NNqTghqkv8IKJBpp4kkmS2P27X5P3WoArdGnw; sessionid=3bemzwoy181m0dcq7xufd84x0fbbq1ag", 'deep': 0})

                spidercore = SpiderCore(test_target_list)
                spidercore.scan()

        except KeyboardInterrupt:
            logger.warn("[Spider] stop scan.")
            sys.exit(0)
        except:
            logger.error("[Spider] something error, {}".format(traceback.format_exc()))