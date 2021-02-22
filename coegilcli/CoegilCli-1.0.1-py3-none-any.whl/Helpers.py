import boto3


def put_s3_object(bucket, key, body, content_type: str = None, credential_override=None):
    client = _get_client('s3', credential_override)
    if isinstance(body, str):
        body = str.encode(body)
    params = {
        'ACL': 'private',
        'Body': body,
        'Bucket': bucket,
        'Key': key
    }
    if content_type is not None:
        params['ContentType'] = content_type
    client.put_object(**params)


def _get_client(name, credential_override):
    if credential_override is None:
        return boto3.client(name)
    else:
        params = {
            'aws_access_key_id': credential_override['AccessKeyId'],
            'aws_secret_access_key': credential_override['SecretAccessKey'],
        }
        session_token = credential_override.get('SessionToken')
        if session_token is not None:
            params['aws_session_token'] = session_token
        session = boto3.Session(**params)
        client = session.client(name)
        return client
