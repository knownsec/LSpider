#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: Crt_Scan.py
@time: 2020/4/8 17:25
@desc:
'''


import requests
import traceback
from bs4 import BeautifulSoup

from utils.LReq import LReq
from utils.log import logger


class CrtScan:
    def __init__(self):
        self.req = LReq()

        self.url = "https://crt.sh/?q="

    def query(self, domain, deep=0):

        try:
            content = self.req.getResp(self.url+domain)

        except requests.exceptions.ReadTimeout:

            if deep > 2:
                logger.error("[Pre Scan][CrtScan] Crt.sh request error.")
                return False

            logger.warning("[Pre Scan][CrtScan] Crt.sh request error..test retrying.")
            return self.query(domain, deep+1)

        except:
            logger.warning("[Pre Scan][CrtScan] {} scan error.".format(domain))
            return False

        result = self.htmlparse(domain, content)

        return result

    def htmlparse(self, domain, content):
        result_list = [domain]

        try:
            soup = BeautifulSoup(content, "html.parser")

            tr_tag_list = soup.find_all('tr')

            for tr_tag in tr_tag_list:
                td_tag = tr_tag.find_all('td')

                if len(td_tag) > 4:
                    predomain_list = td_tag[4].contents

                    for predoamin in predomain_list:
                        if '.' in predoamin and '*' not in predoamin:
                            if predoamin not in result_list:
                                result_list.append(predoamin)

        except:
            traceback.print_exc()
            logger.warning("[Pre Scan][CrtScan] {} parse error.".format(domain))
            return False

        return result_list


if __name__ == "__main__":
    Req = CrtScan()

    Req.query("seebug.org")
