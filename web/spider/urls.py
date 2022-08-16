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

    path("profile", profile.ProfileView.as_view(), name="spider_profile"),

    path("scantask", csrf_exempt(scantask.ScanTaskListView.as_view()), name="spider_scantask"),
    path("scantask/count", csrf_exempt(scantask.ScanTaskListCountView.as_view()), name="spider_scantask_count"),
    path("scantask/<int:task_id>", csrf_exempt(scantask.ScanTaskDetailsView.as_view()), name="spider_scantask_detail"),

    path("banlist", csrf_exempt(scantask.BanListView.as_view()), name="spider_banlist"),
    path("banlist/count", csrf_exempt(scantask.BanListCountView.as_view()), name="spider_banlist_count"),
    path("banlist/<int:id>", csrf_exempt(scantask.BanListDetailsView.as_view()), name="spider_banlist_detail"),

    path("loginpagelist", csrf_exempt(scantask.LoginPageListView.as_view()), name="spider_loginpagelist"),
    path("loginpagelist/count", csrf_exempt(scantask.LoginPageListCountView.as_view()), name="spider_loginpagelist_count"),
    path("loginpagelist/<int:id>", csrf_exempt(scantask.LoginPageDetailsView.as_view()), name="spider_loginpagelist_detail"),

    path("accountdatalist", csrf_exempt(scantask.AccountDataListView.as_view()), name="spider_accountdatalist"),
    path("accountdatalist/count", csrf_exempt(scantask.AccountDataListCountView.as_view()), name="spider_accountdatalist_count"),
    path("accountdatalist/<int:id>", csrf_exempt(scantask.AccountDataDetailsView.as_view()), name="spider_accountdatalist_detail"),

    path("urltablelist", csrf_exempt(scantask.UrlTableListView.as_view()), name="spider_urltablelist"),
    path("urltablelist/count", csrf_exempt(scantask.UrlTableListCountView.as_view()), name="spider_urltablelist_count"),
    path("urltablelist/<int:id>", csrf_exempt(scantask.UrlTableDetailsView.as_view()), name="spider_urltablelist_detail"),

    path("subdomainlist", csrf_exempt(scantask.SubDomainListView.as_view()), name="spider_subdomainlist"),
    path("subdomainlist/count", csrf_exempt(scantask.SubDomainListCountView.as_view()), name="spider_subdomainlist_count"),
    path("subdomainlist/<int:id>", csrf_exempt(scantask.SubDomainDetailsView.as_view()), name="spider_subdomainlist_detail"),
]
