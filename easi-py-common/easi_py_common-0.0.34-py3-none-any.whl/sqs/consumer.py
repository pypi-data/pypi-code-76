import math
import os
import random
import signal
import sys
import time
from multiprocessing import cpu_count, Process

import gevent
import orjson
from gevent.pool import Pool

from easi_py_common.core.redis import redis_store
from easi_py_common.sqs import utils, constants
from easi_py_common.sqs.constants import ConsumerLogConstants
from easi_py_common.sqs.producer import producer

MAX_DELAY_SECONDS = 900

consumer_handlers = {}


def subscribe(address, call, **parms):
    work_number = parms.get("work_number", 8)
    msg_lifetime = parms.get("msg_lifetime", 86400 * 3)
    visibility_timeout_seconds = parms.get("visibility_timeout_seconds", 300)
    if work_number > 1024:
        work_number = 1024
    # if work_number <= 0:
    #     work_number = 1
    # if work_number > 32:
    #     work_number = 32

    if msg_lifetime > 86400 * 3:
        msg_lifetime = 86400 * 3

    if msg_lifetime < 1:
        msg_lifetime = 1

    msg_lifetime = int(msg_lifetime * 1000)

    consumer_handlers[address] = dict(
        call=call,
        pool_worker=Pool(work_number),
        msg_lifetime=msg_lifetime,
        visibility_timeout=visibility_timeout_seconds,
    )


class ConsumerStart:
    def __init__(self):
        self.handlers = {}
        self.sign = ""
        self.tasks = []
        self.sqs_client_wrapper = None
        self.is_run = True

    def start(self, app, handlers, db_pool_size, db_pool_size_every, db_pool_timeout):
        self.handlers = handlers
        self.app = app
        queue_len = len(handlers)

        if db_pool_size is None:
            if not db_pool_size_every:
                db_pool_size_every = 2
            db_pool_size = queue_len * db_pool_size_every

        if not db_pool_timeout:
            db_pool_timeout = 15

        app.config.update(SQLALCHEMY_POOL_SIZE=db_pool_size)
        app.config.update(SQLALCHEMY_MAX_OVERFLOW=db_pool_size)
        app.config.update(SQLALCHEMY_POOL_TIMEOUT=db_pool_timeout)

        conf = app.config["PUBSUB"]
        sign = ""
        if app and app.config["ENV"] != "prod":
            if "sign" in conf:
                sign = conf["sign"] + "_"
        if not sign:
            raise Exception("sign is require")
        app.logger.info(
            "PID:{}, QUEUE_LEN:{}, SQLALCHEMY_POOL_SIZE:{}, SIGN:{}, QUEUE:{}".format(
                os.getpid(), queue_len, db_pool_size, sign, [k for k in handlers]
            )
        )
        self.sqs_client_wrapper = producer.get_sqs_client()
        tasks = []
        for address, parms in self.handlers.items():
            tasks.append(gevent.spawn(self.do, sign + address, parms))
        self.tasks = tasks

        gevent.signal_handler(signal.SIGTERM, self.stop)
        gevent.joinall(tasks)
        self.app.logger.info("PID:{}, exit".format(os.getpid()))

    def install_subscribe(self):
        self.handlers = consumer_handlers.copy()

    def do(self, address, parms):
        client = self.sqs_client_wrapper.get_sqs_client()

        qurl = self.sqs_client_wrapper.get_queue_url(address)

        call = parms.get("call")
        pool_worker = parms.get("pool_worker")
        visibility_timeout = parms.get("visibility_timeout")
        msg_lifetime = parms.get("msg_lifetime")

        self.update_visibility_timeout(qurl, visibility_timeout)

        # self.app.logger.info("PID:{}, {}, run...".format(os.getpid(), address))
        while self.is_run:
            response = None
            try:
                response = client.receive_message(
                    QueueUrl=qurl, MaxNumberOfMessages=10, WaitTimeSeconds=15
                )
            except Exception as e:
                self.app.logger.exception("%s" % e)

            if response is None:
                continue

            if "Messages" not in response:
                continue

            get_message_time = utils.get_utc_timestamp()
            messages = response["Messages"]
            for m in messages:
                pool_worker.spawn(
                    self.wrapper_call, m, call, client, qurl, address, msg_lifetime, get_message_time
                )
            time.sleep(float('%.3f' % random.uniform(0.001, 0.02)))

        pool_worker.join()

    def update_visibility_timeout(self, qurl, visibility_timeout):
        try:
            resp = self.sqs_client_wrapper.get_queue_attr(qurl, ["VisibilityTimeout"])
            if "Attributes" not in resp:
                return

            attr = resp["Attributes"]
            visibility_timeout_ret = attr["VisibilityTimeout"]
            if int(visibility_timeout_ret) != int(visibility_timeout):
                self.sqs_client_wrapper.set_queue_attributes(
                    qurl, {"VisibilityTimeout": str(visibility_timeout)}
                )
        except:
            pass

    def wrapper_call(self, message, call, client, qurl, address, msg_lifetime, get_message_time):
        with self.app.app_context():
            try:
                body = message["Body"]
                receipt_handle = message.get("ReceiptHandle", "")
                msg_body = body

                sub_log_ret = self.__init_sub_log(
                    message.get("MessageId", ""), address, qurl, body, get_message_time)
                try:
                    msg_body = orjson.loads(body)
                    key = ""
                    if "key" in msg_body:
                        key = msg_body["key"]
                        sub_log_ret["key"] = key

                    if "t" in msg_body:
                        t = int(msg_body["t"])

                        sub_log_ret["message_wait_time"] = int(get_message_time - t)

                        differ = utils.get_utc_timestamp() - t
                        if differ > msg_lifetime + 1000:
                            client.delete_message(
                                QueueUrl=qurl, ReceiptHandle=receipt_handle
                            )
                            return

                        if "delay_seconds" in msg_body:
                            delay_seconds = int(msg_body["delay_seconds"])
                            sub_log_ret['delay_seconds'] = delay_seconds
                            if delay_seconds > MAX_DELAY_SECONDS:
                                differ_second = int(differ / 1000)

                                surplus_delay_seconds = delay_seconds - differ_second
                                if surplus_delay_seconds > 0:
                                    address_ret = address
                                    if self.sign and self.sign in address:
                                        address_ret = address_ret.split(self.sign)[1]

                                    producer.publish(
                                        address_ret,
                                        msg_body["msg"],
                                        key=key,
                                        delay_seconds=surplus_delay_seconds,
                                    )

                                    client.delete_message(
                                        QueueUrl=qurl, ReceiptHandle=receipt_handle
                                    )
                                    return
                    msg_body = msg_body["msg"]
                except:
                    pass

                call(msg_body)
                client.delete_message(QueueUrl=qurl, ReceiptHandle=receipt_handle)

                sub_log_ret["status"] = "success"
                sub_log_ret["receive_success_time"] = utils.format_timestamp(utils.get_utc_timestamp(),
                                                                             formats='%Y.%m.%d %H:%M:%S.%f')[:-3]
            except Exception as e:
                sub_log_ret['status'] = 'error'
                sub_log_ret['receive_success_time'] = utils.format_timestamp(utils.get_utc_timestamp(),
                                                                             formats='%Y.%m.%d %H:%M:%S.%f')[:-3]
                raise e
            finally:
                self.__save_sub_log(sub_log_ret)

    def __init_sub_log(self, msg_id, address, qurl, body, get_message_time):
        work_message_time = utils.get_utc_timestamp()
        return {
            "msg_id": msg_id,
            "address": address,
            "url": qurl,
            "body": body,
            "key": "",
            "delay_seconds": 0,
            "status": "fail",
            "work_wait_time": int(work_message_time - get_message_time),
            "message_wait_time": -1,
            "receive_time": utils.format_timestamp(utils.get_utc_timestamp(), formats="%Y.%m.%d %H:%M:%S.%f")[:-3],
            "receive_success_time": "",
        }

    def __save_sub_log(self, sub_log_ret):
        try:
            sub_log_len = redis_store.lpush(ConsumerLogConstants.SUB_LOG, orjson.dumps(sub_log_ret))
            if sub_log_len >= ConsumerLogConstants.CONSUMER_LOG_MAX_SLEEP_ES_BULK_BUFFER_SIZE:
                redis_store.rpop(ConsumerLogConstants.SUB_LOG)
                return
            # 计算是否可以进行保存
            can_bulk_save = sub_log_len % ConsumerLogConstants.CONSUMER_LOG_ES_BULK_NUM == 0
            # 如果不可以保存，并且小于缓存最大值，则直接返回
            if not can_bulk_save and sub_log_len < ConsumerLogConstants.CONSUMER_LOG_ES_BULK_BUFFER_SIZE:
                return
            # 如果可以保存 或者 是200的倍数 则尝试进行保存
            if can_bulk_save or sub_log_len % 200 == 0 or sub_log_len >= ConsumerLogConstants.CONSUMER_LOG_MAX_SLEEP_ES_BULK_BUFFER_SIZE:
                producer.send(constants.SUB_LOG_BULK_SAVE, '')
        except Exception:
            pass

    def stop(self, sig, frame):
        self.is_run = False


class ConsumerRun:
    def __init__(self, app_cb):
        self.process_list = []
        self.app_cb = app_cb

    def run(self, cpu_count=cpu_count() * 2, db_pool_size=None, db_pool_size_every=2, db_pool_timeout=15):
        chandlers = consumer_handlers.copy()
        phandlers = self.split_handler_by_cpu(cpu_count, chandlers)

        for handler in phandlers:
            p = Process(target=self.start, args=(handler, db_pool_size, db_pool_size_every, db_pool_timeout))
            p.start()
            self.process_list.append(p)

        print(
            u"CPU核数:{0}, 队列数:{1}, 进程数:{2}, Main Pid:{3}".format(
                cpu_count, len(chandlers), len(self.process_list), os.getpid()
            )
        )

    def split_handler_by_cpu(self, cpu_number, handlers):
        phandlers = []
        spsize = len(handlers) / float(cpu_number)
        spsize = int(math.floor(spsize))

        if spsize < 1:
            spsize = 1

        temp = {}
        i = 0
        for k, v in handlers.items():
            temp[k] = v
            i += 1
            if i == spsize:
                if len(phandlers) >= cpu_number:
                    continue

                phandlers.append(temp)
                temp = {}
                i = 0

        j = 0
        for k, v in temp.items():
            handler_dict = phandlers[j]
            t = {}
            t[k] = v
            handler_dict.update(t)
            j += 1

        return phandlers

    def exit(self):
        print("grace exiting...")
        s = time.time()
        for p in self.process_list:
            cmd = "kill -{} {}".format(signal.SIGTERM, p.pid)
            os.system(cmd)

        for p in self.process_list:
            p.join()

        print("exit success:{}".format(time.time() - s))
        sys.exit(0)

    def start(self, handler, db_pool_size, db_pool_size_every, db_pool_timeout):
        ConsumerStart().start(self.app_cb(), handler, db_pool_size, db_pool_size_every, db_pool_timeout)
