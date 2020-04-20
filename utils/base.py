#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: base.py
@time: 2020/3/23 17:09
@desc:
'''

import random

from web.spider.models import ScanTable


def random_string(length=8):
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa = []
    for i in range(length):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def reg_trim(data):
    result = []

    for i in data:
        if type(i) is tuple:
            for j in i:
                if j:
                    result.append(j.strip())

            continue

        if i:
            result.append(i.strip())

    return result


def get_new_scan_id():
    s1 = ScanTable()
    s1.save()
    return s1.id


def get_now_scan_id():
    s1 = ScanTable.objects.last()
    return s1.id


def check_target(target_list):
    result = []

    if ',' in target_list:
        for target in target_list.split(','):
            if target:
                if target.strip().startswith("http://"):
                    result.append(target.strip())
                else:
                    result.append('http://'+target.strip())

    elif '\n' in target_list:
        for target in target_list.split('\n'):
            if target:
                if target.strip().startswith("http://"):
                    result.append(target.strip())
                else:
                    result.append('http://' + target.strip())

    else:
        if target_list.strip().startswith("http://"):
            result = [target_list]
        else:
            result = ['http://' + target_list]

    return result