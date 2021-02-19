# TODO add to beepbeep.gcs
from typing import Union, Any
import os
from google.cloud import storage


def get_list_of_objects_in_bucket(source_bucket_name: str) -> Union[list, None]:
    """
    Retrieves a list of buckets for the given project.

    Parameters:
    -----------
    Required query parameters:
        source_bucket_name (str) : A valid API project identifier. Required query parameters.
    
    Returns:
    --------
    If successful, this method returns a response body with the bucket object list.

    """
    try:
        project_id = os.environ.get('GCP_PROJECT')
        GCS = storage.Client(project=project_id)
        
        source_bucket = GCS.get_bucket(source_bucket_name)
        bucket_objects = source_bucket.list_blobs()

        bucket_object_list: Union[list, None] = [bucket_object.name for bucket_object in bucket_objects]

    except Exception as e:
        print(e)
        bucket_object_list = None
    
    return bucket_object_list


def download_object_from_gcs_to_local_path(
                        source_bucket_name: str, 
                        input_filename: str, 
                        file_path: str ="/tmp/") -> Union[str, None]:

    """
    Send download requests to Cloud Storage to a temporary destination.


    Parameters:
    Required query parameters:
        source_bucket_name (str) : The bucket name containing the object to download.
        input_filename (str) : The name of the object to download.
        file_path (str) : The local path to save the object.
    
    Returns:
        If successful, it returns a response with the local file path.
        Otherwise it returns a result of type None.
    """

    try:
        project_id = os.environ.get('GCP_PROJECT')
        GCS = storage.Client(project=project_id)                

        # ge bucket and object
        origin_bucket = GCS.get_bucket(source_bucket_name)
        blob = origin_bucket.get_blob(input_filename)

        # set path and download 
        local_filepath : Union[str, None] = None
        local_filepath = file_path + input_filename
        blob.download_to_filename(local_filepath)
        print(f"file {input_filename} downloaded from gs://{source_bucket_name} to {local_filepath}")

    except Exception as e:
        print (e)
        local_filepath = None


    return local_filepath 


def load_file_to_gcs(file: str, destination_bucket_name: str, destination_filename: str) -> Union[str, None, Any]:
    """
    Upload new file at Google Cloud Storage Bucket.


    Parameters:
    Required query parameters:
        file (str) : The file to upload.
        destination_bucket_name (str) : Define the path within the bucket and the file name 
        destination_filename (str) : The destination filename.
    
    Returns:
        If successful, it returns a status.
        Otherwise it returns a result of type None.
    """

    try:
        project_id = os.environ.get('GCP_PROJECT')
        GCS = storage.Client(project=project_id)
        bucket = GCS.get_bucket(destination_bucket_name)
        blob = bucket.blob(destination_filename)
        status = blob.upload_from_filename(file)

    except Exception as e:
        print(e)
        status = None

    return status


