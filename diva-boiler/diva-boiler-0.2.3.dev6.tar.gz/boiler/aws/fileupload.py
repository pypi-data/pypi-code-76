import os

from boiler import BoilerError

supported_extensions = ['mp4', 'avi']


def multipart_upload(
    client,
    video: dict,
    video_id: str,
    source_path: str,
    bucket: str,
    destination_base_directory: str = 'original',
):
    """
    Uploads a stumpf-known video to s3 for transcoding.
    """

    _, extension = os.path.splitext(source_path)
    if extension not in supported_extensions:
        raise BoilerError(f'extension={extension} unsupported for file={source_path}')
    destination_base_directory = destination_base_directory.lstrip('/')
    destination = '/'.join(
        [
            destination_base_directory,
            video['date'],
            '_'.join([video['start_time'], video['end_time']]),
            '_'.join([video['gtag'], video['location']]),
            video_id + extension,
        ]
    )
    with open(source_path, 'rb') as f:
        return client.put_object(ACL='private', Bucket=bucket, Key=destination, Body=f,)
