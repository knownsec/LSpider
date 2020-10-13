#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: rabbitmqhandler.py.py
@time: 2020/4/8 14:57
@desc:
'''

import pika
import time
from pika.exceptions import ChannelClosed

from utils.log import logger
from LSpider.settings import RABBITMQ_IP, RABBITMQ_PORT, RABBITMQ_VHOST
from LSpider.settings import RABBITMQ_USERNAME, RABBITMQ_PASSWORD


class RabbitmqHandler:
    def __init__(self, id=1):
        self.ip = RABBITMQ_IP
        self.port = RABBITMQ_PORT
        self.user = RABBITMQ_USERNAME
        self.password = RABBITMQ_PASSWORD
        self.id = id

        self.link()

        # remessage init
        # self.remessage_channel = self.conn_broker.channel()
        # scan_target init
        self.scan_target_channel = self.conn_broker.channel()
        self.emergency_scan_target_channel = self.conn_broker.channel()

        logger.info("[Monitor][INIT] Rabbitmq init success...")

    def link(self):
        logger.info("[Monitor][INIT][Rabbitmq] New Rabbitmq link to {}".format(self.ip))

        self.credentials = pika.PlainCredentials(self.user, self.password)
        self.connection = pika.ConnectionParameters(host=self.ip, port=self.port, credentials=self.credentials,
                                                    virtual_host=RABBITMQ_VHOST, heartbeat=600, blocked_connection_timeout=300)
        self.conn_broker = pika.BlockingConnection(self.connection)

        return True

    def check_link_and_bind_scan(self):

        if self.conn_broker.is_closed:
            # reconnect
            self.connection = pika.ConnectionParameters(host=self.ip, port=self.port, credentials=self.credentials,
                                                        virtual_host=RABBITMQ_VHOST, heartbeat=600, blocked_connection_timeout=300)
            self.conn_broker = pika.BlockingConnection(self.connection)

        if self.scan_target_channel.is_closed:
            # reconnect
            self.scan_target_channel = self.conn_broker.channel()

        self.scan_target_channel.exchange_declare(exchange="scantarget", exchange_type="direct", passive=False, durable=True, auto_delete=False)
        # 防止queue不存在，新建queue
        queue = self.scan_target_channel.queue_declare(queue="scantarget", arguments={"x-max-priority": 10}, durable=True)
        # 绑定queue和exchange
        self.scan_target_channel.queue_bind(exchange="scantarget", queue="scantarget", routing_key="scantarget")

        return queue

    def check_emergency_link_and_bind_scan(self):

        if self.conn_broker.is_closed:
            # reconnect
            self.connection = pika.ConnectionParameters(host=self.ip, port=self.port, credentials=self.credentials,
                                                        virtual_host=RABBITMQ_VHOST, heartbeat=600, blocked_connection_timeout=300)
            self.conn_broker = pika.BlockingConnection(self.connection)

        if self.emergency_scan_target_channel.is_closed:
            # reconnect
            self.emergency_scan_target_channel = self.conn_broker.channel()

        self.emergency_scan_target_channel.exchange_declare(exchange="emergency_scantarget", exchange_type="direct", passive=False, durable=True, auto_delete=False)
        # 防止queue不存在，新建queue
        queue = self.emergency_scan_target_channel.queue_declare(queue="emergency_scantarget", arguments={"x-max-priority": 10}, durable=True)
        # 绑定queue和exchange
        self.emergency_scan_target_channel.queue_bind(exchange="emergency_scantarget", queue="emergency_scantarget", routing_key="emergency_scantarget")

        return queue

    def new_scan_target(self, msg, weight=0):
        self.check_link_and_bind_scan()

        logger.debug("[Scan][SEND] msg: {}".format(msg))

        msg_groups = pika.BasicProperties()
        msg_groups.content_type = "text/plain"
        msg_groups.priority = weight

        self.scan_target_channel.basic_publish(body=msg, exchange="scantarget", properties=msg_groups, routing_key="scantarget")

        return True

    def new_emergency_scan_target(self, msg):
        self.check_emergency_link_and_bind_scan()

        logger.debug("[Scan][emergency SEND] msg: {}".format(msg))

        msg_groups = pika.BasicProperties()
        msg_groups.content_type = "text/plain"

        self.emergency_scan_target_channel.basic_publish(body=msg, exchange="emergency_scantarget", properties=msg_groups, routing_key="emergency_scantarget")

        return True

    def get_scan_ready_count(self):
        try:
            queue = self.check_link_and_bind_scan()

            if self.conn_broker.is_closed or self.scan_target_channel.is_closed:
                return 0

            return queue.method.message_count

        except pika.exceptions.StreamLostError:
            logger.error("[Rabbitmq] Scan consum transport error.")
            return 0

    def get_emergency_scan_ready_count(self):
        try:
            queue = self.check_emergency_link_and_bind_scan()

            if self.conn_broker.is_closed or self.emergency_scan_target_channel.is_closed:
                return 0

            return queue.method.message_count

        except pika.exceptions.StreamLostError:
            logger.error("[Rabbitmq] Scan consum transport error.")
            return 0

    # def new_message(self, msg):
    #
    #     if self.conn_broker.is_closed:
    #         # reconnect
    #         self.connection = pika.ConnectionParameters(host=self.ip, port=self.port, credentials=self.credentials,
    #                                                     virtual_host=RABBITMQ_VHOST)
    #         self.conn_broker = pika.BlockingConnection(self.connection)
    #
    #     if self.remessage_channel.is_closed:
    #         # reconnect
    #         self.remessage_channel = self.conn_broker.channel()
    #
    #     self.remessage_channel.exchange_declare(exchange="remessage", exchange_type="direct", passive=False, durable=True, auto_delete=False)
    #     # 防止queue不存在，新建queue
    #     self.remessage_channel.queue_declare(queue="remessage", durable=True)
    #     # 绑定queue和exchange
    #     self.remessage_channel.queue_bind(exchange="remessage", queue="remessage", routing_key="remessage")
    #
    #     logger.debug("[Message][SEND] msg: {}".format(msg[:100]))
    #
    #     msg_groups = pika.BasicProperties()
    #     msg_groups.content_type = "text/plain"
    #
    #     self.remessage_channel.basic_publish(body=msg, exchange="remessage", properties=msg_groups, routing_key="remessage")

    def get_scan_target_channel(self):
        return self.scan_target_channel

    def test_print(self, channel, method, header, body):
        time.sleep(1)
        print(body)

        return

    def start_scan_target(self, fallback):

        # self.check_link_and_bind_scan()

        # 绑定队列和交换器
        self.scan_target_channel.queue_declare(queue="scantarget", arguments={"x-max-priority": 10}, durable=True)
        self.scan_target_channel.queue_bind(queue="scantarget", exchange="scantarget", routing_key="scantarget")
        self.scan_target_channel.basic_qos(prefetch_count=1)

        self.scan_target_channel.basic_consume("scantarget", fallback, consumer_tag="scantarget-consumer")

        #开始订阅
        try:
            self.scan_target_channel.start_consuming()
        except pika.exceptions.StreamLostError:
            logger.error("[Rabbitmq] Scan consum transport error.")
            return False
        except:
            raise

    def start_emergency_scan_target(self, fallback):

        # self.check_link_and_bind_scan()

        # 绑定队列和交换器
        self.emergency_scan_target_channel.queue_declare(queue="emergency_scantarget", arguments={"x-max-priority": 10}, durable=True)
        self.emergency_scan_target_channel.queue_bind(queue="emergency_scantarget", exchange="emergency_scantarget", routing_key="emergency_scantarget")
        self.emergency_scan_target_channel.basic_qos(prefetch_count=1)

        self.emergency_scan_target_channel.basic_consume("emergency_scantarget", fallback, consumer_tag="emergency_scantarget-consumer")

        #开始订阅
        try:
            self.emergency_scan_target_channel.start_consuming()
        except pika.exceptions.StreamLostError:
            logger.error("[Rabbitmq] Scan consum transport error.")
            return False
        except:
            raise
