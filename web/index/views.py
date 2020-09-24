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

        received_json_data = json.loads(request.body)

        if received_json_data:

            if "detail" in received_json_data:
                # new vul
                received_data = """
New vuls:\n
"""

                for key in received_json_data:

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
                if time.time() % 3600 < 2:
                    # 每小时提醒一次
                    received_data = """
每时通报\n
{}
""".format(received_json_data)
                else:
                    return HttpResponse("Success Webhook.")

            self.ReMess.new_message(received_data)
            return HttpResponse("Success Webhook.")


        else:
            return HttpResponse("Hello Webhook.")
