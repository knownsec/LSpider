#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: const.py
@time: 2022/4/27 16:45
@desc:

'''

PROJECT_TYPE_LIST = {
    0: "Unknown",
    1: "Src",
    2: "Hackerone",
    3: "BugCrowd",
    4: "Others",
}

PROJECT_ASSERTS_TYPE_LIST = {
    0: "Unknown",
    1: "Web 资产",
    2: "实物类资产",
}

PROJECT_ASSERTS_SEVERITYS = {
    0: "Unknown",
    1: "核心资产",
    2: "一般资产",
    3: "边缘资产",
    4: "非所属资产",
}

PROJECT_VULS_SEVERITY = {
    0: "Low",
    1: "Medium",
    2: "High",
    3: "Critical",
}

SCA_VULS_SEVERITY = {
    0: "Low",
    1: "Medium",
    2: "High",
    3: "Critical",
}

USER_LEVEL = {
    0: "会员",
    1: "一般会员",
    2: "核心会员",
}