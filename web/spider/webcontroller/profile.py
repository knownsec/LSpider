#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: profile.py
@time: 2022/5/17 15:41
@desc:

'''

from __future__ import unicode_literals

import os
import json
import time
import codecs

from django.views import View
from django.http import HttpResponse, JsonResponse

from LSpider.settings import WECHAT_USER_LIST, WECHAT_ADMIN_LIST


class ProfileView(View):
    """
        配置
    """

    @staticmethod
    def get(request):

        profile = {
            "WECHAT_USER_LIST": WECHAT_USER_LIST,
            "WECHAT_ADMIN_LIST": WECHAT_ADMIN_LIST,
        }

        return JsonResponse({"code": 200, "status": True, "message": profile})
