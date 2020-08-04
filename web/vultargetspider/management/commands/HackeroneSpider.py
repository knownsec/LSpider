#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: HackeroneSpider.py
@time: 2020/4/22 15:05
@desc:
'''

from django.core.management.base import BaseCommand

from web.vultargetspider.controller.hackerone import HackeroneSpider

from utils.log import logger

import sys
import traceback


class Command(BaseCommand):
    help = 'spider for hackerone'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('appname', type=str)

    def handle(self, *args, **options):

        try:
            if 'appname' not in options:
                logger.error('[Hackerone Spider] no appname input.')
                sys.exit(0)

            logger.info("[Hackerone Spider] Hackerone {} Scope spider start.".format(options['appname']))
            h = HackeroneSpider()
            result_list = h.spider(options['appname'])

            for result in result_list:
                print(result)

        except KeyboardInterrupt:
            logger.warn("[Spider] stop monitor.")
            sys.exit(0)
        except:
            logger.error("[Spider] something error, {}".format(traceback.format_exc()))
