import base64
import os
import uuid

import boto3


class S3:

    def __init__(self, aws_access_key, aws_secret_access_key):
        self.aws_access_key = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key

    def delete_s3(self, key, bucket):
        s3 = boto3.resource(service_name='s3',
                            aws_access_key_id=self.aws_access_key,
                            aws_secret_access_key=self.aws_secret_access_key)
        s3.Object(bucket, key).delete()

    def upload_s3(self, upload_file, bucket, ext=''):
        try:
            s3 = boto3.resource(service_name='s3',
                                aws_access_key_id=self.aws_access_key,
                                aws_secret_access_key=self.aws_secret_access_key)
            prefix = "s3_"
            if not ext:
                ext = self.__get_upload_file_ext(upload_file)
                okey = prefix + str(uuid.uuid1()).replace('-', '') + '.' + ext
                key = okey
                s3.Bucket(bucket).put_object(Key=key, Body=upload_file)
            else:
                okey = prefix + str(uuid.uuid1()).replace('-', '') + '.' + ext
                key = okey
                s3.Bucket(bucket).put_object(Key=key, Body=upload_file)
        finally:
            upload_file.close()
        return key

    def upload_img_to_s3_by_base64(self, bucket, b64encode_data: bytes) -> str:
        img_data = base64.b64decode(b64encode_data)

        s3 = boto3.resource(service_name='s3',
                            aws_access_key_id=self.aws_access_key,
                            aws_secret_access_key=self.aws_secret_access_key)
        prefix = "s3_"
        image_name = prefix + str(uuid.uuid1()).replace('-', '') + '.png'

        s3.Bucket(bucket).put_object(Key=image_name, Body=img_data)
        return image_name

    def __get_upload_file_ext(cls, upload_file):
        try:
            filename = os.path.basename(upload_file.filename)
            ext = filename[filename.rindex('.') + 1:]
            if len(ext) == 0:
                ext = 'jpg'
            return ext.lower()
        except:
            return 'jpg'
