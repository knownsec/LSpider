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
from web.spider.controller.spider import SpiderCoreBackend

from utils.log import logger


class Command(BaseCommand):
    help = 'test for spider backend'

    def handle(self, *args, **options):

        SpiderCoreBackend()
        logger.info("[Spider Main] Spider finish.")