# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class SubDomainList(models.Model):
    scanid = models.IntegerField()
    subdomain = models.CharField(max_length=50)
    lastscan = models.DateTimeField()


URL_TYPE = {
    0: "link",
    1: "js",
}


class UrlTable(models.Model):
    domain = models.CharField(max_length=50)
    type = models.CharField(max_length=10, default='link')
    url = models.CharField(max_length=200)
