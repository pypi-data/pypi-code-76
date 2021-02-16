import logging

import click

import gimme_secrets.aws.decrypt_encrypt as aws_decrypt_encrypt
import gimme_secrets.aws.manage_secrets_parameterstore as aws_manage_secrets

import gimme_secrets.azure.decrypt_encrypt as azure_decrypt_encrypt
import gimme_secrets.azure.manage_secrets as azure_manage_secrets

import gimme_secrets.gcp.decrypt_encrypt as gcp_decrypt_encrypt
from .logging import configure_logging

logger = logging.getLogger(__name__)


@click.group()
def entrypoint():
    """
    Command-line interface for managing secrets for:\n
     AWS
    """
    configure_logging()


"""
To encrypt secret using KMS key
"""


@entrypoint.command()
@click.option('--keyid', required=True, prompt=True,
              help='aws kms key id')
@click.option('--child_role_arn', required=True, default='local', prompt=True,
              help='destination account to get key from, default to local master account')
@click.option('--region', required=False, default='us-west-2', prompt=True,
              help='region to query , e.g.us-west-2')
@click.option('--secret', required=True, prompt=True,
              help='secret to encrypt')
def aws_encrypt_secret(keyid, region, secret, child_role_arn):
    """aws encrypt secrets using kms key"""
    click.echo("Encrypt AWS secret")
    aws_decrypt_encrypt.get_secret.encrypt_secret(secret, keyid, child_role_arn, region)


"""
To decrypt secret using KMS key
"""


@entrypoint.command()
@click.option('--keyid', required=True, prompt=True,
              help='for AWS: KMS key ID')
@click.option('--ciphertext', required=True, prompt=True,
              help='Cipher text from AWS')
@click.option('--account_role_arn', required=True, prompt=True,
              help='AWS account ID')
@click.option('--region', default='us-west-2', required=True, prompt=True,
              help='AWS region')
def aws_decrypt_secret(keyid, account_role_arn, region, ciphertext):
    """aws decrypt secrets using kms key"""
    click.echo("Decrypt AWS secret")
    aws_decrypt_encrypt.get_secret.decrypt_secret(keyid, account_role_arn, region, ciphertext)


"""
To get values from Parameter Store/Secrets Manager
"""


@entrypoint.command()
@click.option('--resource_type', default='parameterstore', required=False, prompt=True,
              help='AWS resource type: parameterstore or secretsmanager')
@click.option('--valuetype', default='String', required=False, prompt=True,
              help='one of String, StringList, SecureString')
@click.option('--name', required=False,
              help='name or path is required')
@click.option('--path', required=False,
              help='name or path is required')
@click.option('--region', required=False, default='us-west-2', prompt=True,
              help='region to query , e.g.us-west-2')
@click.option('--kms_keyid', required=False,
              help='The KMS Key ID that you want to use to encrypt a parameter')
@click.option('--decrypt/--no-decrypt', default=False, required=False,
              help='show decrypted value or not')
@click.option('--child_role_arn', required=True, default='local', prompt=True,
              help='destination account to get key from, default to local master account')
def aws_get_secret(child_role_arn,
                   resource_type,
                   valuetype,
                   name,
                   path,
                   kms_keyid,
                   region,
                   decrypt
                   ):
    """aws get values from Parameter Store"""
    if resource_type.lower() == 'parameterstore':
        if name is not None:
            if valuetype.lower() == 'securestring':
                if kms_keyid is not None:
                    click.echo("SecuredString: Parameter Store entry")
                    try:
                        aws_manage_secrets.manage_values.get_value_from_parameter_store(name, region, child_role_arn,
                                                                                        kms_keyid)
                    except:
                        click.echo("unable to decrypt values")
                else:
                    click.echo("kms_keyid is required for ValueType SecureString")
            else:
                click.echo("ParameterStore entry for: {0}".format(name))
                aws_manage_secrets.manage_values.get_value_from_parameter_store(name, region, child_role_arn,
                                                                                kms_keyid=None)
        elif path is not None:
            click.echo("ParameterStore entry for path: {0}".format(path))
            aws_manage_secrets.manage_values.get_value_from_parameters_store_by_path(path, region, child_role_arn)
        else:
            logger.error('--name or --path not defined')


"""
To put values in Parameter Store/Secrets Manager
"""


@entrypoint.command()
@click.option('--text', required=True, prompt=True,
              help='Plain text or Cipher text')
@click.option('--child_role_arn', required=True, default='local', prompt=True,
              help='destination account to get key from, default to local master account')
@click.option('--region', required=False, default='us-west-2', prompt=True,
              help='region to query , e.g.us-west-2')
@click.option('--resource_type', default='parameterstore', required=True, prompt=True,
              help='AWS resource type: parameterstore or secretsmanager')
@click.option('--name', required=True, prompt=True,
              help='name , e.g./<project_name>/<application_name>')
@click.option('--valuetype', default='String', required=False, prompt=True,
              help='one of String, StringList, SecureString')
@click.option('--kms_keyid', required=False,
              help='The KMS Key ID that you want to use to encrypt a parameter')
@click.option('--overwrite/--no-overwrite', default=False, required=False,
              help='overwrite existing value')
def aws_put_secret(text,
               child_role_arn,
               region,
               resource_type,
               name,
               valuetype,
               kms_keyid,
               overwrite,
               ):
    """aws put values in Parameter Store"""
    if resource_type.lower() != 'secretsmanager':
        if valuetype.lower() == 'securestring':
            if kms_keyid is not None:
                click.echo("SecuredString: Parameter Store entry")
                try:
                    aws_manage_secrets.manage_values.put_value_to_parameter_store(text,
                                                                                  valuetype,
                                                                                  name,
                                                                                  overwrite,
                                                                                  region,
                                                                                  kms_keyid)
                except:
                    click.echo("unable to put secret")
            else:
                click.echo("kms_keyid is required for ValueType SecureString")
        else:
            click.echo("ParameterStore entry for: {0}".format(valuetype.lower()))
            aws_manage_secrets.manage_values.put_value_to_parameter_store(text,
                                                                          valuetype,
                                                                          name,
                                                                          overwrite,
                                                                          region,
                                                                          child_role_arn,
                                                                          kms_keyid)

    else:
        click.echo("Secrets Manager")
        aws_manage_secrets.manage_values.put_value_to_secrets_manager(text, valuetype, name, overwrite, region,
                                                                      kms_keyid=None)


"""
To copy secret from one account to another or from one cloud provider to another
"""


@entrypoint.command()
@click.option('--source_cloud', default='aws', required=False, prompt=True,
              help='available options: aws, azure and gcp')
@click.option('--dest_cloud', default='aws', required=False, prompt=True,
              help='available options: aws, azure and gcp')
@click.option('--ciphertext', required=True, prompt=True,
              help='Cipher text to move')
@click.option('--source_role_arn', required=True, prompt=True,
              help='AWS account role arn where to copy from ')
@click.option('--dest_role_arn', required=True, prompt=True,
              help='AWS account role arn where to copy to')
@click.option('--source_region', default='us-west-2', required=True, prompt=True,
              help='AWS region')
@click.option('--dest_region', default='us-east-1', required=True, prompt=True,
              help='AWS region')
@click.option('--resource_type', default='parameterstore', required=True, prompt=True,
              help='AWS resource type: parameterstore or secretsmanager')
@click.option('--name', required=True, prompt=True,
              help='name , e.g./<project_name>/<application_name>')
@click.option('--valuetype', default='SecureString', required=True, prompt=True,
              help='one of String, StringList, SecureString')
@click.option('--source_kms_keyid', required=True, prompt=True,
              help='The Source KMS Key ID used to encrypt the secret')
@click.option('--dest_kms_keyid', required=True, prompt=True,
              help='The Destination KMS Key ID that will be used to encrypt the secret')
@click.option('--overwrite/--no-overwrite', default=False, required=False, prompt=True,
              help='overwrite existing value')
def copy_secret(source_cloud, dest_cloud, ciphertext, source_role_arn, dest_role_arn, source_region, dest_region,
                resource_type, name, valuetype, source_kms_keyid, dest_kms_keyid, overwrite):
    """copy secrets"""
    print("inside")
    if source_cloud.lower() == 'aws' and dest_cloud.lower() == 'aws':
        if resource_type.lower() == 'parameterstore':
            if valuetype.lower() == 'securestring':
                if source_kms_keyid is not None and dest_kms_keyid is not None:
                    click.echo("SecuredString: Parameter Store entry")
                    try:
                        aws_manage_secrets.manage_values.copy_value_across(source_cloud, dest_cloud, ciphertext,
                                                                           source_role_arn, dest_role_arn,
                                                                           source_region, dest_region, resource_type,
                                                                           name, valuetype, source_kms_keyid,
                                                                           dest_kms_keyid, overwrite)
                    except:
                        click.echo("unable to copy secret")
                else:
                    click.echo("kms_keyid is required for ValueType SecureString")
            else:
                logger.error("String and StringList options are not supported")


# def entrypoint():
#     """The entry that the CLI is executed from"""
# try:
#     entrypoint()
# except Exception as e:
#     click.secho(f"ERROR: {e}", bold=True, fg="red")
if __name__ == "__main__":
    entrypoint()
