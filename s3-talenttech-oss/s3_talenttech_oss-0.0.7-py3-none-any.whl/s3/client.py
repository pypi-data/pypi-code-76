import logging
import os
import threading

import boto3
import sys


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)"
                % (self._filename, self._seen_so_far, self._size, percentage)
            )
            sys.stdout.flush()


class Client:
    def __init__(
            self,
            aws_access_key_id=None,
            aws_secret_access_key=None,
            endpoint_url=None,
            bucket=None,
    ):
        log_format = "%(asctime)-15s %(name)s:%(levelname)s: %(message)s"

        logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)
        logging.basicConfig(format=log_format, stream=sys.stderr, level=logging.ERROR)
        logging.captureWarnings(True)
        self.logger = logging.getLogger("TOPMIND-S3")

        self.config = {
            "aws_access_key_id": aws_access_key_id or os.getenv("S3_ACCESS_KEY_ID"),
            "aws_secret_access_key": aws_secret_access_key
                                     or os.getenv("S3_SECRET_ACCESS_KEY"),
            "endpoint_url": endpoint_url or os.getenv("S3_ENDPOINT_URL"),
            "service_name": "s3",
        }

        self.bucket = bucket or os.getenv("S3_BUCKET")
        self.session = boto3.session.Session()
        self.s3_client = self.session.client(**self.config)
        self.s3_resource = self.session.resource(**self.config)
        self.root_dir = None

    def init_root_dir(
            self, etl_name_no_version, task_id, execution_date, data_type="staging"
    ):
        """
        init s3 directory by using a few params
        :param etl_name_no_version:
        :param task_id: task_id in airflow
        :param execution_date: execution date in airflow
        :param data_type: staging/landing/e.t.c
        :return: prefix to s3 path
        """
        self.root_dir = (
            f"etl/{data_type}/{etl_name_no_version}/{task_id}/{execution_date}/"
        )

    def dir_to_s3(self, path):
        if path.startswith("/"):
            path = path[1:]
        return os.path.join(path, "")

    def updated_path(self, path):
        return (self.root_dir or "") + path

    def is_file(self, path):
        path = self.updated_path(path)
        raise Exception("not implemented")

    def path_exists(self, path):
        path = self.updated_path(path)
        s3_dir = self.dir_to_s3(path)
        delim_num = s3_dir.count("/")
        b = self.s3_resource.Bucket(self.bucket)
        return (
                len(
                    list(
                        (
                            f.key
                            for f in b.objects.filter(Prefix=s3_dir)
                            if f.key.count("/") == delim_num
                        )
                    )
                )
                != 0
        )

    def create_file(self, path, data=""):
        path = self.updated_path(path)
        self.s3_client.put_object(Bucket=self.bucket, Key=path, Body=data)

    def create_dir(self, path):
        path = self.updated_path(path)
        self.s3_client.put_object(Bucket=self.bucket, Key=self.dir_to_s3(path))

    def upload_file(self, src, dst):
        dst = self.updated_path(dst)
        self.s3_client.upload_file(
            Bucket=self.bucket, Filename=src, Key=dst, Callback=ProgressPercentage(src)
        )

    def read_file(self, path):
        path = self.updated_path(path)
        content = self.s3_client.get_object(Bucket=self.bucket, Key=path)
        return str(content["Body"].read(), "utf-8")

    def bulk_read(self, path):
        path = self.updated_path(path)
        result = []
        file_list = self.get_file_list(path)
        for k in file_list:
            result.append(self.read_file(k))
        return result

    def delete_dir(self, path):
        path = self.updated_path(path)
        b = self.s3_resource.Bucket(self.bucket)
        b.objects.filter(Prefix=self.dir_to_s3(path)).delete()

    def delete_file(self, path):
        path = self.updated_path(path)
        self.s3_client.delete_object(Bucket=self.bucket, Key=path)

    def get_file_list(self, parent_path):
        parent_path = self.updated_path(parent_path)
        s3_dir = self.dir_to_s3(parent_path)
        delim_num = s3_dir.count("/")
        b = self.s3_resource.Bucket(self.bucket)
        return list(
            (
                f.key
                for f in b.objects.filter(Prefix=s3_dir)
                if not f.key.endswith("/") and f.key.count("/") == delim_num
            )
        )
