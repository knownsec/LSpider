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
from web.index.middleware import login_level1_required, login_level2_required, login_level3_required, login_level4_required, login_required


class ProfileView(View):
    """
        配置
    """

    @staticmethod
    @login_level4_required
    def get(request):

        profile = {
            "WECHAT_USER_LIST": WECHAT_USER_LIST,
            "WECHAT_ADMIN_LIST": WECHAT_ADMIN_LIST,
        }

        return JsonResponse({"code": 200, "status": True, "message": profile})
