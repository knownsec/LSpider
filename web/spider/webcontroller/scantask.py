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

from utils.base import check_gpc_undefined


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
            sts = ScanTask.objects.filter(target__contains=target, task_name__contains=task_name).values()[
                  (page - 1) * size:page * size]
        else:
            sts = ScanTask.objects.all().values()[(page - 1) * size:page * size]
        count = len(sts)

        sts_list = list(sts)

        for st in sts_list:
            st['cookies'] = ""
            st['target'] = ""

        return JsonResponse({"code": 200, "status": True, "message": sts_list, "total": count, "keyword": target})

    @staticmethod
    def post(request):
        params = json.loads(request.body)

        task_name = check_gpc_undefined(params, "task_name")
        target = check_gpc_undefined(params, "target")
        target_type = check_gpc_undefined(params, "target_type")
        task_tag = check_gpc_undefined(params, "task_tag")
        cookies = check_gpc_undefined(params, "cookies")
        is_active = check_gpc_undefined(params, "is_active", 1)
        is_emergency = check_gpc_undefined(params, "is_emergency", 0)
        is_finished = check_gpc_undefined(params, "is_finished", 1)

        s1 = ScanTask.objects.filter(task_name=task_name).first()
        if s1:
            return JsonResponse({"code": 500, "status": False, "message": "Task {} is exists".format(task_name)})

        s = ScanTask(task_name=task_name, target=target, target_type=target_type, task_tag=task_tag,
                     cookies=cookies, is_active=is_active,
                     is_emergency=is_emergency, is_finished=is_finished)
        s.save()

        return JsonResponse({"code": 200, "status": True, "message": "New Task successful"})


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
        params = json.loads(request.body)

        st = ScanTask.objects.filter(id=task_id).first()

        task_name = check_gpc_undefined(params, "task_name")
        target = check_gpc_undefined(params, "target")
        target_type = check_gpc_undefined(params, "target_type")
        target_tag = check_gpc_undefined(params, "description")
        last_scan_time = check_gpc_undefined(params, "last_scan_time")
        cookies = check_gpc_undefined(params, "cookies")
        is_active = check_gpc_undefined(params, "is_active", 1)
        is_emergency = check_gpc_undefined(params, "is_emergency", 0)
        is_finished = check_gpc_undefined(params, "is_finished", 1)

        if st:
            st.task_name = task_name
            st.target = target
            st.target_type = target_type
            st.target_tag = target_tag
            st.last_scan_time = last_scan_time
            st.cookies = cookies
            st.is_active = is_active
            st.is_emergency = is_emergency
            st.is_finished = is_finished
            st.save()
            return JsonResponse({"code": 200, "status": True, "message": "Update Task successful"})
        else:
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

    @staticmethod
    def post(request):
        params = json.loads(request.body)

        domain = check_gpc_undefined(params, "domain")
        url = check_gpc_undefined(params, "url")
        title = check_gpc_undefined(params, "title")
        is_active = check_gpc_undefined(params, "is_active", 1)

        lpls = LoginPageList.objects.filter(domain=domain).first()
        if lpls:
            return JsonResponse({"code": 500, "status": False, "message": "Domain {} is exists".format(domain)})

        lp = LoginPageList(domain=domain, url=url, title=title, is_active=is_active)
        lp.save()

        return JsonResponse({"code": 200, "status": True, "message": "New LoginPage successful"})


class LoginPageDetailsView(View):
    """
        登录页
    """

    @staticmethod
    def get(request, id):
        lpls = LoginPageList.objects.filter(id=id).values()
        count = len(lpls)

        return JsonResponse({"code": 200, "status": True, "message": list(lpls), "total": count, })

    @staticmethod
    def post(request, id):
        params = json.loads(request.body)

        lpls = LoginPageList.objects.filter(id=id).first()

        domain = check_gpc_undefined(params, "domain")
        url = check_gpc_undefined(params, "url")
        title = check_gpc_undefined(params, "title")
        is_active = check_gpc_undefined(params, "is_active", 1)

        if lpls:
            lpls.domain = domain
            lpls.url = url
            lpls.title = title
            lpls.is_active = is_active
            lpls.save()
            return JsonResponse({"code": 200, "status": True, "message": "Update LoginPage successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "LoginPage {} not Found.".format(id)})


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

    @staticmethod
    def post(request):
        params = json.loads(request.body)

        ban_name = check_gpc_undefined(params, "ban_name")
        ban_domain = check_gpc_undefined(params, "ban_domain")
        is_active = check_gpc_undefined(params, "is_active", 1)

        bls = BanList.objects.filter(ban_name=ban_name).first()
        if bls:
            return JsonResponse({"code": 500, "status": False, "message": "Ban name {} is exists".format(ban_name)})

        bls = BanList(ban_name=ban_name, ban_domain=ban_domain, is_active=is_active)
        bls.save()

        return JsonResponse({"code": 200, "status": True, "message": "New Ban successful"})


class BanListDetailsView(View):
    """
        登录页
    """

    @staticmethod
    def get(request, id):
        bls = BanList.objects.filter(id=id).values()
        count = len(bls)

        return JsonResponse({"code": 200, "status": True, "message": list(bls), "total": count, })

    @staticmethod
    def post(request, id):
        params = json.loads(request.body)

        bls = BanList.objects.filter(id=id).first()

        ban_name = check_gpc_undefined(params, "ban_name")
        ban_domain = check_gpc_undefined(params, "ban_domain")
        is_active = check_gpc_undefined(params, "is_active", 1)

        if bls:
            bls.ban_name = ban_name
            bls.ban_domain = ban_domain
            bls.is_active = is_active
            bls.save()
            return JsonResponse({"code": 200, "status": True, "message": "Update Ban successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Ban {} not Found.".format(id)})


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

    @staticmethod
    def post(request):
        params = json.loads(request.body)

        domain = check_gpc_undefined(params, "domain")
        username = check_gpc_undefined(params, "username")
        password = check_gpc_undefined(params, "password")
        iphone = check_gpc_undefined(params, "iphone")
        cookies = check_gpc_undefined(params, "cookies")

        adls = AccountDataTable.objects.filter(domain=domain).first()
        if adls:
            return JsonResponse({"code": 500, "status": False, "message": "Account Data in {} is exists".format(domain)})

        adls = AccountDataTable(domain=domain, username=username, password=password, iphone=iphone,cookies=cookies)
        adls.save()

        return JsonResponse({"code": 200, "status": True, "message": "New Account Data successful"})


class AccountDataDetailsView(View):
    """
        账户信息
    """

    @staticmethod
    def get(request, id):
        adls = AccountDataTable.objects.filter(id=id).values()
        count = len(adls)

        return JsonResponse({"code": 200, "status": True, "message": list(adls), "total": count, })

    @staticmethod
    def post(request, id):
        params = json.loads(request.body)

        adls = AccountDataTable.objects.filter(id=id).first()

        domain = check_gpc_undefined(params, "domain")
        username = check_gpc_undefined(params, "username")
        password = check_gpc_undefined(params, "password")
        iphone = check_gpc_undefined(params, "iphone")
        cookies = check_gpc_undefined(params, "cookies")

        if adls:
            adls.domain = domain
            adls.username = username
            adls.password = password
            adls.iphone = iphone
            adls.cookies = cookies
            adls.save()
            return JsonResponse({"code": 200, "status": True, "message": "Update AccountData successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "AccountData {} not Found.".format(id)})


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

    @staticmethod
    def post(request):
        params = json.loads(request.body)

        domain = check_gpc_undefined(params, "domain")
        url = check_gpc_undefined(params, "url")
        type = check_gpc_undefined(params, "type")
        scanid = check_gpc_undefined(params, "scanid", 0)

        urls = UrlTable.objects.filter(url=url).first()
        if urls:
            return JsonResponse({"code": 500, "status": False, "message": "url {} in urltable is exists".format(url)})

        urls = UrlTable(domain=domain, url=url, type=type, scanid=scanid)
        urls.save()

        return JsonResponse({"code": 200, "status": True, "message": "New Url successful"})


class UrlTableDetailsView(View):
    """

    """

    @staticmethod
    def get(request, id):
        urls = UrlTable.objects.filter(id=id).values()
        count = len(urls)

        return JsonResponse({"code": 200, "status": True, "message": list(urls), "total": count, })

    @staticmethod
    def post(request, id):
        params = json.loads(request.body)

        urls = UrlTable.objects.filter(id=id).first()

        domain = check_gpc_undefined(params, "domain")
        url = check_gpc_undefined(params, "url")
        type = check_gpc_undefined(params, "type")
        scanid = check_gpc_undefined(params, "scanid", 0)

        if urls:
            urls.domain = domain
            urls.url = url
            urls.type = type
            urls.scanid = scanid
            urls.save()
            return JsonResponse({"code": 200, "status": True, "message": "Update Url successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Url {} not Found.".format(id)})


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
            sdls = SubDomainList.objects.filter(subdomain__contains=subdomain, banner__contains=banner).values()[
                   (page - 1) * size:page * size]
        else:
            sdls = SubDomainList.objects.all().values()[(page - 1) * size:page * size]
        count = len(sdls)

        sdls_list = list(sdls)

        return JsonResponse({"code": 200, "status": True, "message": sdls_list, "total": count})

    @staticmethod
    def post(request):
        params = json.loads(request.body)

        subdomain = check_gpc_undefined(params, "subdomain")
        title = check_gpc_undefined(params, "title")
        lastscan = check_gpc_undefined(params, "lastscan")
        banner = check_gpc_undefined(params, "banner")
        is_emergency = check_gpc_undefined(params, "is_emergency", 0)
        is_finished = check_gpc_undefined(params, "is_finished", 0)

        sdls = SubDomainList.objects.filter(subdomain=subdomain).first()
        if sdls:
            return JsonResponse({"code": 500, "status": False, "message": "Subdomain {}  is exists".format(subdomain)})

        sdls = SubDomainList(subdomain=subdomain, title=title, lastscan=lastscan, banner=banner,
                             is_emergency=is_emergency, is_finished=is_finished)
        sdls.save()

        return JsonResponse({"code": 200, "status": True, "message": "New Subdomain successful"})


class SubDomainDetailsView(View):
    """

    """

    @staticmethod
    def get(request, id):
        sdls = SubDomainList.objects.filter(id=id).values()
        count = len(sdls)

        return JsonResponse({"code": 200, "status": True, "message": list(sdls), "total": count, })

    @staticmethod
    def post(request, id):
        params = json.loads(request.body)

        sdls = SubDomainList.objects.filter(id=id).first()

        subdomain = check_gpc_undefined(params, "subdomain")
        title = check_gpc_undefined(params, "title")
        lastscan = check_gpc_undefined(params, "lastscan")
        banner = check_gpc_undefined(params, "banner")
        is_emergency = check_gpc_undefined(params, "is_emergency", 0)
        is_finished = check_gpc_undefined(params, "is_finished", 0)

        if sdls:
            sdls.subdomain = subdomain
            sdls.title = title
            sdls.lastscan = lastscan
            sdls.banner = banner
            sdls.is_emergency = is_emergency
            sdls.is_finished = is_finished
            sdls.save()
            return JsonResponse({"code": 200, "status": True, "message": "Update Subdomain successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Subdomain {} not Found.".format(id)})

