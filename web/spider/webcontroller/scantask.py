#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: scantask.py
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
from web.spider.models import SubDomainList, UrlTable


class ScanTaskListView(View):
    """
        扫描任务
    """

    @staticmethod
    def get(request):
        size = 10
        page = 1
        target = ""
        task_name = ""

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "target" in request.GET or "task_name" in request.GET:
            target = request.GET['target'] if 'target' in request.GET else ""
            task_name = request.GET['task_name'] if 'task_name' in request.GET else ""

        if target or task_name:
            sts = ScanTask.objects.filter(target__contains=target, task_name__contains=task_name).values()[(page - 1) * size:page * size]
        else:
            sts = ScanTask.objects.all().values()[(page - 1) * size:page * size]
        count = len(sts)

        sts_list = list(sts)

        for st in sts_list:
            st['cookies'] = ""
            st['target'] = ""

        return JsonResponse({"code": 200, "status": True, "message": sts_list, "total": count, "keyword": target})


class ScanTaskDetailsView(View):
    """
        扫描任务
    """

    @staticmethod
    def get(request, task_id):

        sts = ScanTask.objects.filter(id=task_id).values()
        count = len(sts)

        return JsonResponse({"code": 200, "status": True, "message": list(sts), "total": count, })

    @staticmethod
    def post(request, task_id):
        st = ScanTask.objects.filter(id=task_id).first()

        if not st:
            return JsonResponse({"code": 404, "status": False, "message": "Task {} not Found.".format(task_id)})


class LoginPageListView(View):
    """
        登录页
    """

    @staticmethod
    def get(request):
        size = 10
        page = 1
        domain = ""

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "domain" in request.GET:
            domain = request.GET['domain']

        if domain:
            lpls = LoginPageList.objects.filter(domain__contains=domain).values()[(page - 1) * size:page * size]
        else:
            lpls = LoginPageList.objects.all().values()[(page - 1) * size:page * size]

        count = len(lpls)

        return JsonResponse({"code": 200, "status": True, "message": list(lpls), "total": count})


class LoginPageDetailsView(View):
    """
        登录页
    """

    @staticmethod
    def get(request, id):

        lpls = LoginPageList.objects.filter(id=id).values()
        count = len(lpls)

        return JsonResponse({"code": 200, "status": True, "message": list(lpls), "total": count, })


class BanListView(View):
    """
        ban
    """

    @staticmethod
    def get(request):
        size = 10
        page = 1

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        bls = BanList.objects.all().values()[(page - 1) * size:page * size]
        count = len(bls)

        return JsonResponse({"code": 200, "status": True, "message": list(bls), "total": count})


class BanListDetailsView(View):
    """
        登录页
    """

    @staticmethod
    def get(request, id):

        bls = BanList.objects.filter(id=id).values()
        count = len(bls)

        return JsonResponse({"code": 200, "status": True, "message": list(bls), "total": count, })


class AccountDataListView(View):
    """
        账户信息
    """

    @staticmethod
    def get(request):
        size = 10
        page = 1

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        adls = AccountDataTable.objects.all().values()[(page - 1) * size:page * size]
        count = len(adls)

        adls_list = list(adls)

        for ad in adls_list:
            ad['username'] = ""
            ad['password'] = ""
            ad['iphone'] = ""
            ad['cookies'] = ""

        return JsonResponse({"code": 200, "status": True, "message": adls_list, "total": count})


class AccountDataDetailsView(View):
    """
        账户信息
    """

    @staticmethod
    def get(request, id):

        adls = AccountDataTable.objects.filter(id=id).values()
        count = len(adls)

        return JsonResponse({"code": 200, "status": True, "message": list(adls), "total": count, })


class UrlTableListView(View):
    """
        urltable
    """

    @staticmethod
    def get(request):
        size = 100
        page = 1
        domain = ""

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "domain" in request.GET:
            domain = request.GET['domain']

        if domain:
            urls = UrlTable.objects.filter(domain__contains=domain).values()[(page - 1) * size:page * size]
        else:
            urls = UrlTable.objects.all().values()[(page - 1) * size:page * size]

        count = len(urls)

        urls_list = list(urls)

        return JsonResponse({"code": 200, "status": True, "message": urls_list, "total": count})


class SubDomainListView(View):
    """
        SubDomainList
    """

    @staticmethod
    def get(request):
        size = 20
        page = 1
        subdomain = ""
        banner = ""

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "subdomain" in request.GET or "banner" in request.GET:
            subdomain = request.GET['subdomain'] if 'subdomain' in request.GET else ""
            banner = request.GET['banner'] if 'banner' in request.GET else ""

        if subdomain or banner:
            sdls = SubDomainList.objects.filter(subdomain__contains=subdomain, banner__contains=banner).values()[(page - 1) * size:page * size]
        else:
            sdls = SubDomainList.objects.all().values()[(page - 1) * size:page * size]
        count = len(sdls)

        sdls_list = list(sdls)

        return JsonResponse({"code": 200, "status": True, "message": sdls_list, "total": count})
