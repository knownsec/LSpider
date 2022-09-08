#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: middleware.py
@time: 2022/9/7 19:34
@desc:

'''

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from web.dashboard.models import UserProfile
from django.contrib.auth.models import User


def login_level1_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            u = User.objects.filter(username=request.user.username).first()

            if not u:
                return JsonResponse({"code": 403, "status": False, "message": "login required."})

            up = UserProfile.objects.filter(user_id=u.id).first()

            if not up:
                return JsonResponse({"code": 403, "status": False, "message": "something error."})

            level = up.level

            if not level > 0:
                return JsonResponse({"code": 403, "status": False, "message": "you can't do its."})

            return function(request, *args, **kwargs)
        else:
            return JsonResponse({"code": 403, "status": False, "message": "login required."})

    return wrapper


def login_level2_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            u = User.objects.filter(username=request.user.username).first()

            if not u:
                return JsonResponse({"code": 403, "status": False, "message": "login required."})

            up = UserProfile.objects.filter(user_id=u.id).first()

            if not up:
                return JsonResponse({"code": 403, "status": False, "message": "something error."})

            level = up.level

            if not level > 1:
                return JsonResponse({"code": 403, "status": False, "message": "you can't do its."})

            return function(request, *args, **kwargs)
        else:
            return JsonResponse({"code": 403, "status": False, "message": "login required."})

    return wrapper


def login_level3_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            u = User.objects.filter(username=request.user.username).first()

            if not u:
                return JsonResponse({"code": 403, "status": False, "message": "login required."})

            up = UserProfile.objects.filter(user_id=u.id).first()

            if not up:
                return JsonResponse({"code": 403, "status": False, "message": "something error."})

            level = up.level

            if not level > 2:
                return JsonResponse({"code": 403, "status": False, "message": "you can't do its."})

            return function(request, *args, **kwargs)
        else:
            return JsonResponse({"code": 403, "status": False, "message": "login required."})

    return wrapper


def login_level4_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            u = User.objects.filter(username=request.user.username).first()

            if not u:
                return JsonResponse({"code": 403, "status": False, "message": "login required."})

            up = UserProfile.objects.filter(user_id=u.id).first()

            if not up:
                return JsonResponse({"code": 403, "status": False, "message": "something error."})

            level = up.level

            if not level > 3:
                return JsonResponse({"code": 403, "status": False, "message": "you can't do its."})

            return function(request, *args, **kwargs)
        else:
            return JsonResponse({"code": 403, "status": False, "message": "login required."})

    return wrapper