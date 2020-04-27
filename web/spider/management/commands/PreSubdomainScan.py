#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: PreSubdomainScan.py
@time: 2020/4/27 18:24
@desc:
'''

from django.core.management.base import BaseCommand
from web.spider.controller.prescan import PrescanCore

from utils.log import logger

import sys
import traceback
from queue import Queue, Empty


class Command(BaseCommand):
    help = 'pre subdomain scan'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('domain', type=str)

    def handle(self, *args, **options):

        try:
            if 'domain' not in options:
                logger.error('[PreScan] no domain input.')
                sys.exit(0)

            logger.info("[PreScan] Hackerone {} Scope spider start.".format(options['domain']))
            h = PrescanCore()
            result_list = h.start(options['domain'], False)

            for result in result_list:
                print(result)

        except KeyboardInterrupt:
            logger.warn("[PreScan] stop Scan.")
            sys.exit(0)
        except:
            logger.error("[PreScan] something error, {}".format(traceback.format_exc()))
