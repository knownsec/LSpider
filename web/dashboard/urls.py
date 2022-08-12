#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: urls.py.py
@time: 2022/4/19 14:48
@desc:

'''

from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from web.dashboard import views
from web.dashboard.controller import project, options


app_name = "dashboard"

urlpatterns = [
    path("", views.index),

    # project
    path("project", csrf_exempt(project.ProjectListView.as_view()), name="project"),
    path("project/<int:project_id>", csrf_exempt(project.ProjectDetailsView.as_view()), name="project_detail"),

    path("project/<int:project_id>/assets", csrf_exempt(project.ProjectAssetsListView.as_view()), name="project_assets"),
    path("project/<int:project_id>/assets/<int:asset_id>", csrf_exempt(project.ProjectAssetsDetailsView.as_view()),
         name="project_asset_detail"),

    path("project/<int:project_id>/ips", csrf_exempt(project.ProjectIpsListView.as_view()), name="project_ips"),
    path("project/<int:project_id>/ips/<int:ips_id>", csrf_exempt(project.ProjectIpsDetailsView.as_view()), name="project_ip_detail"),

    path("project/<int:project_id>/vuls", csrf_exempt(project.ProjectVulsListsView.as_view()), name="project_vuls"),
    path("project/<int:project_id>/vuls/<int:vul_id>", csrf_exempt(project.ProjectVulsDetailsView.as_view()), name="project_vuls_details"),

    # options
    path("options/vultype", csrf_exempt(options.VulTypeListView.as_view()), name="vultype"),

    path("options/projectType", options.ProjectType, name="option_project_type"),
    path("options/projectAssertsType", options.ProjectAssertsType, name="option_project_asserts_type"),
    path("options/projectAssertsSeverity", options.ProjectAssertsSeverity, name="option_project_asserts_severity"),
    path("options/projectVulsSeverity", options.ProjectVulsSeverity, name="option_project_vuls_severity"),
    path("options/scaVulsSeverity", options.ScaVulsSeverity, name="option_sca_severity"),

]
