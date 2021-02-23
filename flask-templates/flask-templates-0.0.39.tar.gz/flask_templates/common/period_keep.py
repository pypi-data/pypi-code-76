from datetime import datetime as dt, timedelta
from functools import wraps

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class Keeper:

    def fetch(self, key: str):
        pass

    def set_status(self, key: str, status: int):
        pass

    def keep(self, key: str, time_value: dt, value, status=0):
        pass


class DefaultKeeper(Keeper):
    collection = dict()

    def fetch(self, key: str):
        return self.collection.get(key)

    def set_status(self, key: str, status: int):
        value = self.collection.get(key)
        if value:
            value['status'] = status

    def keep(self, key: str, time_value: dt, value, status=0):
        self.collection[key] = {"key": key, "time_value": dt.strftime(time_value, DATETIME_FORMAT),
                                "value": str(value) if value else '',
                                'status': status}


def fresher(key, default_value=None, default_time_value=None, keeper: Keeper = DefaultKeeper, skip=0):
    def wrapper(func):
        @wraps(func)
        def wrappers(*args, **kwargs):
            # 当前时间
            now_dt = dt.now()
            skiper = skip
            # 获取原值
            key_info = keeper().fetch(key=key)
            if key_info:
                skiper = key_info['status']
                src_value = key_info['value']
                src_time_value = dt.strptime(key_info['time_value'], DATETIME_FORMAT)
            else:
                src_value = default_value if default_value else None
                src_time_value = default_time_value if default_time_value else now_dt - timedelta(days=30)
            if skiper:
                return func(*args, **kwargs)
            res = func(*args, _src_value=src_value, _src_time=src_time_value, _now_time=now_dt, **kwargs)
            keeper().keep(key, now_dt, res, status=0)
            return res

        return wrappers

    return wrapper


if __name__ == '__main__':
    import time


    @fresher("a")
    def test(_src_value=None, _src_time=None, _now_time=None):
        print(_src_time, _src_value, _now_time)


    while True:
        test()
        time.sleep(10)
