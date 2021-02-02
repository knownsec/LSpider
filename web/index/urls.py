#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: urls.py
@time: 2020/9/24 15:56
@desc:

'''


from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from web.index import views


app_name = "index"

urlpatterns = [
    path("", views.index),

    path("vuls/", views.VulFileListView.as_view(), name="vullist"),
    path("vuls/<str:filepath>", views.VulFileListView.as_view(), name="vulpath"),
    path("webhook", csrf_exempt(views.WebhookView.as_view()), name="webhook"),
]
