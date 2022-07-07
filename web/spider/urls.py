#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: urls.py
@time: 2022/5/17 14:47
@desc:

'''


from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from web.dashboard import views
from web.spider.webcontroller import profile, result, scantask


app_name = "spider"

urlpatterns = [
    path("", views.index),

    path("/profile", profile.ProfileView.as_view(), name="spider_profile"),

    path("/scantask", scantask.ScanTaskListView.as_view(), name="spider_scantask"),
    path("/scantask/<int:task_id>", scantask.ScanTaskDetailsView.as_view(), name="spider_scantask_detail"),

    path("/banlist", scantask.BanListView.as_view(), name="spider_banlist"),
    path("/banlist/<int:id>", scantask.BanListDetailsView.as_view(), name="spider_banlist_detail"),

    path("/loginpagelist", scantask.LoginPageListView.as_view(), name="spider_loginpagelist"),
    path("/loginpagelist/<int:id>", scantask.LoginPageDetailsView.as_view(), name="spider_loginpagelist_detail"),

    path("/accountdatalist", scantask.AccountDataListView.as_view(), name="spider_accountdatalist"),
    path("/accountdatalist/<int:id>", scantask.AccountDataDetailsView.as_view(), name="spider_accountdatalist_detail"),

    path("/urltablelist", scantask.UrlTableListView.as_view(), name="spider_urltablelist"),
    path("/subdomainlist", scantask.SubDomainListView.as_view(), name="spider_subdomainlist"),
]
