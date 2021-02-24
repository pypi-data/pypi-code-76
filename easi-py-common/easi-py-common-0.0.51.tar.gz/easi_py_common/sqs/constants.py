# -*- coding: utf-8 -*-

class ConsumerLogConstants:
    PUB_LOG = '{}_pub_log'
    SUB_LOG = '{}_sub_log'

    CONSUMER_LOG_ES_BULK_NUM = 1000
    CONSUMER_LOG_ES_BULK_THREAD_NUM = 8
    CONSUMER_LOG_ES_BULK_BUFFER_SIZE = CONSUMER_LOG_ES_BULK_NUM * CONSUMER_LOG_ES_BULK_THREAD_NUM * 2
    CONSUMER_LOG_MAX_SLEEP_ES_BULK_BUFFER_SIZE = CONSUMER_LOG_ES_BULK_BUFFER_SIZE * 1.5

# 日志
PUB_LOG = 'pub_log'
SUB_LOG = 'sub_log'
PUB_LOG_BULK_SAVE = 'pub_log_bulk_save'
SUB_LOG_BULK_SAVE = 'sub_log_bulk_save'
