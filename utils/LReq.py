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
import time
import requests
import random
import traceback
import socket
import urllib3
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

    def get_header(self, url="", cookies=""):
        return {
            "User-Agent": random.choice(self.ua),
            "Referer": url,
            "Cookie": cookies
        }

    def check_url(self, url):

        if url == "javascript:void(0);":
            return None

        if not urlparse(url).scheme:

            if url.startswith('//'):
                url = 'http:' + url
                return url

            if url.startswith('/') or url.startswith('.'):
                return url

            if not urlparse(url).netloc:
                return url

            url = 'http://' + url

        return url

    def get(self, url, type='Resp', times=0, *args):

        try:
            method = getattr(self, 'get'+type)
            return method(url, args)

        except requests.exceptions.ReadTimeout:
            logger.warning("[LReq] Request {} timeout...".format(url))
            if times > 0:
                return False
            logger.warning("[LReq] Retry Request {} once...".format(url))
            return self.get(url, type, 1, *args)

        except socket.timeout:
            logger.warning("[LReq] Request {} timeout...".format(url))
            if times > 0:
                return False
            logger.warning("[LReq] Retry Request {} once...".format(url))
            return self.get(url, type, 1, *args)

        except urllib3.exceptions.NewConnectionError:
            logger.warning("[LReq] Request {} error...".format(url))
            if times > 0:
                return False
            logger.warning("[LReq] Retry Request {} once...".format(url))
            return self.get(url, type, 1, *args)

        except requests.exceptions.ConnectionError:
            logger.warning("[LReq] Request {} error...".format(url))
            if times > 0:
                return False
            logger.warning("[LReq] Retry Request {} once...".format(url))
            return self.get(url, type, 1, *args)

        except urllib3.exceptions.MaxRetryError:
            logger.warning("[LReq] Request {} too more. have a wait...".format(url))
            if times > 0:
                return False

            time.sleep(3)
            logger.warning("[LReq] Retry Request {} once...".format(url))
            return self.get(url, type, 1, *args)

        except:
            logger.warning('[LReq] something error, {}'.format(traceback.format_exc()))
            return False

    def post(self, url, type='Resp', times=0, *args):

        try:
            method = getattr(self, 'post'+type)
            return method(url, args)

        except requests.exceptions.ReadTimeout:
            logger.warning("[LReq] Request {} timeout...".format(url))
            if times > 0:
                return False
            logger.warning("[LReq] Retry Request {} once...".format(url))
            return self.post(url, type, 1, *args)

        except socket.timeout:
            logger.warning("[LReq] Request {} timeout...".format(url))
            if times > 0:
                return False
            logger.warning("[LReq] Retry Request {} once...".format(url))
            return self.post(url, type, 1, *args)

        except urllib3.exceptions.NewConnectionError:
            logger.warning("[LReq] Request {} error...".format(url))
            if times > 0:
                return False
            logger.warning("[LReq] Retry Request {} once...".format(url))
            return self.post(url, type, 1, *args)

        except requests.exceptions.ConnectionError:
            logger.warning("[LReq] Request {} error...".format(url))
            if times > 0:
                return False
            logger.warning("[LReq] Retry Request {} once...".format(url))
            return self.post(url, type, 1, *args)

        except urllib3.exceptions.MaxRetryError:
            logger.warning("[LReq] Request {} too more. have a wait...".format(url))
            if times > 0:
                return False

            time.sleep(3)
            logger.warning("[LReq] Retry Request {} once...".format(url))
            return self.get(url, type, 1, *args)

        except:
            logger.warning('[LReq] something error, {}'.format(traceback.format_exc()))
            return False

    def getResp(self, url, cookies):
        url = self.check_url(url)
        logger.info("[LReq] New request {}".format(url))
        cookies = cookies[0] if cookies else ""

        r = self.s.get(url, headers=self.get_header(url, cookies), timeout=3)

        return r.content

    def getRespByChrome(self, url, cookies):
        url = self.check_url(url)
        logger.info("[LReq] New request {}".format(url))
        cookies = cookies[0] if cookies else ""

        return self.cs.get_resp(url, cookies)

    def postResp(self, url, data, cookies):
        url = self.check_url(url)
        logger.info("[LReq] New request {}".format(url))
        cookies = cookies[0] if cookies else ""

        r = self.s.post(url, data=data, headers=self.get_header(url, cookies), timeout=3)

        return r.content

    def postJsonResp(self, url, data, cookies):
        url = self.check_url(url)
        logger.info("[LReq] New request {}".format(url))
        cookies = cookies[0] if cookies else ""

        header = self.get_header(url, cookies)
        header['Content-Type'] = 'application/json'

        r = self.s.post(url, data=json.dumps(data), headers=header, timeout=3)

        return r.content

    def close_driver(self):
        self.cs.close_driver()


if __name__ == "__main__":
    Req = LReq(is_chrome=True)

    # print(Req.getResp("https://lorexxar.cn"))
    print(Req.getResp("https://cdn.jsdelivr.net/npm/jquery@3.3.1/dist/jquery.min.js"))
