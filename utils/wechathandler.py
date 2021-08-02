#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: wechathandler.py
@time: 2020/9/24 15:27
@desc:

'''

from utils.log import logger
from wechatpy.enterprise import WeChatClient
from LSpider.settings import LOGHANDER_IS_OPEN_WEIXIN
from LSpider.settings import WECHAT_NOTICE, WECHAT_NOTICE_DEBUG
from LSpider.settings import WECHAT_ADMIN_LIST, WECHAT_USER_LIST


enterprise = WeChatClient(
    corp_id=WECHAT_NOTICE['corp_id'],
    secret=WECHAT_NOTICE['secret'],
)

enterprise_debug = WeChatClient(
    corp_id=WECHAT_NOTICE_DEBUG['corp_id'],
    secret=WECHAT_NOTICE_DEBUG['secret'],
)


def send_text(content):
    enterprise.message.send_text(
        agent_id=WECHAT_NOTICE['agent_id'],
        user_ids=WECHAT_USER_LIST,
        tag_ids='',
        content=content,
        # title="HaoTian 实时监控警报"
    )


def send_text_admin(content):
    enterprise_debug.message.send_text(
        agent_id=WECHAT_NOTICE_DEBUG['agent_id'],
        user_ids=WECHAT_ADMIN_LIST,
        tag_ids='',
        content=content,
        # title="HaoTian 实时监控警报"
    )


def send_text_card(title, description, url='#'):
    enterprise.message.send_text_card(
        agent_id=WECHAT_NOTICE['agent_id'],
        user_ids='',
        tag_ids='',
        title=title,
        description=description,
        url=url,
    )


class LogHandlerClass:
    def __init__(self, is_weixin):

        self.is_weixin = is_weixin

    def new_message(self, message, user=False):
        if self.is_weixin:
            if user:
                message = """
User {user} Attention, {message}
                """.format(user=user, message=message)

                send_text(message)

            else:
                send_text(message)

    def debug_message(self, message):
        if self.is_weixin:
            send_text_admin(message)


ReMess = LogHandlerClass(is_weixin=LOGHANDER_IS_OPEN_WEIXIN)
