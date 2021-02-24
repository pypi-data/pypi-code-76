# coding:utf-8
# author caturbhuja
# date   2020/12/18 6:00 下午 
# wechat chending2012 
"""
支持选择 db，指定key，
选择 同步周期
"""
from DbFactory import DbFactory
from threading import Thread
from dlog import DLog
import time


class SyncHandler:
    """"""

    def __init__(
            self, outer_cache, monitor_db=None, monitor_keys=None, sync_period=180, log=None,
            db_type='redis', host='0.0.0.0', port='6379', password='f66sU9iP', db_name='0'
    ):
        self._outer_cache = outer_cache
        self._monitor_db = monitor_db or list()
        self._monitor_keys = monitor_keys or list()
        self._stop = False
        self.log = log or DLog().get_log
        self._sync_period = sync_period
        self._pipeline_count = 1000  # pipe 每次执行命令次数
        self.sync_lock = True
        # 这里需要强制指定use_redis_local_cache 为false
        self._redis_client = DbFactory(db_type=db_type, host=host, password=password, port=port,
                                       db_name=db_name, use_redis_local_cache=False, use_time_out_decorator=False)
        t = Thread(target=self._sync)
        t.start()

    def _sync(self):
        def action():
            part_keys = list()
            if self._monitor_keys:
                for each_match in self._monitor_keys:
                    cursor = 0
                    count = 10000
                    while 1:
                        res = self._redis_client.scan(cursor=cursor, match=each_match, count=count)
                        cursor = res[0]
                        part_keys.extend(res[1])
                        if cursor == 0:  # 游标再次回到初始位置
                            break
            else:
                cursor = 0
                count = 15
                while 1:
                    res = self._redis_client.scan(cursor=cursor, count=count)
                    cursor = res[0]
                    part_keys.extend(res[1])
                    if cursor == 0:  # 游标再次回到初始位置
                        break
            # print(part_keys)
            value_type_list = self._get_key_type(part_keys)
            # print(value_type_dict)
            # 获取key的值
            value_dict = self._get_value_by_key(value_type_list)
            self.all_value_dict.update(value_dict)

        while not self._stop:
            self.sync_lock = True
            self.all_value_dict = dict()

            if self._monitor_db:    # todo 这块功能暂时有问题。因为不同数据库，可能存在同名key，导致异常。暂时不要使用这个功能
                for each_db in self._monitor_db:
                    # 获取 所有 指定key
                    self._redis_client.switch_db(each_db)
                    action()
            else:
                action()

            self.sync_lock = False
            time.sleep(self._sync_period)

    def _get_key_type(self, keys: list) -> list:
        pp = self._redis_client.pipeline()
        value_type_list = list()
        while keys:
            keys_tmp = keys[:self._pipeline_count]
            for each in keys_tmp:
                pp.type(each)
            res = pp.execute()
            value_type_list.extend([(key, value) for key, value in zip(keys_tmp, res)])
            keys = keys[self._pipeline_count:]
        return value_type_list

    def _get_value_by_key(self, value_type_list: list) -> dict:
        pp = self._redis_client.pipeline()
        value_dict = dict()
        while value_type_list:
            keys_tmp = value_type_list[:self._pipeline_count]
            for each in keys_tmp:
                if each[1] == "string":
                    pp.get(each[0])
                elif each[1] == "set":
                    pp.smembers(each[0])
                elif each[1] == "hash":  # todo 待验证
                    pp.hgetall(each[0])
                elif each[1] == "list":  # todo 待验证
                    pp.lrange(each[0], 0, -1)
                elif each[1] == "sorted set":  # todo 待验证
                    pp.zrange(each[0], 0, -1)
                else:
                    self.log.warning(f"type:{each[0]} not support, data is :{each}")

            res = pp.execute()
            [value_dict.update({key[0]: value}) for key, value in zip(keys_tmp, res)]
            value_type_list = value_type_list[self._pipeline_count:]
        return value_dict

    def close(self):
        self._stop = True

    def __call__(self) -> object:
        """"""
        return self


if __name__ == '__main__':
    import cacheout


    def make_fake_data():
        db = DbFactory(db_type='redis', host='0.0.0.0', password='f66sU9iP', port=26371,
                       db_name='0')
        pp = db.pipeline()
        for each in range(100):
            pp.set(each, 'aaa')
        pp.execute()
        print('done')


    try:
        # make_fake_data()

        outer_cache = cacheout.Cache()
        sy = SyncHandler(outer_cache)
    except KeyboardInterrupt:
        sy.close()
