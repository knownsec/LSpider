#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: user.py
@time: 2022/8/30 18:35
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

from web.dashboard.models import UserProfile
from django.contrib.auth.models import User
from utils.base import check_gpc_undefined

from LSpider.settings import IS_OPEN_REGISTER
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from web.index.middleware import login_level1_required, login_level2_required, login_level3_required, login_level4_required, login_required


class UserListView(View):
    """
        用户列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        size = 10
        page = 1
        username = ""
        userdata_list = []

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "username" in request.GET:
            username = request.GET['username']

        if username:
            users = User.objects.filter(username__contains=username)[(page - 1) * size:page * size]
        else:
            users = User.objects.all()[(page - 1) * size:page * size]
        count = len(users)

        for user in users:
            userdata = {
                "id": user.id,
                "username": user.username,
                "nickname": user.username,
                "email": user.email,
                "last_login": user.last_login,
                "is_superuser": user.is_superuser,
                "is_staff": user.is_staff,
                "is_active": user.is_active,
            }
            user_profile = UserProfile.objects.filter(user_id=user.id).first()

            if user_profile:
                userdata["nickname"] = user_profile.nickname
                userdata["iphone"] = user_profile.iphone
                userdata["score"] = user_profile.score
                userdata["level"] = user_profile.level

            userdata_list.append(userdata)

        return JsonResponse({"code": 200, "status": True, "message": list(userdata_list), "total": count})


class UserListCountView(View):
    """
        用户名列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        count = User.objects.all().count()
        return JsonResponse({"code": 200, "status": True, "total": count})


class UserDetailsView(View):
    """
        用户名详情
    """

    @staticmethod
    @login_level4_required
    def get(request, user_id):
        userdata_list = []

        users = User.objects.filter(id=user_id)
        count = len(users)

        for user in users:
            userdata = {
                "id": user.id,
                "username": user.username,
                "nickname": user.username,
                "email": user.email,
                "iphone": "",
                "score": 0,
                "level": 0,
                "last_login": user.last_login,
                "is_superuser": user.is_superuser,
                "is_staff": user.is_staff,
                "is_active": user.is_active,
            }
            user_profile = UserProfile.objects.filter(user_id=user.id).first()

            if user_profile:
                userdata["nickname"] = user_profile.nickname
                userdata["iphone"] = user_profile.iphone
                userdata["score"] = user_profile.score
                userdata["level"] = user_profile.level

            userdata_list.append(userdata)

        return JsonResponse({"code": 200, "status": True, "message": list(userdata_list), "total": count})

    @staticmethod
    @login_level4_required
    def post(request, user_id):
        params = json.loads(request.body)

        user = User.objects.filter(id=user_id).first()

        username = check_gpc_undefined(params, "username")
        nickname = check_gpc_undefined(params, "nickname")
        email = check_gpc_undefined(params, "email")
        is_superuser = check_gpc_undefined(params, "is_superuser", 0)
        is_staff = check_gpc_undefined(params, "is_staff", 0)
        is_active = check_gpc_undefined(params, "is_active", 0)
        iphone = check_gpc_undefined(params, "iphone")
        score = check_gpc_undefined(params, "score", 0)
        level = check_gpc_undefined(params, "level", 1)

        if user:
            user.username = username
            user.email = email
            user.is_superuser = is_superuser
            user.is_active = is_active
            user.is_staff = is_staff

            userdata = UserProfile.objects.filter(user_id=user_id).first()

            if userdata:
                userdata.nickname = nickname
                userdata.iphone = iphone
                userdata.score = score
                userdata.level = level
                userdata.save()
            else:
                ud = UserProfile(user_id=user_id, nickname=nickname, iphone=iphone, score=score, level=level)
                ud.save()

            user.save()
            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "User not found"})


def signup(request):

    if not IS_OPEN_REGISTER:
        return JsonResponse({"code": 404, "status": False, "message": "Register is close."})

    if request.method == 'POST':
        params = json.loads(request.body)
        if params:
            username = check_gpc_undefined(params, "username")
            nickname = check_gpc_undefined(params, "nickname")
            password = check_gpc_undefined(params, "password")
            iphone = check_gpc_undefined(params, "iphone")
            email = check_gpc_undefined(params, "email")

            u = User.objects.filter(username=username).first()
            if not u:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()

                user_profile = UserProfile(user_id=user.id, nickname=nickname, iphone=iphone, level=1, score=0)
                user_profile.save()

                auth.login(request, user)
                return JsonResponse({"code": 200, "status": True, "message": "Register successful"})
            else:
                return JsonResponse({"code": 404, "status": False, "message": "User is exist."})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Something error."})
    else:
        return JsonResponse({"code": 404, "status": False, "message": "Something error."})


def signin(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        username = check_gpc_undefined(params, "username")
        password = check_gpc_undefined(params, "password")

        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            return JsonResponse({"code": 200, "status": True, "message": "login successful"})
        else:
            messages.add_message(request, messages.ERROR, "Username or Password is incorrect.")
            return JsonResponse({"code": 404, "status": False, "message": "User or Password is incorrect."})
    else:
        return JsonResponse({"code": 404, "status": False, "message": "Something error."})


def logout(req):
    auth.logout(req)
    return JsonResponse({"code": 200, "status": True, "message": "login out successful"})


class UserDetaView(View):
    """
        当前用户详情
    """

    @staticmethod
    @login_level1_required
    def get(request):
        userdata_list = []

        if request.user.is_authenticated:
            username = request.user.username
        else:
            return JsonResponse({"code": 404, "status": False, "message": "login required."})

        users = User.objects.filter(username=username)
        count = len(users)

        for user in users:
            userdata = {
                "id": user.id,
                "username": user.username,
                "nickname": user.username,
                "email": user.email,
                "iphone": "",
                "score": 0,
                "level": 0,
                "last_login": user.last_login,
                "is_superuser": user.is_superuser,
                "is_staff": user.is_staff,
                "is_active": user.is_active,
            }
            user_profile = UserProfile.objects.filter(user_id=user.id).first()

            if user_profile:
                userdata["nickname"] = user_profile.nickname
                userdata["iphone"] = user_profile.iphone
                userdata["score"] = user_profile.score
                userdata["level"] = user_profile.level

            userdata_list.append(userdata)

        return JsonResponse({"code": 200, "status": True, "message": list(userdata_list), "total": count})