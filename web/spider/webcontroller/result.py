#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: result.py
@time: 2022/5/17 15:42
@desc:

'''


from __future__ import unicode_literals

import os
import json
import time
import codecs

from django.views import View
from django.http import HttpResponse, JsonResponse

from web.index.models import ScanTask, LoginPageList, BanList, AccountDataTable
from web.dashboard.models import Project
from web.index.middleware import login_level1_required, login_level2_required, login_level3_required, login_level4_required, login_required


class ProjectListView(View):
    """
        项目结果
    """

    @staticmethod
    @login_level4_required
    def get(request):
        size = 10
        page = 1
        project_type = 0

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "type" in request.GET:
            project_type = int(request.GET['type'])

        if not project_type:
            ps = Project.objects.filter(is_active=1).values()[(page-1)*size:page*size]
        else:
            ps = Project.objects.filter(type=project_type, is_active=1).values()[(page - 1) * size:page * size]

        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})
