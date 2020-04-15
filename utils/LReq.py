#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: request.py
@time: 2020/3/13 15:48
@desc:
'''

import json
import requests
import random
import traceback
from urllib.parse import urlparse

from utils.log import logger
from core.chromeheadless import ChromeDriver


class LReq:
    """
    请求类
    """
    def __init__(self, is_chrome=False):

        self.ua = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/538",
                   "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"]

        self.s = requests.Session()

        if is_chrome:
            self.cs = ChromeDriver()

    @staticmethod
    def get_timeout():
        return random.randint(1, 5) * 0.5

    def get_header(self):
        return {
            "User-Agent": random.choice(self.ua)
        }

    def check_url(self, url):

        if url == "javascript:void(0);":
            return None

        if not urlparse(url).scheme:

            if not urlparse(url).netloc:
                return url

            if url.startswith('//'):
                return url

            url = 'http://' + url

        return url

    def getResp(self, url):
        url = self.check_url(url)
        logger.info("[LReq] New request {}".format(url))

        try:
            r = self.s.get(url, headers=self.get_header(), timeout=3)
        except:
            logger.warning('[LReq] something error, {}'.format(traceback.format_exc()))
            return False

        return r.content

    def getRespByChrome(self, url):
        url = self.check_url(url)
        logger.info("[LReq] New request {}".format(url))

        try:
            return self.cs.get_resp(url)

        except:
            logger.warning('[LReq] something error, {}'.format(traceback.format_exc()))
            return False

    def postResp(self, url, data):
        url = self.check_url(url)
        logger.info("[LReq] New request {}".format(url))

        try:
            r = self.s.post(url, data=data, headers=self.get_header(), timeout=3)
        except:
            logger.warning('[LReq] something error, {}'.format(traceback.format_exc()))
            return False

        return r.content

    def postJsonResp(self, url, data):
        url = self.check_url(url)
        logger.info("[LReq] New request {}".format(url))

        header = self.get_header()
        header['Content-Type'] = 'application/json'

        try:
            r = self.s.post(url, data=json.dumps(data), headers=header, timeout=3)
        except:
            logger.warning('[LReq] something error, {}'.format(traceback.format_exc()))
            return False

        return r.content

    def close_driver(self):
        self.cs.close_driver()


if __name__ == "__main__":
    Req = LReq(is_chrome=True)

    # print(Req.getResp("https://lorexxar.cn"))
    print(Req.getResp("https://cdn.jsdelivr.net/npm/jquery@3.3.1/dist/jquery.min.js"))
