import json

import orjson
import traceback

import flask
from gevent.pool import Pool
from datetime import datetime

from easi_py_common.core.redis import redis_store
from easi_py_common.sqs import constants
from easi_py_common.sqs.constants import ConsumerLogConstants
from easi_py_common.sqs.producer_session import ProducerSession
from easi_py_common.sqs.sqs import SQSClient

pool = Pool(128)

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class Producer:

    def __init__(self):
        self.started = False
        self.sqs_client = None
        self.app = None
        self.sign = ''

    def __format_msg(self, msg):
        if isinstance(msg, (str, int, bool, float)):
            return msg
        else:
            return orjson.dumps(msg)

    def start(self, app: flask.app.Flask, max_pool_connections=50, max_attempts=3):
        self.app = app

        if self.started:
            return

        self.started = True

        if self.app and self.app.config['ENV'] != 'prod':
            if 'sign' in app.config['PUBSUB']:
                self.sign = app.config['PUBSUB']['sign'] + '_'

        if 'region_name' in app.config['PUBSUB']:
            try:
                aws_access_key_id = app.config['AWS_ACCESS_KEY_ID']
                aws_secret_access_key = app.config['AWS_SECRET_ACCESS_KEY']
                self.sqs_client = SQSClient(app.config['PUBSUB']['region_name'],
                                            queue_name_prefix=self.sign,
                                            aws_access_key_id=aws_access_key_id,
                                            aws_secret_access_key=aws_secret_access_key,
                                            max_pool_connections=max_pool_connections,
                                            max_attempts=max_attempts)
            except Exception:
                if self.app:
                    self.app.logger.error(traceback.format_exc())

        self.init_batch_mode(self.app)

    def start_by_sqs_client(self, sqs_client):
        self.sqs_client = sqs_client

    def publish(self, address, msg, key='', group_id='', delay_seconds=0, sign=None):
        pool.spawn(self.send, address, msg, key=key, group_id=group_id, delay_seconds=delay_seconds, sign=sign)

    def send(self, address, msg, key='', group_id='', delay_seconds=0, sign=None):
        if self.sqs_client is None:
            if self.app:
                self.app.logger.error("sqs_client is None")
            return False
        if sign is None:
            address = self.sign + address
        else:
            address = sign + address
        return self.sqs_client.send_message(address, msg, key=key,
                                            group_id=group_id, delay_seconds=delay_seconds, cb=self.__log)

    def get_sqs_client(self):
        return self.sqs_client

    @property
    def session(self):
        # type: () -> ProducerSession
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'producer_session'):
                ctx.producer_session = ProducerSession(self.sqs_client, self.sign, app=self.app, cb=None)
            return ctx.producer_session

    def commit(self):
        self.session.commit()

    def init_batch_mode(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.batch_mode_teardown)
        else:
            app.teardown_request(self.batch_mode_teardown)

    def batch_mode_teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'producer_session'):
            ctx.producer_session.commit()
            # if exception is None:
            #     ctx.producer_session.commit()
            # else:
            #     ctx.producer_session.flush()
        return exception

    def __log(self, msg_id, msg_body):
        send_time = self.__format_timestamp(msg_body['t'])
        send_success_time = self.__format_timestamp(msg_body['s_t'])
        msg_body['send_time'] = send_time
        msg_body['send_success_time'] = send_success_time
        msg_body['msg_id'] = msg_id

        producer_log_len = redis_store.lpush(ConsumerLogConstants.PUB_LOG, json.dumps(msg_body))
        if producer_log_len >= ConsumerLogConstants.CONSUMER_LOG_MAX_SLEEP_ES_BULK_BUFFER_SIZE:
            redis_store.rpop(ConsumerLogConstants.PUB_LOG)
            return
        # 计算是否可以进行保存
        can_bulk_save = producer_log_len % ConsumerLogConstants.CONSUMER_LOG_ES_BULK_NUM == 0
        # 如果不可以保存，并且小于缓存最大值，则直接返回
        if not can_bulk_save and producer_log_len < ConsumerLogConstants.CONSUMER_LOG_ES_BULK_BUFFER_SIZE:
            return
        # 如果可以保存 或者 是200的倍数 则尝试进行保存
        if can_bulk_save or producer_log_len % 200 == 0 or producer_log_len >= ConsumerLogConstants.CONSUMER_LOG_MAX_SLEEP_ES_BULK_BUFFER_SIZE:
            self.publish(constants.PUB_LOG_BULK_SAVE, '')
            return

    def __format_timestamp(self, timestamp, is_millisecond=True):
        if is_millisecond:
            timestamp = round(timestamp / 1000.0, 2)
        date_array = datetime.utcfromtimestamp(timestamp)
        return date_array.strftime('%Y.%m.%d %H:%M:%S.%f')[:-3]


producer = Producer()
