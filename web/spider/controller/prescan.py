#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: prescan.py
@time: 2020/3/12 16:30
@desc:
'''


from utils.log import logger
from web.spider.models import SubDomainList


class PrescanCore:
    """
    预扫描核心
    """
    def __init__(self):
        self.plugin_list = ['CrtScan']
        self.pluginObj_list = []

        self.result_list = []

        self.init_import()

    def init_import(self):

        for plugin_name in self.plugin_list:

            pluginClass = __import__("web.spider.controller.plugins." + plugin_name)
            tmpMod = getattr(pluginClass, "spider")
            tmpMod = getattr(tmpMod, "controller")
            tmpMod = getattr(tmpMod, "plugins")
            tmpMod = getattr(tmpMod, plugin_name)
            tmpClass = getattr(tmpMod, plugin_name)
            pluginObj = tmpClass()

            self.pluginObj_list.append(pluginObj)

    def start(self, domain):
        for pluginObj in self.pluginObj_list:

            self.result_list.extend(pluginObj.query(domain))

            # 去重
            self.result_list = list(set(self.result_list))

            # save to database
            for subdomain in self.result_list:

                # check exist
                s = SubDomainList.objects.filter(subdomain=subdomain)
                if not s:
                    continue

                s1 = SubDomainList(subdomain=subdomain, lastscan='1970-01-01 01:01:01')
                s1.save()

        logger.info("[Pre Scan] domain {} find pre-domain {}".format(domain, self.result_list))
        return self.result_list
