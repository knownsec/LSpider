# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class ScanTask(models.Model):
    task_name = models.CharField(max_length=50)
    target = models.TextField()
    target_type = models.CharField(max_length=30, default='link')
    task_tag = models.CharField(max_length=100)
    last_scan_time = models.DateTimeField()
    cookies = models.CharField(max_length=5000, default=None, null=True)
    is_active = models.BooleanField(default=False)
    is_emergency = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)


class BanList(models.Model):
    ban_name = models.CharField(max_length=50)
    ban_domain = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

