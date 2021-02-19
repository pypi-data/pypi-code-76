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
        """Generates a v2 signed URL for downloading a blob.
        Note that this method requires a service account key file. You can not use
        this if you are using Application Default Credentials from Google Compute
        Engine or from the Google Cloud SDK.


        Args:
            file_name ([type]): [description]
            options ([type]): [description]

        Returns:
            [type]: [description]
        """
        credentials = service_account.Credentials.from_service_account_file(options['CREDENTIAL_FILE'])
        storage_client = storage.Client(credentials=credentials,project=options['PROJECT_NAME'])
        bucket = storage_client.bucket(options['BUCKET_NAME'])
        blob = bucket.blob(blob_name=filename)

        url = blob.generate_signed_url(
            expiration=datetime.timedelta(hours=1),
            method="GET",
        )
        print("The signed url for {} is {}".format(blob.name, url))
        return url
