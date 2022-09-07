# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


# Project
class Project(models.Model):
    project_name = models.CharField(max_length=50)
    source = models.CharField(max_length=1000)
    type = models.IntegerField(default=0)
    description = models.CharField(max_length=5000, default=None, null=True)
    create_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)


class ProjectAssets(models.Model):
    project_id = models.IntegerField()
    name = models.CharField(max_length=200)
    type = models.IntegerField(default=0)
    severity = models.IntegerField(default=0)
    ext = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=True)


class ProjectIps(models.Model):
    project_id = models.IntegerField()
    ips = models.CharField(max_length=200)
    ext = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=True)


# vuls
class ProjectVuls(models.Model):
    project_id = models.IntegerField()
    name = models.CharField(max_length=200)
    vultype_id = models.IntegerField()
    severity = models.IntegerField(default=0)
    details = models.TextField()
    is_active = models.BooleanField(default=True)


class VulType(models.Model):
    name = models.CharField(max_length=50)


class ProjectSubdomain(models.Model):
    project_id = models.IntegerField()
    subdomain = models.CharField(max_length=200)
    title = models.CharField(max_length=1000, null=True, default="")
    banner = models.CharField(max_length=1000, null=True, default="")
    weight = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)


# user profile
class UserProfile(models.Model):
    user_id = models.IntegerField()
    nickname = models.CharField(max_length=30)
    iphone = models.CharField(max_length=20)
    score = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
