# -*- coding: utf-8 -*-
"""
----------------------------------------------------
    File Name:              cache
    Description             
    Author:                 develop
    date:                   2019/4/8
----------------------------------------------------
"""
__author__ = 'develop'

import time
import simplejson as json
import pickle
# import json

from flask_templates.common.redis_module import MyRedis, cache_decorator


def __combine_key(src_id, cache_type=None):
    key = src_id
    if cache_type is None:
        key = str(key)
    else:
        key = str(cache_type) + "::" + str(key)
    return key


@cache_decorator()
def set_json_cache(src_id, content, cache_type=None, ex=None, redis_client=None, **kwargs):
    key = __combine_key(src_id, cache_type)
    if ex:
        redis_client.expire(key, ex)
    return redis_client.set(key, json.dumps(content))


@cache_decorator(master=False)
def get_json_cache(src_id, cache_type=None, redis_client=None, **kwargs):
    key = __combine_key(src_id, cache_type)
    res = redis_client.get(key)
    if res is None:
        return None
    return json.loads(res)


@cache_decorator()
def set_pickle_cache(src_id, content, cache_type=None, redis_client=None, **kwargs):
    key = __combine_key(src_id, cache_type)
    value = pickle.dumps(content)
    return redis_client.set(key, value)


@cache_decorator(master=False)
def get_pickle_cache(src_id, cache_type=None, redis_client=None, **kwargs):
    key = __combine_key(src_id, cache_type)
    res = redis_client.get(key)
    if res is None:
        return None
    return pickle.loads(res)


@cache_decorator()
def clear_cache(src_id, cache_type=None, redis_client=None, **kwargs):
    key = __combine_key(src_id, cache_type)
    return redis_client.delete(key)


@cache_decorator(master=False)
def keys_cache(pattern, redis_client=None, **kwargs):
    return redis_client.keys(pattern)


@cache_decorator()
def set_hash_cache(src_id, content, cache_type=None, redis_client=None, **kwargs):
    """
    设置缓存
    :param src_id:
    :param content:
    :param cache_type:
    :param redis_client:
    :return:
    """
    key = __combine_key(src_id, cache_type)
    return redis_client.hmset(key, content)


@cache_decorator(master=False)
def get_hash_cache(src_id, cache_type=None, redis_client=None, **kwargs):
    key = __combine_key(src_id, cache_type)
    return redis_client.hgetall(key)


@cache_decorator()
def clear_db(redis_client=None, **kwargs):
    return redis_client.flushdb()


@cache_decorator()
def set_hash_item_cache(src_id, content_key, content_value, cache_type=None, redis_client=None, **kwargs):
    key = __combine_key(src_id, cache_type)
    res = redis_client.hset(key, content_key, content_value)
    return res


@cache_decorator(master=False)
def get_hash_item_cache(src_id, content_key, cache_type=None, redis_client=None, **kwargs):
    key = __combine_key(src_id, cache_type)
    return redis_client.hget(key, content_key)


@cache_decorator()
def clear_hash_item_cache(src_id, *content_keys, cache_type=None, redis_client=None, **kwargs):
    key = __combine_key(src_id, cache_type)
    return redis_client.hdel(key, *content_keys)


@cache_decorator()
def set_cache(src_id, content_value, cache_type=None, redis_client=None, **kwargs):
    key = __combine_key(src_id, cache_type)
    return redis_client.set(key, content_value)


@cache_decorator(master=False)
def get_cache(src_id, cache_type=None, redis_client=None, **kwargs):
    key = __combine_key(src_id, cache_type)
    return redis_client.get(key)


@cache_decorator()
def set_list_cache(src_id, content_values, cache_type=None, redis_client=None, **kwargs):
    key = __combine_key(src_id, cache_type)
    return redis_client.lpush(key, *content_values)


@cache_decorator(master=False)
def get_list_cache(src_id, start=0, end=None, cache_type=None, redis_client=None, **kwargs):
    key = __combine_key(src_id, cache_type)
    if not end:
        end = -1
    return redis_client.lrange(key, start, end)


if __name__ == "__main__":
    set_json_cache("a", 1, None, None, redis_name="default")
    print(get_json_cache("a", None, MyRedis().get_redis_client()))
