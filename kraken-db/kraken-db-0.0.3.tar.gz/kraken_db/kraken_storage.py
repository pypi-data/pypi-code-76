"""

Reference from : https://cloud.google.com/storage/docs/listing-objects#storage-list-objects-python


"""





from google.cloud import storage
import uuid
import json

class Storage:

    def __init__(self):
        a=1


    def get(self, bucket_name, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        # bucket_name = "your-bucket-name"
        # source_blob_name = "storage-object-name"
        # destination_file_name = "local/path/to/file"

        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

        print(
            "Blob {} downloaded to {}.".format(
                source_blob_name, destination_file_name
            )
        )




    def post(self, bucket, record):
        """Uploads a file to the bucket."""
        # bucket_name = "your-bucket-name"
        # source_file_name = "local/path/to/file"
        
        blob_name = uuid.uuid4().hex

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket)
        blob = bucket.blob(blob_name)

        blob.upload_from_string(record)

        new_record = {}
        new_record['name'] = blob.name
        new_record['bucket_name']= blob.bucket.name
        new_record['storage_class'] = blob.storage_class
        new_record['id'] = blob.id
        new_record['size'] = blob.size
        new_record['updated'] = blob.updated
        new_record['generation'] = blob.generation
        new_record['metadata'] = blob.metadata

        return new_record
        

    def delete(self, bucket_name, blob_name):
        """Deletes a blob from the bucket."""
        # bucket_name = "your-bucket-name"
        # blob_name = "your-object-name"

        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()

        print("Blob {} deleted.".format(blob_name))



    def create_bucket_class_location(self, bucket_name):
        """Create a new bucket in specific location with storage class"""
        # bucket_name = "your-new-bucket-name"

        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = "COLDLINE"
        new_bucket = storage_client.create_bucket(bucket, location="us")

        print(
            "Created bucket {} in {} with storage class {}".format(
                new_bucket.name, new_bucket.location, new_bucket.storage_class
            )
        )
        return new_bucket

        
    def list_blobs(bucket_name):
        """Lists all the blobs in the bucket."""
        # bucket_name = "your-bucket-name"

        storage_client = storage.Client()

        # Note: Client.list_blobs requires at least package version 1.17.0.
        blobs = storage_client.list_blobs(bucket_name)

        for blob in blobs:
            print(blob.name)
