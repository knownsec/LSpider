#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: bugcrowd.py
@time: 2020/8/4 14:35
@desc:

'''


import re
import time
import requests
import traceback
from core.chromeheadless import ChromeDriver
from utils.log import logger

from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


class BugcrowdSpider:
    """
    Bugcrowd spider main core
    """
    def __init__(self):

        self.url = 'https://bugcrowd.com/'
        self.chromeclass = ChromeDriver()

    def spider(self, appname):
        url = self.url + appname

        code, content, title = self.chromeclass.get_resp(url, isclick=False)
        time.sleep(5)

        result = self.html_parse()

        return result

    def html_parse(self):
        result_list = []

        td_list = self.chromeclass.driver.find_elements_by_xpath('//*[@id="user-guides__bounty-brief__targets-table"]/table/tbody/tr')

        for td in td_list:

            try:
                domain = td.find_element_by_tag_name("code").text.strip()
                type = td.find_element_by_tag_name("small").text.strip()

                if type == "Website Testing":
                    # replace {} () <>
                    domain = re.sub(r'[({<][^)}>]*[)}>]', '1', domain)

                    result_list.append(domain.replace("*.", ""))

            except:
                logger.warning("[Bugcrowd spider][parse] url data parse error. {}".format(traceback.format_exc()))
                continue

        return result_list


if __name__ == "__main__":

    h = BugcrowdSpider()
    h.spider('opera')
