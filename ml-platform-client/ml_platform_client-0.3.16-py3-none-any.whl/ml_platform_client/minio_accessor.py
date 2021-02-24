import os
import traceback

import time
from minio import Minio

from .config import global_config
from .logger import log


class MinIOAccessor:
    _client = None
    max_retry = 3

    @staticmethod
    def init_client(host, access_key, secret_key, secure):
        minio_client_instance = Minio(host, access_key=access_key, secret_key=secret_key, secure=secure)
        log.info('minio connection info: host={}, access_key={}, secret_key={}, secure={}'
                 .format(host, access_key, secret_key, secure))
        MinIOAccessor._client = minio_client_instance

    @staticmethod
    def get_client() -> Minio:
        if MinIOAccessor._client is None:
            # minio_host = '172.16.102.156:9000'
            # minio_access_key = '24WTCKX23M0MRI6BA72Y'
            # minio_secret_key = '6mxoQMf1Lha2q1H3fp3fjNHEZRJJ7LvbC5k3+CQX'
            # minio_secure = False
            MinIOAccessor.init_client(global_config.minio_host, global_config.minio_access_key,
                                      global_config.minio_secret_key, global_config.minio_secure)
            # raise Exception('client is not initialized')
        return MinIOAccessor._client

    @staticmethod
    def fget_object(filepath: str, save_path: str):
        pos = filepath.index('/')
        bucket = filepath[:pos]
        filepath = filepath[pos + 1:]
        retry = 0
        while retry < MinIOAccessor.max_retry:
            try:
                MinIOAccessor.get_client().fget_object(bucket, filepath, save_path)
                log.info('read file from minio success: {}.{}'.format(bucket, filepath, retry))
                return
            except Exception as e:
                log.error('read file from minio error: {}.{}, retry:{}'.format(bucket, filepath, retry))
                log.error(e)
                traceback.print_exc()
                retry += 1
                time.sleep(2)
        log.error('read file from minio fail: {}.{}'.format(bucket, filepath))

    @staticmethod
    def save_object(local_path: str, remote_path: str):
        pos = remote_path.index('/')
        bucket = remote_path[:pos]
        filepath = remote_path[pos + 1:]
        with open(local_path, 'rb') as file_data:
            file_stat = os.stat(local_path)
            MinIOAccessor.get_client().put_object(bucket, filepath, file_data, file_stat.st_size)

    @staticmethod
    def delete(bucket, prefix: str, recursive=False):
        objs = MinIOAccessor.get_client().list_objects(bucket, prefix, recursive)
        for obj in objs:
            MinIOAccessor.get_client().remove_object(bucket, obj.object_name)
