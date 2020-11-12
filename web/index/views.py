# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import time

from django.views import View
from django.shortcuts import render
from django.http import HttpResponse

from utils.wechathandler import ReMess


def index(req):
    return HttpResponse("Hello Lspider.")


class WebhookView(View):
    """
    授权模块
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.ReMess = ReMess

    def get(self, request):

        return HttpResponse("Hello Webhook.")

    def post(self, request):

        received_json_data = json.loads(request.body)['data']
        received_type = json.loads(request.body)['type']

        if received_json_data:

            if received_type != 'web_statistic':
                # new vul
                received_data = """
New vuls:\n
"""

                for key in received_json_data:

                    if key == 'plugin':
                        if received_json_data[key] in ['dirscan', 'brute_force']:
                            return HttpResponse("Success Webhook.")

                    if type(received_json_data[key]) is dict:

                        received_data += "{}:\n".format(key)
                        for kkey in received_json_data[key]:
                            if kkey not in ['detail', 'host', 'param', 'payload', 'port', 'stat', 'title',
                                            'type', 'url', 'plugin', 'target', 'type', 'vuln_class']:
                                continue

                            received_data += "  {}: {}\n".format(kkey, received_json_data[key][kkey])
                    else:
                        received_data += "{}: {}\n".format(key, received_json_data[key])

            else:
                if time.time() % 3600 < 5:
                    # 每小时提醒一次
                    received_data = """每时通报
扫描发现的url数量: {},
还没有扫描的url数量: {},
最近30s请求失败率: {}
""".format(received_json_data['num_found_urls'],
           int(received_json_data['num_found_urls']) - int(received_json_data['num_scanned_urls']),
           received_json_data['ratio_failed_http_requests'],
           )
                else:
                    return HttpResponse("Success Webhook.")

            self.ReMess.new_message(received_data)
            return HttpResponse("Success Webhook.")

        else:
            return HttpResponse("Hello Webhook.")
