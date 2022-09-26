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

from web.dashboard.models import Project, ProjectAssets, ProjectIps, ProjectVuls, ProjectSubdomain, ProjectAnnouncement
from web.spider.models import SubDomainList, UrlTable
from utils.base import check_gpc_undefined

from web.index.middleware import login_level1_required, login_level2_required, login_level3_required, login_level4_required, login_required


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
    @login_level2_required
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
    @login_level3_required
    def get(request, project_id, asset_id):

        ps = ProjectAssets.objects.filter(project_id=project_id, id=asset_id, is_active=1).values()
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})

    @staticmethod
    @login_level3_required
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
    @login_level2_required
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


class ProjectIpsListPublishView(View):
    """
        批量插入ip
    """

    @staticmethod
    @login_level3_required
    def post(request, project_id):
        params = json.loads(request.body)

        if "ipslistdata" not in params:
            return JsonResponse({"code": 404, "status": False, "message": "Required parameter not found"})

        p = Project.objects.filter(id=project_id).first()

        if not p:
            return JsonResponse({"code": 404, "status": False, "message": "Project not found"})

        ipslistdata = check_gpc_undefined(params, "ipslistdata")
        is_define = check_gpc_undefined(params, "is_define", 0)
        ipsList = []

        ipsSpliteList = ipslistdata.splitlines()
        for ipss in ipsSpliteList:
            ipsList.append({"ipdata": ipss})

        ipsList_count = len(ipsList)

        if not is_define:
            return JsonResponse({"code": 200, "status": True, "message": list(ipsList), "total": ipsList_count})

        for ipData in ipsList:
            ipd = ProjectIps.objects.filter(project_id=project_id, ips=ipData['ipdata']).first()
            if ipd:
                continue

            ipd = ProjectIps(project_id=project_id, ips=ipData['ipdata'], is_active=1)
            ipd.save()
        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


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
    @login_level3_required
    def get(request, project_id, ips_id):

        pi = ProjectIps.objects.filter(project_id=project_id, id=ips_id, is_active=1).values()
        count = len(pi)

        return JsonResponse({"code": 200, "status": True, "message": list(pi), "total": count})

    @staticmethod
    @login_level3_required
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
        ps_list = []

        # 权重为0的子域名传染权重为2的子域名
        for p in ps:
            ps_list.append(p)
            if p['weight'] == 0:
                base_subdomain = p['subdomain']
                sds = SubDomainList.objects.filter(subdomain__endswith=base_subdomain)

                for sd in sds:
                    ps_list.append(
                        {
                            "project_id": p['id'],
                            "subdomain": sd.subdomain,
                            "banner": sd.banner,
                            "title": sd.title,
                            "weight": 2,
                            "is_active": 1,
                        }
                    )

        ps_list = sorted(ps_list, key=lambda e: e.__getitem__('weight'))[(page - 1) * size:page * size]
        count = len(ps_list)

        return JsonResponse({"code": 200, "status": True, "message": list(ps_list), "total": count})

    @staticmethod
    @login_level2_required
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


class ProjectSubdomainListPublishView(View):
    """
        批量插入子域名
    """

    @staticmethod
    @login_level3_required
    def post(request, project_id):
        params = json.loads(request.body)

        if "subdomainlistdata" not in params:
            return JsonResponse({"code": 404, "status": False, "message": "Required parameter not found"})

        p = Project.objects.filter(id=project_id).first()

        if not p:
            return JsonResponse({"code": 404, "status": False, "message": "Project not found"})

        subdomainlistdata = check_gpc_undefined(params, "subdomainlistdata")
        is_define = check_gpc_undefined(params, "is_define", 0)
        subdomainList = []

        subdomainSpliteList = subdomainlistdata.splitlines()
        subdomainList_count = len(subdomainSpliteList)

        for subs in subdomainSpliteList:
            subdomainList.append({"subdomaindata": subs})

        if not is_define:
            return JsonResponse({"code": 200, "status": True, "message": list(subdomainList), "total": subdomainList_count})

        for subdomain_data in subdomainList:
            subdata = subdomain_data['subdomaindata'].replace('*.', '').strip()

            if not subdata:
                continue

            sub = ProjectSubdomain.objects.filter(subdomain=subdata).first()
            if sub:
                continue

            ps = ProjectSubdomain(project_id=project_id, subdomain=subdata, is_active=1, weight=1)
            ps.save()

        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


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
    @login_level3_required
    def get(request, project_id, subdomain_id):

        ps = ProjectSubdomain.objects.filter(project_id=project_id, id=subdomain_id, is_active=1).values()
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})

    @staticmethod
    @login_level3_required
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
    @login_level2_required
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
    @login_level3_required
    def get(request, project_id, vul_id):

        ps = ProjectVuls.objects.filter(project_id=project_id, id=vul_id, is_active=1).values()
        count = len(ps)

        return JsonResponse({"code": 200, "status": True, "message": list(ps), "total": count})

    @staticmethod
    @login_level3_required
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


class ProjectAnnouncementsListsView(View):
    """
        公告列表
    """

    @staticmethod
    def get(request, project_id):
        size = 10
        page = 1

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        pas = ProjectAnnouncement.objects.filter(project_id=project_id, is_active=1).values()[(page - 1) * size:page * size]
        count = len(pas)

        pas_list = list(pas)

        for pa in pas_list:
            pa['content'] = ""

        return JsonResponse({"code": 200, "status": True, "message": pas_list, "total": count})

    @staticmethod
    @login_level2_required
    def post(request, project_id):
        params = json.loads(request.body)

        if "title" not in params:
            return JsonResponse({"code": 404, "status": False, "message": "Required parameter not found"})

        p = Project.objects.filter(id=project_id).first()

        if not p:
            return JsonResponse({"code": 404, "status": False, "message": "Project not found"})

        title = check_gpc_undefined(params, "title")
        author = check_gpc_undefined(params, "author")
        link = check_gpc_undefined(params, "link")
        content = check_gpc_undefined(params, "content")
        is_active = check_gpc_undefined(params, "is_active", 1)

        pa = ProjectAnnouncement(project_id=project_id, title=title, author=author, link=link, content=content, is_active=True)
        pa.save()
        return JsonResponse({"code": 200, "status": True, "message": "New project Announcements successful"})


class ProjectAnnouncementsListCountView(View):

    @staticmethod
    def get(request, project_id):
        count = ProjectAnnouncement.objects.filter(project_id=project_id).count()
        return JsonResponse({"code": 200, "status": True, "total": count })


class ProjectAnnouncementsDetailsView(View):
    """
        项目公告详情
    """

    @staticmethod
    def get(request, project_id, aid):

        pas = ProjectAnnouncement.objects.filter(project_id=project_id, id=aid, is_active=1).values()
        count = len(pas)

        return JsonResponse({"code": 200, "status": True, "message": list(pas), "total": count})

    @staticmethod
    @login_level3_required
    def post(request, project_id, aid):
        params = json.loads(request.body)
        pa = ProjectAnnouncement.objects.filter(id=aid).first()

        if not pa:
            return JsonResponse({"code": 404, "status": False, "message": "Project Announcements not found"})

        title = check_gpc_undefined(params, "title")
        author = check_gpc_undefined(params, "author")
        link = check_gpc_undefined(params, "link")
        content = check_gpc_undefined(params, "content")
        is_active = check_gpc_undefined(params, "is_active", 1)

        pa.title = title
        pa.author = author
        pa.link = link
        pa.content = content
        pa.is_active = is_active
        pa.save()
        return JsonResponse({"code": 200, "status": True, "message": "update successful"})


class ProjectUrlsListsView(View):
    """
        项目url列表
    """

    @staticmethod
    def get(request, project_id):
        size = 30
        page = 1
        urllist = []

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        sds = ProjectSubdomain.objects.filter(project_id=project_id, is_active=1)

        for sd in sds:
            urls = UrlTable.objects.filter(domain=sd.subdomain).values()

            for u in urls:
                urllist.append(u)

        urllist = urllist[(page - 1) * size:page * size]
        count = len(urllist)

        return JsonResponse({"code": 200, "status": True, "message": urllist, "total": count})


class ProjectUrlsListCountView(View):

    @staticmethod
    @login_level3_required
    def get(request, project_id):
        urllist = []

        sds = ProjectSubdomain.objects.filter(project_id=project_id, is_active=1)

        for sd in sds:
            urls = UrlTable.objects.filter(domain=sd.subdomain).values()

            for u in urls:
                urllist.append(u)

        count = len(urllist)
        return JsonResponse({"code": 200, "status": True, "total": count})