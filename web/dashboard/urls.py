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
    path("project/count", csrf_exempt(project.ProjectListCountView.as_view()), name="project_count"),
    path("project/<int:project_id>", csrf_exempt(project.ProjectDetailsView.as_view()), name="project_detail"),

    path("project/<int:project_id>/assets", csrf_exempt(project.ProjectAssetsListView.as_view()), name="project_assets"),
    path("project/<int:project_id>/assets/count", csrf_exempt(project.ProjectAssetsListCountView.as_view()),
         name="project_assets_count"),
    path("project/<int:project_id>/assets/<int:asset_id>", csrf_exempt(project.ProjectAssetsDetailsView.as_view()),
         name="project_asset_detail"),

    path("project/<int:project_id>/ips", csrf_exempt(project.ProjectIpsListView.as_view()), name="project_ips"),
    path("project/<int:project_id>/ips/count", csrf_exempt(project.ProjectIpsListCountView.as_view()), name="project_ips_count"),
    path("project/<int:project_id>/ips/<int:ips_id>", csrf_exempt(project.ProjectIpsDetailsView.as_view()), name="project_ip_detail"),

    path("project/<int:project_id>/subdomain", csrf_exempt(project.ProjectSubdomainListView.as_view()), name="project_subdomain_vuls"),
    path("project/<int:project_id>/subdomain/count", csrf_exempt(project.ProjectSubdomainListCountView.as_view()),
         name="project_subdomain_count"),
    path("project/<int:project_id>/subdomain/<int:subdomain_id>", csrf_exempt(project.ProjectSubdomainDetailsView.as_view()),
         name="project_subdomain_details"),

    path("project/<int:project_id>/vuls", csrf_exempt(project.ProjectVulsListsView.as_view()), name="project_vuls"),
    path("project/<int:project_id>/vuls/count", csrf_exempt(project.ProjectVulsListCountView.as_view()), name="project_vuls_count"),
    path("project/<int:project_id>/vuls/<int:vul_id>", csrf_exempt(project.ProjectVulsDetailsView.as_view()), name="project_vuls_details"),

    path("project/<int:project_id>/urls", csrf_exempt(project.ProjectUrlsListsView.as_view()), name="project_urls"),
    path("project/<int:project_id>/urls/count", csrf_exempt(project.ProjectUrlsListCountView.as_view()),
         name="project_urls_count"),

    # options
    path("options/vultype", csrf_exempt(options.VulTypeListView.as_view()), name="vultype"),

    path("options/projectType", options.ProjectType, name="option_project_type"),
    path("options/projectAssertsType", options.ProjectAssertsType, name="option_project_asserts_type"),
    path("options/projectAssertsSeverity", options.ProjectAssertsSeverity, name="option_project_asserts_severity"),
    path("options/projectVulsSeverity", options.ProjectVulsSeverity, name="option_project_vuls_severity"),
    path("options/scaVulsSeverity", options.ScaVulsSeverity, name="option_sca_severity"),

]
