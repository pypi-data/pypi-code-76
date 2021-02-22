# coding:utf-8
# author caturbhuja
# date   2020/8/31 5:10 下午 
# wechat chending2012 

# python pack
from functools import wraps
import time
import signal
import traceback


def cost_time(function):
    """
    warning_time: 操作耗时告警时间
    log: 日志 实例 接入
    request_id: 消息 id 用于追踪上下文日志
    """

    @wraps(function)
    def cost(*args, **kwargs):
        self = args[0]
        if not getattr(self, "config", None):
            self = args[0].client__
        config = self.config
        warning_time = config.get("action_warning_time", 5)
        debug = config.get("debug")
        log = self.log

        st = int(time.time())
        res = function(*args, **kwargs)
        ct = int(time.time()) - st
        if ct >= warning_time:
            message = "Db Client Function < {} > cost too long: {}s".format(function.__name__, ct)
            log.warning(message)
        if debug:
            message = "Function < {} > cost : {}s".format(function.__name__, ct)
            log.warning(message)

        return res

    return cost


def time_out(func):
    def handler(signum, frame):
        raise SelfTimeoutError("GG simada! run func timeout ")

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 额，判断self。因为分层问题，导致self 不同，暂时打个补丁。
        self = args[0]
        if not getattr(self, "config", None):
            self = args[0].client__
        config = self.config
        log = self.log,
        interval = config.get("action_time_out", 240)
        use_time_out_decorator = config.get("use_time_out_decorator")
        try:
            if use_time_out_decorator:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(interval)  # interval秒后向进程发送SIGALRM信号
            result = func(*args, **kwargs)
            if use_time_out_decorator:
                signal.alarm(0)  # 函数在规定时间执行完后关闭alarm闹钟
            return result
        except SelfTimeoutError as e:
            log.error(traceback.format_exc(3, e))

    return wrapper


# 自定义超时异常
class SelfTimeoutError(Exception):
    def __init__(self, msg):
        super(SelfTimeoutError, self).__init__()
        self.msg = msg


def try_and_reconnect(function):
    @wraps(function)
    def warp(*args, **kwargs):

        # 额，判断self。因为分层问题，导致self 不同，暂时打个补丁。
        self = args[0]
        if not getattr(self, "config", None):
            self = args[0].client__
        try:
            res = function(*args, **kwargs)

        except TypeError:
            self.log.error("type error, err_msg: {}".format(traceback.format_exc()))
            res = function(*args, **kwargs)

        except Exception as e:
            self.log.warning("warning, dbfactory will try fix it. warn_msg: {}\t{}".format(e, traceback.format_exc()))
            self._reconnect()
            res = function(*args, **kwargs)
        return res

    return warp


def kafka_type_check(init_type='consumer', real_type='consumer'):
    """检查kafka 实例化类型"""

    def wrap(function):
        """"""

        @wraps(function)
        def action(*args, **kwargs):
            if init_type != real_type:
                raise TypeError('init_type must be eq {}'.format(real_type))
            res = function(*args, **kwargs)
            return res

        return action

    return wrap


if __name__ == '__main__':
    # @cost_time(warning_time=1)
    # def test_ggg():
    #     time.sleep(1)
    # test_ggg()

    # ---------- time_out test --------
    import logging

    logging.basicConfig(level=logging.DEBUG)


    @time_out
    def task1():
        print("task1 start")
        time.sleep(3)
        print("task1 end")


    @time_out
    def task2():
        print("task2 start")
        time.sleep(1)
        print("task2 end")


    task1()
    task2()
