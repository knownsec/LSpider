#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: project.py
@time: 2022/4/19 14:55
@desc:

'''

from __future__ import unicode_literals

import os
import json
import time
import codecs

from django.views import View
from django.http import HttpResponse, JsonResponse

from web.dashboard.models import Project, ProjectAssets, ProjectIps, ProjectVuls, VulType


class ProjectListView(View):
    """
        项目结果
    """

    @staticmethod
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


class ProjectDetailsView(View):
    """
        项目详情
    """

    @staticmethod
    def get(request, project_id):

        ps = Project.objects.filter(id=project_id, is_active=1).values()
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})


class ProjectAssetsDetailsView(View):
    """
        项目详情
    """

    @staticmethod
    def get(request, project_id):

        ps = ProjectAssets.objects.filter(project_id=project_id, is_active=1).values()
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})


class ProjectIpsDetailsView(View):
    """
        项目ip资产详情
    """

    @staticmethod
    def get(request, project_id):

        ps = ProjectIps.objects.filter(project_id=project_id, is_active=1).values()
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})


class ProjectVulsListsView(View):
    """
        项目漏洞列表
    """

    @staticmethod
    def get(request, project_id):

        ps = ProjectVuls.objects.filter(project_id=project_id, is_active=1).values()
        count = len(ps)

        ps_list = list(ps)

        for p in ps_list:
            p['details'] = ""

        return JsonResponse({"code": 200, "status": True, "message": ps_list, "total": count})


class ProjectVulsDetailsView(View):
    """
        项目漏洞详情
    """

    @staticmethod
    def get(request, project_id, vul_id):

        ps = ProjectVuls.objects.filter(project_id=project_id, id=vul_id, is_active=1).values()
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})
