import boto3
import json
from dukeai.config import duke_auto_lambda_arn, orchatect_auto_lambda_arn, ralock_auto_lambda_arn


def duke_auto(text):
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    payload = json.dumps({
                           "local": True,
                           "text": text
                        })

    lambda_response = lambda_client.invoke(
                                            FunctionName=duke_auto_lambda_arn,
                                            InvocationType='RequestResponse',
                                            Payload=payload
                                          )

    resp_str = lambda_response['Payload'].read()
    response = json.loads(resp_str)
    return response


def orchatect_auto(text):
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    payload = json.dumps({
                            "local": True,
                            "text": text
                        })

    lambda_response = lambda_client.invoke(
                                            FunctionName=orchatect_auto_lambda_arn,
                                            InvocationType='RequestResponse',
                                            Payload=payload
                                          )
    resp_str = lambda_response['Payload'].read()
    response = json.loads(resp_str)
    return response


def ralock_auto(text):
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    payload = json.dumps({
                            "local": True,
                            "text": text
                        })

    lambda_response = lambda_client.invoke(
                                            FunctionName=ralock_auto_lambda_arn,
                                            InvocationType='RequestResponse',
                                            Payload=payload
                                        )

    resp_str = lambda_response['Payload'].read()
    response = json.loads(resp_str)
    return response
