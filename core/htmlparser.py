#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: htmlparser.py
@time: 2020/3/16 16:04
@desc:
'''


import re
import traceback
from bs4 import BeautifulSoup

from utils.log import logger
from utils.base import reg_trim


def match_content(reg, content):
    """
    匹配内容中的信息
    """
    result = []

    if re.search(reg, content, re.I):
        p = re.compile(reg)
        match = p.findall(content)

        result = reg_trim(match)

    return result


def html_parser(content):
    """
    parser html
    """
    result_list = []

    try:
        soup = BeautifulSoup(content, "html.parser")

        script_tag_list = soup.find_all('script')

        for script_tag in script_tag_list:
            if script_tag.get('src'):
                result_list.append({"type": "link", "url": script_tag.get('src')})

        link_tag_list = soup.find_all('a')

        for link_tag in link_tag_list:
            if link_tag.get('href'):
                result_list.append({"type": "link", "url": link_tag.get('href')})

        form_tag_list = soup.find_all('form')

        for form_tag in form_tag_list:
            if form_tag.get('action'):
                result_list.append({"type": "link", "url": form_tag.get('action')})

        iframe_tag_list = soup.find_all('iframe')

        for iframe_tag in iframe_tag_list:
            if iframe_tag.get('src'):
                result_list.append({"type": "link", "url": iframe_tag.get('src')})

        # for script
        if not soup.body:
            line_break = content.count('\n')

            if line_break < 5:
                # 混淆代码不扫描
                return result_list

            # match
            for url in match_content('(((ht|f)tps?):\/\/)?[\w\-]+(\.[\w\-]+)+([\w\-.,@?^=%&:/~+#]*[\w\-@?^=%&/~+#])?', content):
                result_list.append({"type": "link", "url": url})

            for url in match_content('(?<=(\"|\'|\`))\/[a-zA-Z0-9_?&=\/\-\#\.]*(?=(\"|\'|\`))', content):
                result_list.append({"type": "link", "url": url})



    except:
        logger.warning('[AST] something error, {}'.format(traceback.format_exc()))

    return result_list
