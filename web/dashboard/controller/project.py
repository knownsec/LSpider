#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: project.py
@time: 2022/4/19 14:55
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

from web.dashboard.models import Project, ProjectAssets, ProjectIps, ProjectVuls, ProjectSubdomain
from utils.base import check_gpc_undefined


class ProjectListView(View):
    """
        项目列表
    """

    @staticmethod
    def get(request):
        size = 10
        page = 1
        project_type = 0

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "type" in request.GET:
            project_type = int(request.GET['type'])

        if not project_type:
            ps = Project.objects.filter(is_active=1).values()[(page-1)*size:page*size]
        else:
            ps = Project.objects.filter(type=project_type, is_active=1).values()[(page - 1) * size:page * size]

        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})

    @staticmethod
    def post(request):
        params = json.loads(request.body)

        project_name = check_gpc_undefined(params, "project_name")
        source = check_gpc_undefined(params, "source")
        type = check_gpc_undefined(params, "type", 0)
        description = check_gpc_undefined(params, "description")

        p1 = Project.objects.filter(project_name=project_name).first()
        if p1:
            return JsonResponse({"code": 500, "status": False, "message": "Project {} is exists".format(project_name)})

        p = Project(project_name=project_name, source=source, type=type, description=description, is_active=True)
        p.save()

        return JsonResponse({"code": 200, "status": True, "message": "New Project successful"})


class ProjectListCountView(View):
    """
        项目列表
    """

    @staticmethod
    def get(request):
        count = Project.objects.all().count()
        return JsonResponse({"code": 200, "status": True, "total": count })


class ProjectDetailsView(View):
    """
        项目详情
    """

    @staticmethod
    def get(request, project_id):

        ps = Project.objects.filter(id=project_id, is_active=1).values()
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})

    @staticmethod
    def post(request, project_id):
        params = json.loads(request.body)

        ps = Project.objects.filter(id=project_id).first()

        project_name = check_gpc_undefined(params, "project_name")
        source = check_gpc_undefined(params, "source")
        type = check_gpc_undefined(params, "type", 0)
        description = check_gpc_undefined(params, "description")

        if ps:
            ps.project_name = project_name
            ps.source = source
            ps.type = type
            ps.description = description
            ps.save()
            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Project not found"})


class ProjectAssetsListView(View):
    """
        项目详情
    """

    @staticmethod
    def get(request, project_id):
        size = 10
        page = 1

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        ps = ProjectAssets.objects.filter(project_id=project_id, is_active=1).values()[(page - 1) * size:page * size]
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})

    @staticmethod
    def post(request, project_id):
        params = json.loads(request.body)

        if "name" not in params:
            return JsonResponse({"code": 404, "status": False, "message": "Required parameter not found"})

        p = Project.objects.filter(id=project_id).first()

        if not p:
            return JsonResponse({"code": 404, "status": False, "message": "Project not found"})

        name = check_gpc_undefined(params, "name")
        type = check_gpc_undefined(params, "type", 1)
        severity = check_gpc_undefined(params, "severity", 0)
        ext = check_gpc_undefined(params, "ext")
        is_active = check_gpc_undefined(params, "is_active", 1)

        pa = ProjectAssets.objects.filter(project_id=p.id, name=name).first()

        if pa:
            pa.type = type
            pa.severity = severity
            pa.ext = ext
            pa.is_active = is_active
            pa.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})

        pa2 = ProjectAssets(project_id=project_id, name=name, type=type, severity=severity, ext=ext, is_active=True)
        pa2.save()
        return JsonResponse({"code": 200, "status": True, "message": "New project asset successful"})


class ProjectAssetsListCountView(View):

    @staticmethod
    def get(request, project_id):
        count = ProjectAssets.objects.filter(project_id=project_id).count()
        return JsonResponse({"code": 200, "status": True, "total": count })


class ProjectAssetsDetailsView(View):
    """
        项目资产详情
    """

    @staticmethod
    def get(request, project_id, asset_id):

        ps = ProjectAssets.objects.filter(project_id=project_id, id=asset_id, is_active=1).values()
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})

    @staticmethod
    def post(request, project_id, asset_id):
        params = json.loads(request.body)
        pa = ProjectAssets.objects.filter(id=asset_id).first()

        name = check_gpc_undefined(params, "name")
        type = check_gpc_undefined(params, "type", 1)
        severity = check_gpc_undefined(params, "severity", 0)
        ext = check_gpc_undefined(params, "ext")
        is_active = check_gpc_undefined(params, "is_active", 1)

        if pa:
            pa.name = name
            pa.type = type
            pa.severity = severity
            pa.ext = ext
            pa.is_active = is_active
            pa.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "ProjectAssets not found"})


class ProjectIpsListView(View):
    """
        项目ip资产列表
    """

    @staticmethod
    def get(request, project_id):
        size = 10
        page = 1

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        ps = ProjectIps.objects.filter(project_id=project_id, is_active=1).values()[(page - 1) * size:page * size]
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})

    @staticmethod
    def post(request, project_id):
        params = json.loads(request.body)
        
        if "ips" not in params:
            return JsonResponse({"code": 404, "status": False, "message": "Required parameter not found"})

        p = Project.objects.filter(id=project_id).first()

        if not p:
            return JsonResponse({"code": 404, "status": False, "message": "Project not found"})

        ips = check_gpc_undefined(params, "ips")
        ext = check_gpc_undefined(params, "ext")
        is_active = check_gpc_undefined(params, "is_active", 1)

        pi = ProjectIps.objects.filter(project_id=p.id, ips=ips).first()

        if pi:
            pi.ext = ext
            pi.is_active = is_active
            pi.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})

        pi2 = ProjectIps(project_id=project_id, ips=ips, ext=ext, is_active=True)
        pi2.save()
        return JsonResponse({"code": 200, "status": True, "message": "New project ips successful"})


class ProjectIpsListCountView(View):

    @staticmethod
    def get(request, project_id):
        count = ProjectIps.objects.filter(project_id=project_id).count()
        return JsonResponse({"code": 200, "status": True, "total": count })


class ProjectIpsDetailsView(View):
    """
        项目资产详情
    """

    @staticmethod
    def get(request, project_id, ips_id):

        pi = ProjectIps.objects.filter(project_id=project_id, id=ips_id, is_active=1).values()
        count = len(pi)

        return JsonResponse({"code": 200, "status": True, "message": list(pi), "total": count})

    @staticmethod
    def post(request, project_id, ips_id):
        params = json.loads(request.body)
        pi = ProjectIps.objects.filter(id=ips_id).first()

        ips = check_gpc_undefined(params, "ips")
        ext = check_gpc_undefined(params, "ext")
        is_active = check_gpc_undefined(params, "is_active", 1)

        if pi:
            pi.ips = ips
            pi.ext = ext
            pi.is_active = is_active
            pi.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "ProjectAssets not found"})


class ProjectSubdomainListView(View):
    """
        项目子域名资产列表
    """

    @staticmethod
    def get(request, project_id):
        size = 10
        page = 1

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        ps = ProjectSubdomain.objects.filter(project_id=project_id, is_active=1).values()[(page - 1) * size:page * size]
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})

    @staticmethod
    def post(request, project_id):
        params = json.loads(request.body)

        if "subdomain" not in params:
            return JsonResponse({"code": 404, "status": False, "message": "Required parameter not found"})

        p = Project.objects.filter(id=project_id).first()

        if not p:
            return JsonResponse({"code": 404, "status": False, "message": "Project not found"})

        subdomain = check_gpc_undefined(params, "subdomain")
        title = check_gpc_undefined(params, "title")
        banner = check_gpc_undefined(params, "banner")
        weight = check_gpc_undefined(params, "weight", 0)
        is_active = check_gpc_undefined(params, "is_active", 1)

        ps = ProjectSubdomain.objects.filter(project_id=p.id, subdomain=subdomain).first()

        if ps:
            ps.title = title
            ps.banner = banner
            ps.weight = weight
            ps.is_active = is_active
            ps.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})

        ps2 = ProjectSubdomain(project_id=project_id, subdomain=subdomain, title=title,
                               banner=banner, weight=weight, is_active=True)
        ps2.save()
        return JsonResponse({"code": 200, "status": True, "message": "New Project Subdomain successful"})


class ProjectSubdomainListCountView(View):

    @staticmethod
    def get(request, project_id):
        count = ProjectSubdomain.objects.filter(project_id=project_id).count()
        return JsonResponse({"code": 200, "status": True, "total": count})


class ProjectSubdomainDetailsView(View):
    """
        项目子域名详情
    """

    @staticmethod
    def get(request, project_id, subdomain_id):

        ps = ProjectSubdomain.objects.filter(project_id=project_id, id=subdomain_id, is_active=1).values()
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})

    @staticmethod
    def post(request, project_id, subdomain_id):
        params = json.loads(request.body)
        ps = ProjectSubdomain.objects.filter(id=subdomain_id).first()

        subdomain = check_gpc_undefined(params, "subdomain")
        title = check_gpc_undefined(params, "title")
        banner = check_gpc_undefined(params, "banner")
        weight = check_gpc_undefined(params, "weight", 0)
        is_active = check_gpc_undefined(params, "is_active", 1)

        if ps:
            ps.subdomain = subdomain
            ps.title = title
            ps.banner = banner
            ps.weight = weight
            ps.is_active = is_active
            ps.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "ProjectSubdomain not found"})


class ProjectVulsListsView(View):
    """
        项目漏洞列表
    """

    @staticmethod
    def get(request, project_id):
        size = 10
        page = 1

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        ps = ProjectVuls.objects.filter(project_id=project_id, is_active=1).values()[(page - 1) * size:page * size]
        count = len(ps)

        ps_list = list(ps)

        for p in ps_list:
            p['details'] = ""

        return JsonResponse({"code": 200, "status": True, "message": ps_list, "total": count})

    @staticmethod
    def post(request, project_id):
        params = json.loads(request.body)

        if "name" not in params:
            return JsonResponse({"code": 404, "status": False, "message": "Required parameter not found"})

        p = Project.objects.filter(id=project_id).first()

        if not p:
            return JsonResponse({"code": 404, "status": False, "message": "Project not found"})

        name = check_gpc_undefined(params, "name")
        vultype_id = check_gpc_undefined(params, "vultype_id", 1)
        severity = check_gpc_undefined(params, "severity", 0)
        details = check_gpc_undefined(params, "details")

        pv = ProjectVuls(project_id=project_id, name=name, vultype_id=vultype_id, severity=severity, details=details, is_active=True)
        pv.save()
        return JsonResponse({"code": 200, "status": True, "message": "New project Vuls successful"})


class ProjectVulsListCountView(View):

    @staticmethod
    def get(request, project_id):
        count = ProjectVuls.objects.filter(project_id=project_id).count()
        return JsonResponse({"code": 200, "status": True, "total": count })


class ProjectVulsDetailsView(View):
    """
        项目漏洞详情
    """

    @staticmethod
    def get(request, project_id, vul_id):

        ps = ProjectVuls.objects.filter(project_id=project_id, id=vul_id, is_active=1).values()
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})

    @staticmethod
    def post(request, project_id, vul_id):
        params = json.loads(request.body)
        pv = ProjectVuls.objects.filter(id=vul_id).first()

        if not pv:
            return JsonResponse({"code": 404, "status": False, "message": "Project vuls not found"})

        name = check_gpc_undefined(params, "name")
        vultype_id = check_gpc_undefined(params, "vultype_id", 1)
        severity = check_gpc_undefined(params, "severity", 0)
        details = check_gpc_undefined(params, "details")

        pv.name = name
        pv.vultype_id = vultype_id
        pv.severity = severity
        pv.details = details
        pv.save()
        return JsonResponse({"code": 200, "status": True, "message": "update successful"})
