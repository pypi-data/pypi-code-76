# -*- coding: utf-8 -*-
import json
import time
import traceback
from datetime import datetime
from inspect import isfunction

from flask import current_app

from easi_py_common.core.redis import redis_store, RedisLock
from easi_py_common.sqs import utils
from easi_py_common.sqs.constants import ConsumerLogConstants


def get_consumer_log_es_bulk_key():
    # 生成锁key
    consumer_log_es_bulk_key_template = 'delivery_consumer_log_es_bulk_key_{}'
    consumer_log_es_bulk_key_list = []
    for index in range(ConsumerLogConstants.CONSUMER_LOG_ES_BULK_THREAD_NUM):
        consumer_log_es_bulk_key_list.append(consumer_log_es_bulk_key_template.format(index))

    # 生成锁key 的值
    consumer_log_es_bulk_key_value_list = redis_store.mget(consumer_log_es_bulk_key_list)

    # 进行判断是否有可用锁
    consumer_log_es_bulk_key = None
    for index, value in enumerate(consumer_log_es_bulk_key_value_list):
        if not value:
            consumer_log_es_bulk_key = consumer_log_es_bulk_key_template.format(index)
            break

    if not consumer_log_es_bulk_key:
        return None

    # 进行锁20s
    redis_store.set(consumer_log_es_bulk_key, 1, ex=20)
    return consumer_log_es_bulk_key


class SqsPubLogDTO:
    msg_id = None
    address = None
    url = None
    k = None
    delay_seconds = None
    body = None
    group_id = None
    work_wait_time = None
    send_execute_time = None
    send_time = None
    send_success_time = None
    create_time = None


class SqsSubLogDTO:
    msg_id = None
    address = None
    url = None
    k = None
    body = None
    delay_seconds = None
    status = None
    receive_time = None
    receive_success_time = None
    message_wait_time = None
    work_wait_time = None
    execute_time = None
    create_time = None


def get_log_list(log_list_key, log_app_name):
    with RedisLock(lock_name="{}_consumer_log_es_{}_bulk_num_cat".format(log_app_name, log_list_key), timeout_ms=6000):
        # 获取现在的日志长度
        sub_log_len = redis_store.llen(log_list_key)
        if sub_log_len < ConsumerLogConstants.CONSUMER_LOG_ES_BULK_NUM:
            current_app.logger.info('数量不够')
            return [], ''

        # 获取锁key
        consumer_log_es_bulk_key = get_consumer_log_es_bulk_key()
        if not consumer_log_es_bulk_key:
            current_app.logger.info('没有获取到锁')
            return [], ''

        # 获取保存的日志列表
        pipe = redis_store.pipeline()
        for _ in range(ConsumerLogConstants.CONSUMER_LOG_ES_BULK_NUM):
            pipe.rpop(log_list_key)
        return pipe.execute(), consumer_log_es_bulk_key


class LogSqs:
    buffer_size = 1500
    buffer_cut = 500

    @staticmethod
    def save_producer_log(log_app_name, save_func):
        if not isfunction(save_func):
            return False
        # 获取需要保存的日志列表和锁key
        exec_results_start_time = time.time()
        results, consumer_log_es_bulk_key = get_log_list(ConsumerLogConstants.PUB_LOG.format(log_app_name),
                                                         log_app_name)
        exec_results_end_time = time.time()
        if exec_results_end_time - exec_results_start_time > 1:
            current_app.logger.error(
                'producer_log: get_results:{}'.format(exec_results_end_time - exec_results_start_time))

        if not results:
            return False

        batch_saves_start_time = time.time()
        try:
            batch_saves = []
            for m in results:
                if not m:
                    continue

                msg_ret = json.loads(m)
                msg_body = msg_ret['msg']
                if isinstance(msg_body, dict):
                    try:
                        msg_body = json.dumps(msg_body)
                        msg_body = msg_body[0:2000]
                    except Exception:
                        current_app.logger.error(
                            'producer_log resolve msg body error:{}, '
                            'body:{}'.format(traceback.format_exc(), msg_ret['body'])
                        )

                send_execute_time = -1
                try:
                    send_execute_time_seconds = (
                            datetime.strptime(msg_ret['send_success_time'], '%Y.%m.%d %H:%M:%S.%f')
                            - datetime.strptime(msg_ret['send_time'], '%Y.%m.%d %H:%M:%S.%f')
                    ).total_seconds()
                    send_execute_time = int(send_execute_time_seconds * 1000)
                except Exception:
                    pass

                work_wait_time = -1
                if 'work_wait_time' in msg_ret:
                    work_wait_time = msg_ret['work_wait_time']

                create_time = utils.format_timestamp(utils.get_utc_timestamp(), formats='%Y.%m.%d %H:%M:%S.%f')[:-3]
                send_time = msg_ret['send_time']
                send_success_time = msg_ret['send_success_time']

                pub_log = SqsPubLogDTO()
                pub_log.msg_id = msg_ret['msg_id']
                pub_log.address = msg_ret['address']
                pub_log.url = msg_ret['url']
                pub_log.k = msg_ret['key']
                pub_log.delay_seconds = msg_ret['delay_seconds']
                pub_log.body = msg_body
                pub_log.group_id = msg_ret['group_id']
                pub_log.work_wait_time = work_wait_time
                pub_log.send_execute_time = send_execute_time
                pub_log.send_time = send_time
                pub_log.send_success_time = send_success_time
                pub_log.create_time = create_time

                batch_saves.append(pub_log)

            if batch_saves:
                save_func(batch_saves)
        except Exception as e:
            current_app.logger.error('producer_log batch_saves error:{}'.format(traceback.format_exc()))
            raise e
        finally:
            # current_app.logger.error('producer_log batch_saves3')
            if consumer_log_es_bulk_key:
                redis_store.delete(consumer_log_es_bulk_key)

            batch_saves_total_time = time.time() - batch_saves_start_time
            if batch_saves_total_time > 15:
                current_app.logger.error('producer_log batch_saves_time:{}'.format(batch_saves_total_time))

        return True

    @staticmethod
    def save_consumer_log(log_app_name, save_func):
        if not isfunction(save_func):
            return False
        # 获取需要保存的日志列表和锁key
        exec_results_start_time = time.time()
        results, consumer_log_es_bulk_key = get_log_list(ConsumerLogConstants.SUB_LOG.format(log_app_name),
                                                         log_app_name)
        exec_results_end_time = time.time()
        if exec_results_end_time - exec_results_start_time > 1:
            current_app.logger.error(
                'consumer_log: get_results:{}'.format(exec_results_end_time - exec_results_start_time))

        if not results:
            return False

        batch_saves_start_time = time.time()
        try:
            batch_saves = []
            for m in results:
                if not m:
                    continue

                msg_ret = json.loads(m)
                msg_ret['create_time'] = utils.format_timestamp(utils.get_utc_timestamp(),
                                                                formats='%Y.%m.%d %H:%M:%S.%f')[:-3]

                if 'work_wait_time' not in msg_ret:
                    msg_ret['work_wait_time'] = -1
                if 'message_wait_time' not in msg_ret:
                    msg_ret['message_wait_time'] = -1
                if 'delay_seconds' not in msg_ret:
                    msg_ret['delay_seconds'] = -1

                msg_body = msg_ret['body']
                if utils.is_not_empty(msg_body):
                    try:
                        msg_body_json = json.loads(msg_body)
                        if isinstance(msg_body_json, dict) and 't' in msg_body_json:
                            msg_body_msg = msg_body_json['msg']
                            if utils.is_not_empty(msg_body_msg):
                                msg_body = json.dumps(msg_body_msg)
                            else:
                                msg_body = ''

                        msg_ret['body'] = msg_body[0:2000]
                    except Exception:
                        current_app.logger.error(
                            'consumer_log resolve msg body error:{}, '
                            'body:{}'.format(traceback.format_exc(), msg_ret['body'])
                        )
                msg_ret['execute_time'] = -1
                try:
                    if 'receive_success_time' in msg_ret and msg_ret['receive_success_time']:
                        execute_time = (
                                datetime.strptime(msg_ret['receive_success_time'], '%Y.%m.%d %H:%M:%S.%f')
                                - datetime.strptime(msg_ret['receive_time'], '%Y.%m.%d %H:%M:%S.%f')
                        ).total_seconds()
                        msg_ret['execute_time'] = int(execute_time * 1000)
                    else:
                        msg_ret['receive_success_time'] = msg_ret['receive_time']
                except Exception:
                    pass

                sub_log = SqsSubLogDTO()
                sub_log.msg_id = msg_ret['msg_id']
                sub_log.address = msg_ret['address']
                sub_log.url = msg_ret['url']
                sub_log.k = msg_ret['key']
                sub_log.body = msg_ret['body']
                sub_log.delay_seconds = msg_ret['delay_seconds']
                sub_log.status = msg_ret['status']
                sub_log.receive_time = msg_ret['receive_time']
                sub_log.receive_success_time = msg_ret['receive_success_time']
                sub_log.message_wait_time = msg_ret['message_wait_time']
                sub_log.work_wait_time = msg_ret['work_wait_time']
                sub_log.execute_time = msg_ret['execute_time']
                sub_log.create_time = msg_ret['create_time']

                batch_saves.append(sub_log)

            if batch_saves:
                save_func(batch_saves)

        except Exception as e:
            current_app.logger.error('consumer_log batch_saves error:{}'.format(traceback.format_exc()))
            raise e
        finally:
            # current_app.logger.error('consumer_log batch_saves3')
            if consumer_log_es_bulk_key:
                redis_store.delete(consumer_log_es_bulk_key)

            batch_saves_total_time = time.time() - batch_saves_start_time
            if batch_saves_total_time > 15:
                current_app.logger.error('consumer_log batch_saves_time:{}'.format(batch_saves_total_time))

        return True
