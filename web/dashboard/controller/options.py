#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: profile.py
@time: 2022/4/27 16:40
@desc:

'''

from __future__ import unicode_literals

import os
import json
import time
import codecs

from django.views import View
from django.http import HttpResponse, JsonResponse

from web.dashboard.models import VulType
from LSpider.const import *


class VulTypeListView(View):
    """
        漏洞类型列表
    """

    @staticmethod
    def get(request):

        ps = VulType.objects.all().values()
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})


def ProjectType(request):
    return JsonResponse({"code": 200, "status": True, "message": PROJECT_TYPE_LIST})


def ProjectAssertsType(request):
    return JsonResponse({"code": 200, "status": True, "message": PROJECT_ASSERTS_TYPE_LIST})


def ProjectAssertsSeverity(request):
    return JsonResponse({"code": 200, "status": True, "message": PROJECT_ASSERTS_SEVERITYS})


def ProjectVulsSeverity(request):
    return JsonResponse({"code": 200, "status": True, "message": PROJECT_VULS_SEVERITY})


def ScaVulsSeverity(request):
    return JsonResponse({"code": 200, "status": True, "message": SCA_VULS_SEVERITY})
