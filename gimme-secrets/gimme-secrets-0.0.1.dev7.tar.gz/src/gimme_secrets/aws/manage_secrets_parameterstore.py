from .decrypt_encrypt import *
import os

logger = logging.getLogger(__name__)


class GetValuesFromLocker:
    def __init__(self):
        self.name = None
        self.region = None
        self.role_arn = None
        self.kms_keyid = None

    def get_value_from_parameter_store(self,
                                       name,
                                       region,
                                       role_arn=None,
                                       kms_keyid=None):
        self.name = name
        self.region = region
        self.role_arn = role_arn
        self.kms_keyid = kms_keyid
        logger.info("getting value for parameter store for: {0}" .format(self.name))
        logger.debug('kms_keyid: {0}'.format(self.kms_keyid))
        child_session = switch_role.switch_to_child_role(self.role_arn, self.region)
        ssmclient = child_session.client('ssm')
        try:
            logger.info("ssm client: {0}" .format(child_session))
            parameter = ssmclient.get_parameter(Name=name, WithDecryption=True)
            print("value: {0}".format(parameter['Parameter']['Value']))
        except ssmclient.exceptions.ParameterNotFound:
            logging.error("not found")

    def get_value_from_parameters_store_by_path(self,
                                                path,
                                                region,
                                                role_arn=None):
        logger.info("getting list of value for parameter store path: {0}" .format(path))
        client = boto3.client('ssm')
        try:
            child_session = switch_role.switch_to_child_role(role_arn, region)
            ssmclient = child_session.client('ssm')
            logger.info("ssm client: {0}" .format(child_session))
            parameters = ssmclient.get_parameters_by_path(Path=path, Recursive=True, WithDecryption=True)
            for i in parameters['Parameters']:
                dict_variable = {key: value for (key, value) in i.items()}
                print("\n Key\n", dict_variable['Name'], "\n Value\n", dict_variable['Value'])
        except client.exceptions.ParameterNotFound:
            logging.error("not found")

    def put_value_to_parameter_store(self,
                                     text,
                                     valuetype,
                                     name,
                                     overwrite_value,
                                     region,
                                     child_role_arn=None,
                                     kms_keyid=None
                                     ):
        logger.info('text to push: {0}'.format(text))
        logger.info('resource_type: {0}'.format(valuetype))
        logger.info('name: {0}'.format(name))
        logger.info('kms_keyid: {0}'.format(kms_keyid))
        try:
            logger.info("put parameter store in different account")
            child_session = switch_role.switch_to_child_role(child_role_arn, region)
            ssmclient = child_session.client('ssm')
            logger.info("ssm client: {0}" .format(child_session))
            response = ssmclient.put_parameter(
                Name=name,
                Description=name,
                Value=text,
                Type=valuetype,
                KeyId=kms_keyid,
                Overwrite=overwrite_value,
                Tier='Standard',
                DataType='text'
            )
            logger.info("value updated: {0}".format(response['Version']))
        except:
            logger.error("unable to put Parameter Store entry:\nName: {0}\nValue: {1}\nRegion: {2}\nRole arn: {3}" .format(name, text, region, child_role_arn))

    def copy_value_across(self,
                          source_cloud,
                          dest_cloud,
                          ciphertext,
                          source_role_arn,
                          dest_role_arn,
                          source_region,
                          dest_region,
                          resource_type, name,
                          valuetype,
                          source_kms_keyid,
                          dest_kms_keyid,
                          overwrite):
        logger.info('source_cloud: {0}'.format(source_cloud))
        logger.info('dest_cloud: {0}'.format(dest_cloud))
        logger.info('ciphertext: {0}'.format(ciphertext))
        logger.info('source_role_arn: {0}'.format(source_role_arn))
        logger.info('dest_account_arn: {0}'.format(dest_role_arn))
        logger.info('source_region: {0}'.format(source_region))
        logger.info('resource_type: {0}'.format(resource_type))
        logger.info('name: {0}'.format(name))
        logger.info('dest_region: {0}'.format(dest_region))
        logger.info('valuetype: {0}'.format(valuetype))
        logger.info('source_kms_keyid: {0}'.format(source_kms_keyid))
        logger.info('dest_kms_keyid: {0}'.format(dest_kms_keyid))
        logger.info('overwrite: {0}'.format(overwrite))
        """
        decrypt in source account
        """
        logger.info("calling decrypt on source account")
        try:
            decrypted_value = get_secret.decrypt_secret(source_kms_keyid, source_role_arn, source_region, ciphertext)
        except:
            logger.error("unable to decrypt")
            raise SystemExit
        """
        encrypt in destination account
        """
        logger.info("calling encrypt in dest account")
        try:
            encrytped_value = get_secret.encrypt_secret(decrypted_value, dest_kms_keyid, dest_role_arn, dest_region)
        except:
            logger.error("unable to encrypt")
            raise SystemExit
        logger.info("put key in dest account")
        try:
            self.put_value_to_parameter_store(encrytped_value,
                                              valuetype,
                                              name,
                                              overwrite,
                                              dest_region,
                                              dest_role_arn,
                                              dest_kms_keyid)
        except:
            logger.error("unable to put value in Parameter Store")
            raise SystemExit


manage_values = GetValuesFromLocker()
