# -*- coding: utf-8 -*-
import oss2


class OssToolCls:
    """
    截图上传工具类
    """

    @staticmethod
    def put_file(key, secret, bucket, path, local_path):
        """
        上传本地文件到oss存储
        :param key:
        :param secret:
        :param bucket:
        :param path:
        :param local_path:
        :return: 响应码 ”200“ 上传成功
        """
        auth = oss2.Auth(key, secret)
        bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', bucket)

        # <path>上传文件到OSS时需要指定包含文件后缀在内的完整路径，例如abc/efg/123.jpg。
        # <local_path>由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
        result = bucket.put_object_from_file(path, local_path)
        return str(result.status)
