#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: logs.py
@time: 2022/11/7 17:14
@desc:

'''
from __future__ import unicode_literals

import os
import json
import time
import codecs

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from web.index.models import BackendLog, FrontLog
from django.contrib.auth.models import User
from utils.base import check_gpc_undefined

from web.index.middleware import login_level1_required, login_level2_required, login_level3_required, login_level4_required, login_required


class BackendLogListView(View):
    """
        日志列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        size = 10
        page = 1
        type = ""

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "type" in request.GET:
            type = request.GET['type']

        if type:
            backendlogs = BackendLog.objects.filter(type__contains=type).values()[::-1][(page - 1) * size:page * size]
        else:
            backendlogs = BackendLog.objects.all().values()[::-1][(page - 1) * size:page * size]
        count = len(backendlogs)

        return JsonResponse({"code": 200, "status": True, "message": list(backendlogs), "total": count})

    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        log_type = check_gpc_undefined(params, "type")
        log_text = check_gpc_undefined(params, "log_text")

        bl = BackendLog(type=log_type, log_text=log_text, is_active=1)
        bl.save()
        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


class BackendLogListCountView(View):
    """
        日志列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        type = ""

        if "type" in request.GET:
            type = request.GET['type']

        if type:
            count = BackendLog.objects.filter(type__contains=type).count()
        else:
            count = BackendLog.objects.all().count()
        return JsonResponse({"code": 200, "status": True, "total": count})


class BackendLogDetailsView(View):
    """
        日志详情
    """

    @staticmethod
    @login_level4_required
    def get(request, log_id):
        backendlog_list = []

        backendlogs = BackendLog.objects.filter(id=log_id)
        count = len(backendlogs)

        for backendlog in backendlogs:
            backendlogdata = {
                "id": backendlog.id,
                "type": backendlog.type,
                "log_text": backendlog.log_text,
                "log_time": backendlog.log_time,
                "is_active": backendlog.is_active,
            }

            backendlog_list.append(backendlogdata)

        return JsonResponse({"code": 200, "status": True, "message": list(backendlog_list), "total": count})

    @staticmethod
    @login_level4_required
    def post(request, log_id):
        params = json.loads(request.body)

        backendlog = BackendLog.objects.filter(id=log_id).first()

        log_type = check_gpc_undefined(params, "type")
        log_text = check_gpc_undefined(params, "log_text")
        is_active = check_gpc_undefined(params, "is_active", 0)

        if backendlog:
            backendlog.type = log_type
            backendlog.log_text = log_text
            backendlog.is_active = is_active
            backendlog.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Backend Log not found"})


class FrontLogListView(View):
    """
        日志列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        size = 10
        page = 1
        username = ""
        frontlog_list = []

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "username" in request.GET:
            username = request.GET['username']

        if not username:
            frontlogs = FrontLog.objects.all()[::-1][(page - 1) * size:page * size]
        else:
            user = User.objects.filter(username=username).first()

            if user:
                frontlogs = FrontLog.objects.filter(user_id=user.id)[::-1][(page - 1) * size:page * size]
            else:
                return JsonResponse({"code": 404, "status": False, "message": "bad request."})

        count = len(frontlogs)

        for frontlog in frontlogs:

            user_id = frontlog.user_id
            user = User.objects.filter(id=user_id).first()
            if user:
                username = user.username

            frontlogdata = {
                "id": frontlog.id,
                "username": username,
                "type": frontlog.type,
                "log_text": frontlog.log_text,
                "log_time": frontlog.log_time,
                "is_active": frontlog.is_active,
            }
            user = User.objects.filter(id=frontlog.user_id).first()

            if user:
                frontlogdata["username"] = user.username

            frontlog_list.append(frontlogdata)

        return JsonResponse({"code": 200, "status": True, "message": list(frontlog_list), "total": count})

    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        user_id = check_gpc_undefined(params, "user_id", 1)
        log_type = check_gpc_undefined(params, "type")
        log_text = check_gpc_undefined(params, "log_text")

        fl = FrontLog(user_id=user_id, type=log_type, log_text=log_text, is_active=1)
        fl.save()
        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


class FrontLogListCountView(View):
    """
        日志列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        username = ""
        if "username" in request.GET:
            username = request.GET['username']

        if not username:
            count = FrontLog.objects.all().count()
        else:
            user = User.objects.filter(username=username).first()

            if user:
                count = FrontLog.objects.filter(user_id=user.id).count()
            else:
                return JsonResponse({"code": 404, "status": False, "message": "bad request."})

        return JsonResponse({"code": 200, "status": True, "total": count})


class FrontLogDetailsView(View):
    """
        日志详情
    """

    @staticmethod
    @login_level4_required
    def get(request, log_id):
        frontlog_list = []

        frontlogs = FrontLog.objects.filter(id=log_id)
        count = len(frontlogs)

        for frontlog in frontlogs:
            frontlogdata = {
                "id": frontlog.id,
                "user_id": frontlog.user_id,
                "type": frontlog.type,
                "log_text": frontlog.log_text,
                "log_time": frontlog.log_time,
                "is_active": frontlog.is_active,
            }

            frontlog_list.append(frontlogdata)

        return JsonResponse({"code": 200, "status": True, "message": list(frontlog_list), "total": count})

    @staticmethod
    @login_level4_required
    def post(request, log_id):
        params = json.loads(request.body)

        frontlog = FrontLog.objects.filter(id=log_id).first()

        log_type = check_gpc_undefined(params, "type")
        log_text = check_gpc_undefined(params, "log_text")
        is_active = check_gpc_undefined(params, "is_active", 0)

        if frontlog:
            frontlog.type = log_type
            frontlog.log_text = log_text
            frontlog.is_active = is_active
            frontlog.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Front Log not found"})


class NowFrontLogDataView(View):
    """
        当前log详情
    """

    @staticmethod
    @login_level1_required
    def get(request):
        size = 10
        page = 1

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if request.user.is_authenticated:
            username = request.user.username
        else:
            return JsonResponse({"code": 404, "status": False, "message": "login required."})

        nowuser = User.objects.filter(username=username).first()

        if nowuser:
            frontlogs = FrontLog.objects.filter(user_id=nowuser.id).values()[::-1][(page - 1) * size:page * size]
            count = len(frontlogs)

            return JsonResponse({"code": 200, "status": True, "message": list(frontlogs), "total": count})

        return JsonResponse({"code": 404, "status": False, "message": "Front Log not found"})


class NowFrontLogListCountView(View):
    """
        日志列表
    """

    @staticmethod
    @login_level1_required
    def get(request):
        if request.user.is_authenticated:
            username = request.user.username
        else:
            return JsonResponse({"code": 404, "status": False, "message": "login required."})

        nowuser = User.objects.filter(username=username).first()
        count = 0

        if nowuser:
            frontlogs = FrontLog.objects.filter(user_id=nowuser.id)
            count = len(frontlogs)
        return JsonResponse({"code": 200, "status": True, "total": count})
