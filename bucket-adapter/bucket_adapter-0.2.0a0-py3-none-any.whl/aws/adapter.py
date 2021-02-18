"""AWS adapter."""

import boto3
from botocore.exceptions import ClientError
import logging


class AWS(object):
    """Main AWS adapter object.

    Args:
        object ([type]): [description]
    """

    def upload(self, filename, options, object_name=None):
        """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        print("upload_file aws")
        if object_name is None:
            object_name = filename
        s3_client = boto3.client('s3',
                                 aws_access_key_id=options['ACCESS_KEY'],
                                 aws_secret_access_key=options['SECRET_KEY'])
        try:
            response = s3_client.upload_file(
                filename, options['BUCKET_NAME'], object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return ('File Uploaded on AWS S3 Bucket')

    def download(self, filename, options, object_name=None):
        """download file.

        Args:
            filename ([type]): [description]
            options ([type]): [description]
            object_name ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        print("download_file")
        if object_name is None:
            object_name = filename
        s3 = boto3.client('s3',
                          aws_access_key_id=options['ACCESS_KEY'],
                          aws_secret_access_key=options['SECRET_KEY'])
        response = s3.download_file(
            options['BUCKET_NAME'], object_name, filename)
        print("response", response)
        return response
