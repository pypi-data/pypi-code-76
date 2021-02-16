import boto3
from boto3.session import Session
import os
import logging
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

logger = logging.getLogger(__name__)


class SwitchRole:
    def __init__(self, ):
        """
        aws sts assume-role --role-arn arn:aws:iam::00000000000000:role/example-role --role-session-name example-role
        """
        self.master_session_name = 'master'

    def switch_to_admin_role(self, arn):
        logger.info("switching to admin role: {0}" .format(arn))
        self.arn = arn
        client = boto3.client('sts')
        client.get_caller_identity()["Account"]
        response = client.assume_role(RoleArn=self.arn, RoleSessionName=self.master_session_name)
        return Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                        aws_session_token=response['Credentials']['SessionToken'])

    def switch_to_child_role(self, child_role, region='us-west-2'):
        self.child_role = child_role
        if "AWS_MASTER_ROLE_ARN" not in os.environ:
            logger.error('AWS_MASTER_ROLE_ARN environment variable is not defined.')
            raise SystemExit
        master_role_arn = os.getenv("AWS_MASTER_ROLE_ARN")
        client = self.switch_to_admin_role(master_role_arn).client('sts')
        account_id = client.get_caller_identity()["Account"]
        logger.info("master account: {0}" .format(account_id))
        child_role_passed = self.child_role.strip('\n')
        logger.info('child role: {0}' .format(child_role_passed))
        logger.debug("child account arn: {0}" .format(child_role_passed))
        child_response = client.assume_role(RoleArn=child_role_passed, RoleSessionName='SecurityCentralAdmin')
        try:
            os.environ["AWS_ACCESS_KEY_ID"] = child_response['Credentials']['AccessKeyId']
            os.environ["AWS_SECRET_ACCESS_KEY"] = child_response['Credentials']['SecretAccessKey']
            os.environ["AWS_SESSION_TOKEN"] = child_response['Credentials']['SessionToken']
        except:
            logger.error('error setting environment variables')
            raise SystemExit
        if region is None:
            logger.info("no region specified, setting default region to 'us-west-2'")
        try:
            os.environ["AWS_DEFAULT_REGION"] = region
        except:
            logger.error('unable to set default region')
        return Session(aws_access_key_id=child_response['Credentials']['AccessKeyId'],
                       aws_secret_access_key=child_response['Credentials']['SecretAccessKey'],
                       aws_session_token=child_response['Credentials']['SessionToken'])


switch_role = SwitchRole()
