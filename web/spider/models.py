# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class SubDomainList(models.Model):
    subdomain = models.CharField(max_length=200)
    title = models.CharField(max_length=1000, null=True, default="")
    banner = models.CharField(max_length=1000, null=True, default="")
    lastscan = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
    is_emergency = models.BooleanField(default=False)


URL_TYPE = {
    0: "link",
    1: "js",
}


class UrlTable(models.Model):
    domain = models.CharField(max_length=50)
    type = models.CharField(max_length=10, default='link')
    url = models.CharField(max_length=2000)
    scanid = models.IntegerField(default=0)


class ScanTable(models.Model):
    scantime = models.DateTimeField(auto_now=True)
