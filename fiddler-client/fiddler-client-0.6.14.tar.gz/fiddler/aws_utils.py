import base64
import csv
import json
import uuid
from io import StringIO

import boto3

bucket = 'sagemaker-us-west-2-079310353266'
prefix = 'sagemaker/sagemaker-xgboost-lending/'
s3_client = boto3.client('s3')


def sample_data_capture_log(bucket, prefix, sample_size):
    objects = s3_client.list_objects(Bucket=bucket, Prefix=prefix)

    result = []
    for obj in objects['Contents']:
        key = obj['Key']
        if key.endswith('.jsonl'):
            tmpkey = key.replace('/', '')
            download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
            s3_client.download_file(bucket, key, download_path)
            with open(download_path) as f:
                for line in f:
                    pline = json.loads(line)
                    input = base64.b64decode(
                        pline['captureData']['endpointInput']['data']
                    ).decode('ascii')
                    output = base64.b64decode(
                        pline['captureData']['endpointOutput']['data']
                    ).decode('ascii')
                    # input = pline['captureData']['endpointInput']['data']
                    # output = pline['captureData']['endpointOutput']['data']
                    inputstr = StringIO(input)
                    inarray = next(csv.reader(inputstr, delimiter=','))
                    outputstr = StringIO(output)
                    outarray = next(csv.reader(outputstr, delimiter=','))
                    result.append(inarray + outarray)
                    if len(result) >= sample_size:
                        return result

    return result
