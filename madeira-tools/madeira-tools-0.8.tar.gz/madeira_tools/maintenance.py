import logging

import boto3
from madeira_utils import loggers
from madeira import aws_lambda, session, sts


class Maintenance(object):

    def __init__(self, debug=False, trace_boto3=False):
        self._logger = loggers.get_logger(level=logging.DEBUG if debug else logging.INFO)

        self._aws_lambda = aws_lambda.AwsLambda(logger=self._logger)
        self._session = session.Session()
        self._sts = sts.Sts()

        if trace_boto3:
            # extreme verbosity in boto3 code paths. useful for tracing AWS API calls that time out
            # after many retries without explaining why (happens with HTTP 500 responses)
            boto3.set_stream_logger('')

    def _init_message(self):
        self._logger.info("AWS account ID: %s", self._sts.account_id)
        self._logger.info("AWS credential profile: %s", self._session.profile_name)
        self._logger.info("AWS default region: %s", self._session.region)

    def delete_orphan_lambda_layer_versions(self):
        used_layer_arns = set()
        for function in self._aws_lambda.list_functions():
            for function_layer in function['Layers']:
                used_layer_arns.add(function_layer['Arn'])

        for layer in self._aws_lambda.list_layers():
            for layer_version in self._aws_lambda.list_layer_versions(layer['LayerName']):
                if layer_version['LayerVersionArn'] not in used_layer_arns:
                    self._aws_lambda.delete_layer_version(layer['LayerName'], layer_version['Version'])
