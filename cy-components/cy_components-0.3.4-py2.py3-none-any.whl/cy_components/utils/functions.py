import time


def retry_wrapper(func, params, sleep_seconds=5, retry_times=5):
    """
    需要不断重试的函数，可以使用本函数调用。
    func: 需要重试的函数名
    """
    for _ in range(retry_times):
        try:
            result = func(params=params)
            return result, params
        except Exception as e:
            print(func.__name__, '函数报错，报错内容：', str(e), '程序暂停，sleep时间：', sleep_seconds)
            time.sleep(sleep_seconds)
        else:
            pass
        finally:
            pass
    else:
        raise ValueError(func.__name__, '函数报错重试次数过多，程序退出。')
