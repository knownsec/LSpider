# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


# Project
class ScaVuls(models.Model):
    name = models.CharField(max_length=50)
    vultype_id = models.IntegerField()
    severity = models.IntegerField(default=0)
    link = models.CharField(max_length=200, null=True)
    details = models.CharField(max_length=5000, default=None, null=True)
    affected_version = models.CharField(max_length=500, null=True)
    create_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
