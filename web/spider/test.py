#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: test.py.py
@time: 2020/4/3 15:45
@desc:
'''


from django.test import TestCase
from django.utils import timezone

from .controller.spider import SpiderCore


class SpiderCoreTests(TestCase):

    def test_was_published_recently_with_future_question(self):

        scancore = SpiderCore()

        scancore.target_list.put({'url': 'https://lorexxar.cn', 'type': 'link', 'deep': 0})
        # scancore.target_list.put({'url': "https://cdn.jsdelivr.net/npm/jquery@3.3.1/dist/jquery.min.js", 'type': 'js', 'deep': 0})
        scancore.scan()

        return True
