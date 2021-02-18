"""GCP class file"""

import os
from google.cloud import storage
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials

class GCP(object):
    """GCP.

    Args:
        object ([type]): [description]

    Returns:
        [type]: [description]
    """

    REQUIRED_FIELDS = [
        'CREDENTIAL_FILE','PROJECT_NAME','BUCKET_NAME'
    ]

    def upload(self,filename, options):
        """upload function to uplaod the file to gcp bucket.

        Args:
            filename ([type]): [description]
            options ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            credentials = service_account.Credentials.from_service_account_file(
                options['CREDENTIAL_FILE'])
            client = storage.Client(
                credentials=credentials, project=options['PROJECT_NAME'])
            bucket = client.get_bucket(options['BUCKET_NAME'])
            blob = bucket.blob(filename)
            blob.upload_from_filename(filename)
            return blob.public_url
        except Exception as E:
            print("Exception", E)

    def download(self, file_name, options):
        """download function to download the file from gcp bucket.

        Args:
            file_name ([type]): [description]
            options ([type]): [description]

        Returns:
            [type]: [description]
        """
        print("download_file")
        credentials = service_account.Credentials.from_service_account_file(options['CREDENTIAL_FILE'])
        client = storage.Client(credentials=credentials, project=options['PROJECT_NAME'])
        # storage_client = storage.Client.from_service_account_json(
        #     credentials_file)
        bucket = client.get_bucket(options['BUCKET_NAME'])
        blob = bucket.get_blob(file_name)
        blob.download_to_filename('home/Downloads')
        print("name ",blob.name)
        return storage_name
