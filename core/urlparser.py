#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: urlparser.py
@time: 2020/3/18 15:46
@desc:
'''

import re
from urllib.parse import urlparse

from web.spider.models import SubDomainList, UrlTable
from web.index.models import BanList

from utils.log import logger


def checkbanlist(domain):
    banlist = BanList.objects.filter(is_active=True)

    for banword in banlist:
        if banword.ban_domain in domain:
            return True

    return False


def url_parser(domain, target_list, deep=0):
    """
    通过分割url来给url分类，并试图去重
    """
    origin_domain = urlparse(domain).netloc
    pre_result_list = {}
    temp_result_list = []

    result_list = []

    for target in target_list:

        parse_result = urlparse(target['url'])

        if parse_result.netloc == "":
            target_domain = origin_domain
        else:
            target_domain = parse_result.netloc

        if parse_result.scheme == "javascript":
            continue

        # check domain
        if checkbanlist(parse_result.netloc):
            logger.warning("[Spider][UrlParser] Find Bad Word in domain {}".format(parse_result.netloc))
            continue

        if target_domain not in pre_result_list:
            pre_result_list[target_domain] = []

        pre_result_list[target_domain].append(parse_result)

    # 总结结果
    temp_result_list = url_filter(pre_result_list)

    for temp_result in temp_result_list:

        if temp_result.geturl():
            result_list.append({'url': temp_result.geturl(), 'type': 'link', 'deep': deep + 1})

            if temp_result.netloc == "":
                target_domain = origin_domain
            else:
                target_domain = temp_result.netloc

            # save data
            u1 = UrlTable(domain=target_domain, type='link', url=temp_result.geturl())
            u1.save()

    return result_list


def url_filter(target_list):
    """
    url 去重
    """
    result_list = []

    for domain in target_list:
        temp_list = {}

        for target in target_list[domain]:

            # 路径重复判定处理
            path_parsers = target.path.split('/')

            # 用一个特殊的思路来处理
            # 使用A来代表纯数字，B来代表字符串
            # 如果两个链接中只有A相同，那么则相似
            # 如果只有B相同，则认为不相似
            flag = ""

            for path_par in path_parsers:

                if re.search('^\d+$', path_par):
                    flag += 'A'

                else:
                    flag += 'B'

            if flag not in temp_list:
                temp_list[flag] = [target]

            else:
                if check_path_same(flag, temp_list[flag], target):
                    # 直接存入url
                    temp_list[flag].append(target)

        # merge result
        for flag in temp_list:
            result_list.extend(temp_list[flag])

    return result_list


def check_path_same(flag, origin_target_list, new_target):
    """
    检查相似性

    需要和原本列表中的所有url都不相似
    """

    check_flag = True
    BANWORD_LAST_LIST = ['.html', '.htm']

    for origin_target in origin_target_list:

        i = 0
        diff = 0
        check_flag_one = False

        origin_path = origin_target.path.split('/')
        new_target_path = new_target.path.split('/')

        for m in flag:
            if m == 'A':
                i += 1
                continue
            if m == 'B':

                # check B string
                if origin_path[i] != new_target_path[i]:
                    # 当不同的是最后一部分，那么直接判定为不想似
                    if origin_path[i] == origin_path[-1]:
                        check_flag_one = True

                        # 如果存在特殊字符，那么不计入
                        for banword in BANWORD_LAST_LIST:
                            if banword in origin_path[-1]:
                                check_flag_one = False
                                break

                    # 如果不同的不是最后一部分，那么必须要更多不同才行
                    diff += 1

                    if diff > 1:
                        check_flag_one = True

            i += 1

        check_flag = check_flag & check_flag_one

    # 返回True时，链接与任意链接不想似
    return check_flag
