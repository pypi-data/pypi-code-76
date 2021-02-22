# coding:utf-8
# author caturbhuja
# date   2020/8/31 5:10 下午 
# wechat chending2012 

# python pack
from functools import wraps


def redis_cache(function):
    """实现redis缓存"""
    @wraps(function)
    def warp(*args, **kwargs):
        config = args[0].config
        if config.get('use_redis_local_cache') and config.get('db_type') in ["redis", "redis_cluster"]:
            read_func_class = ['get', 'mget', 'smembers', 'keys', 'scan']  # 这里选择手动维护，为了提速。
            mini_redis = config.get('mini_redis')
            if not mini_redis:
                raise ValueError('not cache instance')
            method = args[1]
            mini_args = args[2:]
            if method in read_func_class:
                res = getattr(mini_redis, method)(*mini_args, **kwargs)
                # print("res1:{}".format(res))
                # 没有结果，且允许直接读取redis。
                if not res and not config.get('only_read_from_mini_redis'):  # todo 这里待验证，返回值失败时，res状态。 None/[]/{}
                    res = function(*args, **kwargs)
            else:
                res = function(*args, **kwargs)
                # print("res2:{}".format(res))
                if res:  # todo 这里待验证，返回值失败时，res状态。 bool
                    getattr(mini_redis, method)(*mini_args, **kwargs)
        else:
            res = function(*args, **kwargs)
        return res
    return warp


if __name__ == '__main__':
    pass
