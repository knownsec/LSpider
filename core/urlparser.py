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
from urllib.parse import urlparse, parse_qs, urljoin

from web.spider.models import SubDomainList, UrlTable
from web.index.models import BanList

from utils.log import logger
from utils.base import get_now_scan_id


def checkbanlist(domain):
    banlist = BanList.objects.filter(is_active=True)

    for banword in banlist:
        if banword.ban_domain in domain:
            return True

    return False


def url_parser(domain, target_list, deep=0, backend_cookies = ""):
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

            if temp_result.netloc:
                request_url = temp_result.geturl()

            else:
                request_url = urljoin(domain, temp_result.path)

            result_list.append({'url': request_url.strip(), 'type': 'link', 'cookies': backend_cookies, 'deep': deep + 1})

            if temp_result.netloc == "":
                target_domain = origin_domain
            else:
                target_domain = temp_result.netloc

            # save data
            # check exist
            url = UrlTable.objects.filter(domain=target_domain, url=request_url)
            if url:
                continue

            u1 = UrlTable(domain=target_domain, type='link', url=request_url, scanid=get_now_scan_id())
            u1.save()

    return result_list


def url_filter(target_list):
    """
    url 去重
    """
    result_list = []

    for domain in target_list:
        temp_list = {}
        domain_list = target_list[domain]

        # 读数据库数据做聚合分析
        database_urllist = UrlTable.objects.filter(domain=domain)

        for url in database_urllist:
            domain_list.append(urlparse(url.url))

        for target in domain_list:

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
                if check_same(flag, temp_list[flag], target):
                    # 直接存入url
                    temp_list[flag].append(target)

        # merge result
        for flag in temp_list:
            result_list.extend(temp_list[flag])

    return result_list


def check_same(flag, origin_target_list, new_target):
    """
    检查相似性

    需要和原本列表中的所有url都不相似
    """

    check_flag = True
    BANWORD_LAST_LIST = ['.htm', '.png', '.jpg', '.mp']

    for origin_target in origin_target_list:

        i = 0
        diff = 0

        # false 是相似 true 是不想似
        check_flag_one = False
        is_diff_last = False
        is_has_banword = False

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
                        # 如果不同的只有最后一部分，那么这个路径下上限100条路由
                        if len(origin_target_list) > 100:
                            check_flag_one = False
                        else:
                            check_flag_one = True

                        # 如果存在特殊字符，那么不计入
                        for banword in BANWORD_LAST_LIST:
                            if banword in origin_path[-1]:
                                check_flag_one = False
                                is_has_banword = True
                                break

                    # 如果不同的不是最后一部分，那么必须要更多不同才行
                    diff += 1

                    if diff > 1:
                        check_flag_one = True

            i += 1

        # 如果最后一部分相同且不存在特殊字符
        if new_target_path[-1] == origin_path[-1] and not check_flag_one and not is_has_banword:
            is_diff_last = True

        # 参数重复判定
        if not check_flag_one and is_diff_last:
            # 如果path判定相似，那么会进入参数重复判定
            origin_query = parse_qs(origin_target.query)
            new_target_query = parse_qs(new_target.query)

            if not origin_query and not new_target_query:
                check_flag_one = False

            if (not origin_query and new_target_query) or (origin_query and not new_target_query):
                # 如果一个有参数一个无参数那么不想似
                check_flag_one = True

            for key in origin_query:
                if key not in new_target_query:
                    # 如果参数不相同，那么不想似
                    check_flag_one = True

        check_flag = check_flag & check_flag_one

    # 返回True时，链接与任意链接不想似
    return check_flag
