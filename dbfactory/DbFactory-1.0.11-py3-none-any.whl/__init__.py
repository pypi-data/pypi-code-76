# coding:utf-8
# author caturbhuja
# date   2020/8/31 2:01 下午 
# wechat chending2012

from .db_factory import DbFactory


def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


__version__ = '1.0.10'
VERSION = tuple(map(int_or_str, __version__.split('.')))

__all__ = [
    'DbFactory',
    'Mysql',
    'KafkaConsumer',
    'KafkaProducer',
    'Redis',
    'RedisCluster',
]


def filter_args(args=None, kwargs=None, gg_args=None):
    """清理 重复的参数
    调用 kafka_consumer 时，如果内层和外层，都使用了同样的参数，比如 init_type ，就会报错。
    TypeError: Singleton object got multiple values for keyword argument 'init_type'
    """
    gg_args = gg_args or ["db_type"]
    args = set(args)
    for each in gg_args:
        kwargs.pop(each, '')
        args.discard(each)
    return list(args), kwargs


def mysql(*args, **kwargs):
    args, kwargs = filter_args(args, kwargs)
    return DbFactory(db_type="mysql", *args, **kwargs)


def kafka_consumer(*args, **kwargs):
    args, kwargs = filter_args(args=args, kwargs=kwargs, gg_args=["db_type", "init_type"])
    return DbFactory(db_type="kafka", init_type='consumer', *args, **kwargs)


def kafka_producer(*args, **kwargs):
    args, kwargs = filter_args(args, kwargs, gg_args=["db_type", "init_type"])
    return DbFactory(db_type="kafka", init_type='producer', *args, **kwargs)


def redis(*args, **kwargs):
    args, kwargs = filter_args(args, kwargs)
    return DbFactory(db_type="redis", *args, **kwargs)


def redis_cluster(*args, **kwargs):
    args, kwargs = filter_args(args, kwargs)
    return DbFactory(db_type="redis_cluster", *args, **kwargs)


# ------------------ 别名 ------------------
Mysql = mysql
KafkaConsumer = kafka_consumer
KafkaProducer = kafka_producer
Redis = redis
RedisCluster = redis_cluster
