# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class SubDomainList(models.Model):
    scanid = models.IntegerField()
    subdomain = models.CharField(max_length=50)


