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
                test_target_list.put({'url': "http://testphp.vulnweb.com", 'type': 'link', 'cookies': "PHPSESSID=malpd9t9qf68a861ppu17pfhf6; user_auth=95ced4640632f7f556a35ce1e0ed0bb7%3A5904be90c39e9f98196f41664a1c4efb;dy_did=e3ac6928cdaaed85c07bc19700061501; acf_did=e3ac6928cdaaed85c07bc19700061501; smidV2=2020042317420813a4a60257434f8522f4e2bc305ceb8600a8b33a84ef2dd40; PHPSESSID=43h3okfkdj10fegm021t9i0k44; acf_auth=2696tljFRsnqcLIzGYQGUlhz91VKMIIQsVxfp1H6WKJX%2Fjwud0vQL7lS06U8Y2e6gVcWkUsH2QvyEaaqSc9%2F8qCutF%2FTcBVZo5lel7IDqG3oPwG2709hTAE; dy_auth=a89eAynmL3g4svYibpYjL2XYAcmV8lEdDCMjcJRxA8qVYMlb42uiiLSXvu%2Bj1s2xKsAs9RomxRAdD5WwJ73X3t83sQIlnshQnuTfvsPXzQbtkQcOGAnkstA; wan_auth37wan=8b35b6ece202gfx3TOUMFS1LITut%2B6mHHB1VaLD7%2F0nP8GuOqIIxbgXHQxW0UT8CG6Q4dJsvBi2ZuEoOqXzN5eOFfz68QJn%2FbH41fWbyD8%2B%2FDSzQ; acf_uid=3634059; acf_username=qq_z5eCyVjt; acf_nickname=LoRexxar; acf_own_room=1; acf_groupid=1; acf_phonestatus=1; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favanew%2Fface%2F201711%2F20%2F20%2F68e7d0fe88c6f175eb345458b789c64b_; acf_ct=0; acf_ltkid=33139121; acf_biz=1; acf_stk=4fff6ee864f5aaeb; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1587634920,1587634944; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1587634944", 'deep': 0})

                spidercore = SpiderCore(test_target_list)
                spidercore.scan_for_queue()

        except KeyboardInterrupt:
            logger.warn("[Spider] stop scan.")
            sys.exit(0)
        except:
            logger.error("[Spider] something error, {}".format(traceback.format_exc()))
