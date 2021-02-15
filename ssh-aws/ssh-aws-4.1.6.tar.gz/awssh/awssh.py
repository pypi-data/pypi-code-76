#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3
import botocore.exceptions as exceptions
import sys
from os import path, system, getenv, rename
import configparser
from pprint import pprint
import argparse
import itertools
from collections import deque
import time
import six
from botocore.exceptions import ClientError
import json

VERSION = "4.1.6"


def connect(instance: object, args: argparse.Namespace):
    """
    :param instance: <class 'boto3.resources.factory.ec2.Instance'> objects
        e.g.: ec2.Instance(id='i-0b4e31bc0b')
    :param args: <class 'argparse.Namespace'>
    :return:
    """
    details = get_details(instance)
    print('\nConnecting to: {name}'.format(**details))
    if args.verbose:
        pprint(details)

    if args.console_output:
        print('\n================== console output start ==================')
        print(instance.console_output().get('Output', '').replace('\\n', '\n'))
        print('=================== console output end ===================\n')

    users = deque(args.users)
    # return code 65280 is 'Permission Denied'
    while _connect(users.popleft(), instance, args) == 65280 and len(users):
        pass


def _connect(user: str, instance: object, args: argparse.Namespace) -> int:
    """
    :param user:  <class 'str'>
    :param instance: <class 'boto3.resources.factory.ec2.Instance'> objects
        e.g.: ec2.Instance(id='i-0b4e31bc0b')
    :param args: <class 'argparse.Namespace'>
    :return:  <class 'int'> system(command) std out  int result
    """
    config = {
        'key_path': get_key_path(args, instance),
        'tunnel': get_tunnel(args),
        'host': "{}@{}".format(user, instance.public_ip_address),
        'timeout': args.timeout
    }

    if config['key_path']:
        command = 'ssh -i {key_path} {tunnel} {host} -o ConnectTimeout={timeout}'.format(**config)
    else:
        command = 'ssh {tunnel} {host} -o ConnectTimeout={timeout}'.format(**config)

    if args.command:
        command = "{} -tt '{}'".format(command, args.command)

    print('\nTrying with user "{}".\nCommand: {}'.format(user, command))
    return system(command)


def jump_connect(ssh_instance: object, jump_server: object, args: argparse.Namespace) -> bool:
    """
    :param ssh_instance: <class 'boto3.resources.factory.ec2.Instance'> objects
        e.g.: ec2.Instance(id='i-0b4e31bc0b')
    :param jump_server: <class 'boto3.resources.factory.ec2.Instance'> objects
        e.g.: ec2.Instance(id='i-0b4e31bc0b')
    :param args: <class 'argparse.Namespace'>
    :return:  <class 'bool'>
    """
    details_ssh_instance = get_details(ssh_instance)
    details_jump_server = get_details(jump_server)
    print('\nConnecting to {} via {}:'.format(details_ssh_instance.get('name'), details_jump_server.get('name')))
    if args.verbose:
        pprint(details_ssh_instance)

    if args.console_output:
        print('\n================== console output start ==================')
        print(ssh_instance.console_output().get('Output', '').replace('\\n', '\n'))
        print('=================== console output end ===================\n')

    users = deque(args.users)
    # return code 65280 is 'Permission Denied'
    while _jump_connect(users.popleft(), ssh_instance, jump_server, args) == 65280 and len(users):
        time.sleep(1)
    return True


def _jump_connect(user: str, ssh_instance: object, jump_server: object, args: argparse.Namespace) -> int:
    """
    :param user: <class 'str'>
    :param ssh_instance: <class 'boto3.resources.factory.ec2.Instance'> objects
        e.g.: ec2.Instance(id='i-0b4e31bc0b')
    :param jump_server:<class 'boto3.resources.factory.ec2.Instance'> objects
        e.g.: ec2.Instance(id='i-0b4e31bc0b')
    :param args: <class 'argparse.Namespace'>
        e.g.: ec2.Instance(id='i-0b4e31bc0b')
    :return:  <class 'int'> system(command) std out  int result
    """
    if '/' in user:
        users = user.split('/')
        command_dict = {
            'key_path': get_key_path(args, jump_server),
            'tunnel': get_tunnel(args),
            'jump_host': "{}@{}".format(users[0], jump_server.public_ip_address),
            'target_host': "{}@{}".format(users[1], ssh_instance.private_ip_address),
            'timeout': args.timeout
        }
    else:
        command_dict = {
            'key_path': get_key_path(args, jump_server),
            'tunnel': get_tunnel(args),
            'jump_host': "{}@{}".format(user, jump_server.public_ip_address),
            'target_host': "{}@{}".format(user, ssh_instance.private_ip_address),
            'timeout': args.timeout
        }

    if command_dict['key_path']:
        command = 'ssh-add {key_path}; ' \
                  'ssh -A {tunnel} -o ConnectTimeout={timeout} ' \
                  '-J {jump_host} {target_host} '.format(**command_dict)
    else:
        command = 'ssh {tunnel} -o ConnectTimeout={timeout} ' \
                  '-J {jump_host} {target_host} '.format(**command_dict)

    if args.command:
        command = "{} -tt '{}'".format(command, args.command)

    print('\nTrying with user "{}".\nCommand: {}'.format(user, command))
    return system(command)


def get_tunnel(args: argparse.Namespace) -> str:
    """
    :param args: <class 'argparse.Namespace'>
    :return: <class 'str'> formatted string for ssh command
    """
    if not args.remote_host:
        return ''

    url = args.remote_host.split(':')
    if len(url) == 2:
        params = {'local_port': args.local_port or url[1], 'remote_host': url[0], 'remote_port': url[1]}
    elif len(url) == 3:
        params = {'local_port': url[0], 'remote_host': url[1], 'remote_port': url[2]}
    else:
        if not args.local_port:
            args.local_port = args.remote_port
        params = args.__dict__
    return "-L '{local_port}:{remote_host}:{remote_port}'".format(**params)


def get_details(instance: object) -> dict:
    """
    :param instance: <class 'boto3.resources.factory.ec2.Instance'> objects
        e.g.: ec2.Instance(id='i-0b4e31bc0b')
    :return: <class 'dict'> dictionary with selected ec2.Instance properties
    """
    try:
        key_name = instance.key_name.replace(" ", "_")
        launch_time = instance.launch_time.isoformat()
    except AttributeError:
        key_name = instance.key_name
        launch_time = instance.launch_time

    details = {
        'id': instance.id,
        'name': get_name(instance),
        'type': instance.instance_type,
        'private_ip_address': str(instance.private_ip_address),
        'public_ip_address': str(instance.public_ip_address),
        'availability_zone': instance.placement.get('AvailabilityZone'),
        'security_groups': instance.security_groups,
        'state': instance.state.get('Name'),
        'launch time': launch_time,
        'block devices': get_device_mappings(instance),
        'key_name': key_name
    }

    return details


def get_key_path(args: argparse.Namespace, instance: object) -> str:
    """
    :param args: <class 'argparse.Namespace'>
    :param instance: <class 'boto3.resources.factory.ec2.Instance'> objects
        e.g.: ec2.Instance(id='i-0b4e31bc0b')
    :return:
    """
    if args.key_path:
        return args.key_path
    else:
        try:
            directory = path.expanduser(args.keys)
            return path.join(directory, instance.key_name.replace(" ", "") + '.pem')
        except AttributeError:
            return None


def get_device_mappings(instance: object) -> list:
    """
    :param instance: <class 'boto3.resources.factory.ec2.Instance'> objects
        e.g.: ec2.Instance(id='i-0b4e31bc0b')
    :return:
    """
    return flatten([device.values() for device in instance.block_device_mappings])


def flatten(array: list):
    list(itertools.chain.from_iterable(array))


def get_name(instance: object) -> str:
    """
    :param instance: <class 'boto3.resources.factory.ec2.Instance'> objects
    :return:
    """
    name: [dict] = [tag for tag in instance.tags if tag['Key'] == 'Name']
    if not name or 'Value' not in name[0]:
        return 'not-named'
    return name[0].get('Value')


def get_instances(args: argparse.Namespace) -> list:
    """
    :param args: <class 'argparse.Namespace'>
    Simple object for storing attributes. Implements equality by attribute names and values,
    and provides a simple string representation.
    :return: list of objects <class 'boto3.resources.factory.ec2.Instance'>
    """
    # AWS_ACCESS_KEY_ID - Specifies an AWS access key associated with an IAM user or role.
    # AWS_SECRET_ACCESS_KEY - Specifies the secret key associated with the access key.
    #                         This is essentially the "password" for the access key.
    # AWS_SESSION_TOKEN – Specifies the session token value that is required if you are using temporary security
    #                     credentials. For more information, see the Output section of the assume-role command in
    #                     the AWS CLI Command Reference.
    # AWS_DEFAULT_REGION – Specifies the AWS Region to send the request to.
    # AWS_DEFAULT_OUTPUT – Specifies the output format to use.
    # AWS_DEFAULT_PROFILE – Specifies the name of the CLI profile with the credentials and options to use.
    #                       This can be the name of a profile stored in a credentials or config file, or the value
    #                       default to use the default profile. If you specify this environment variable,
    #                       it overrides the behavior of using the profile named [default] in the configuration file.
    # AWS_CA_BUNDLE – Specifies the path to a certificate bundle to use for HTTPS certificate validation.
    # AWS_SHARED_CREDENTIALS_FILE – Specifies the location of the file that the AWS CLI uses to store access keys
    #                               (the default is ~/.aws/credentials).
    # AWS_CONFIG_FILE - Specifies the location of the file that the AWS CLI uses to store configuration profiles
    #                   (the default is ~/.aws/config).
    #

    # The "env" values (e.g. `export AWS_DEFAULT_REGION='us-east-2'`) are read by boto3.resource('ec2')
    # except for AWS_DEFAULT_PROFILE, which needs to be read by the utility:
    aws_default_profile = getenv('AWS_DEFAULT_PROFILE')

    if args.profile:
        boto3.setup_default_session(profile_name=args.profile)
    elif aws_default_profile:
        boto3.setup_default_session(profile_name=aws_default_profile)

    # If user uses MFA:
    if args.token_code and args.serial_number:
        client = boto3.client('sts')
        sts_response = client.get_session_token(SerialNumber=args.serial_number, TokenCode=args.token_code)
        if args.verbose:
            print('\nMFA:')
            pprint(sts_response)
            print('\n')

        sts_access_key_id = sts_response['Credentials']['AccessKeyId']
        sts_secret_access_key = sts_response['Credentials']['SecretAccessKey']
        sts_session_token = sts_response['Credentials']['SessionToken']

        # The AWS shared credentials file has a default location of ~/.aws/credentials.
        # However, the user may have changed the location of the shared credentials file
        # by setting the AWS_SHARED_CREDENTIALS_FILE environment variable.
        aws_shared_credentials_file = getenv('AWS_SHARED_CREDENTIALS_FILE')

        config = configparser.ConfigParser()
        # MFA profile section
        config['mfa'] = {'aws_access_key_id': sts_access_key_id,
                         'aws_secret_access_key': sts_secret_access_key,
                         'aws_session_token': sts_session_token,
                         }

        # Save user MFA credentials under his profiles' file [mfa] section:
        if aws_shared_credentials_file:
            config.read(aws_shared_credentials_file)
        else:
            aws_shared_credentials_file = config.read(getenv('HOME') + '/.aws/credentials')[0]

        config.set('mfa', 'aws_access_key_id', sts_access_key_id)
        config.set('mfa', 'aws_secret_access_key', sts_secret_access_key)
        config.set('mfa', 'aws_session_token', sts_session_token)

        with open(aws_shared_credentials_file + '.temp', 'w') as configfile:
            config.write(configfile)

        rename(aws_shared_credentials_file, aws_shared_credentials_file + ".BAK")
        rename(aws_shared_credentials_file + '.temp', aws_shared_credentials_file)

        if args.region == 'default':  # default='default' was set by parser if none given
            ec2 = boto3.resource('ec2', aws_access_key_id=sts_access_key_id,
                                 aws_secret_access_key=sts_secret_access_key, aws_session_token=sts_session_token)
        else:
            ec2 = boto3.resource('ec2', region_name=args.region, aws_access_key_id=sts_access_key_id,
                                 aws_secret_access_key=sts_secret_access_key, aws_session_token=sts_session_token)
    else:

        if args.region == 'default':  # default='default' was set by parser if none given
            ec2 = boto3.resource('ec2')  # uses value found in AWS_DEFAULT_REGION or ~/.aws/config file
        else:
            ec2 = boto3.resource('ec2', region_name=args.region)

    filters = [
        {'Name': 'tag:Name', 'Values': ['*{filter}*'.format(**args.__dict__)]},
        {'Name': 'instance-state-name', 'Values': ['running']},

    ]
    # Filter out Windows and then remove these instances.
    filter_windows = [
        {'Name': 'tag:Name', 'Values': ['*{filter}*'.format(**args.__dict__)]},
        {'Name': 'instance-state-name', 'Values': ['running']},
        {'Name': 'platform', 'Values': ['windows']},
    ]

    all_platform_instances = list(ec2.instances.filter(Filters=filters))
    windows_platform_instances = list(ec2.instances.filter(Filters=filter_windows))

    for windows_instance in windows_platform_instances:
        all_platform_instances.remove(windows_instance)

    # return sorted(ec2.instances.filter(Filters=filters), key=get_name)
    return sorted(all_platform_instances, key=get_name)


def main():
    parser = create_parser()
    args = parser.parse_args()

    # MFA needs these two (mutually inclusive) arguments
    if args.serial_number or args.token_code:
        if not args.serial_number or not args.token_code:
            parser.error("MFA: --serial-number requires --token-code and vice versa.")

    if args.version:
        print(VERSION)
        exit(0)

    try:
        instances: list = get_instances(args)
    except(exceptions.EndpointConnectionError, ValueError):
        print('"{}" is an invalid Region.'.format(args.region))
        exit(0)
    except exceptions.ProfileNotFound:
        print('The config profile "{}" could not be found.\n'
              'To properly configure your AWS Profiles visit:\n'
              'https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html'.format(args.profile))
        exit(0)
    except exceptions.NoCredentialsError:
        print('Unable to locate your AWS credentials file.\n'
              'To properly configure your AWS Credentials, run `aws configure`:\n'
              'https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration')
        exit(0)
    except exceptions.ClientError:
        print('An error occurred (UnauthorizedOperation).\n'
              'You are not authorized to perform this operation.\n'
              'Contact your AWS Administrator or enable MFA in your account.')
        exit(0)

    except exceptions.ParamValidationError:
        print('Parameter validation failed: \n'
              'Invalid length for parameter TokenCode.')
        exit(0)

    if sys.stdin.isatty():
        print('EC2 instances in {region} region:\n'.format(**args.__dict__))
        display_instances(instances)

    if not instances:
        print('No running instances found.\n')
        exit(1)

    if len(instances) == 1:
        if instances[0].public_ip_address:
            print('Found one running instance and connecting to it...\n')
            connect(instances[0], args)
        else:
            print("The instance found has no public IP address.\n")
    else:
        select_instance(args, instances)


def display_instances(instances: list):
    """
    :param instances: list of objects <class 'boto3.resources.factory.ec2.Instance'>
        e.g.: [ec2.Instance(id='i-0b4e31bc0b'), ec2.Instance(id='i-0f5e60ce9f')]
    :return:
    """
    table_col_names = ['Name', 'Public IP', 'Private IP', 'Zone', 'Key Name']
    print("     {:<30}{:<17}{:<17}{:<14}{}".format(*table_col_names))

    details_fmt = "{:2} - {name:<30}{public_ip_address:<17}" \
                  "{private_ip_address:<17}{availability_zone:<14}{key_name}"

    for i, instance in enumerate(instances, 1):
        print(details_fmt.format(i, **get_details(instance)))
    print('')


def select_instance(args: argparse.Namespace, instances: list):
    """
    :param args: <class 'argparse.Namespace'> simple object for storing attributes
    :param instances: <class 'list'>
    List of <class 'boto3.resources.factory.ec2.Instance'> objects
        e.g.: [ec2.Instance(id='i-0b4e31bc0b'), ec2.Instance(id='i-0f5e60ce9f')]
    :return:
    """

    connection = False
    try:
        if sys.stdin.isatty():
            server_selection = [int(x) for x in six.moves.input("Enter server number: ").split()]  # User selection
        else:
            server_selection = [int(x) for x in six.moves.input().split()]

        if len(server_selection) == 1:
            server_selection[0] = server_selection[0] - 1  # server selection numbers start at 1, shift to match index
            if instances[server_selection[0]].public_ip_address is None:
                for instance in instances:
                    if instance.key_name == instances[server_selection[0]].key_name:
                        if instance.public_ip_address is not None:
                            # ssh_instance, jump_server, args
                            if jump_connect(instances[server_selection[0]], instance, args):
                                connection = True
                                break

                if connection:
                    exit(0)
                else:
                    print("No jump servers with the same 'Key Name' were found.\n"
                          "You can input two instances to jump from <a> to <b>.\n"
                          "e.g.:\n"
                          "\tEnter server number: {} {}\n".format((server_selection[0] + 5),
                                                                  server_selection[0]))
            else:
                connect(instances[server_selection[0]], args)
        elif len(server_selection) == 2:
            # server_selection[0] -- jump server
            # server_selection[1] -- target server
            server_selection[0] = server_selection[0] - 1  # server selection options start with 1, not 0
            server_selection[1] = server_selection[1] - 1  # server selection options start with 1, not 0
            if instances[server_selection[0]].public_ip_address is None:
                print("The provided jump server has no public IP address.\n"
                      "You can input two instances to jump from a to b.\n"
                      "However, the jump server needs to be reachable.\n"
                      "e.g.:\n"
                      "\tEnter server number: {} {}\n".format((server_selection[0] + 5), server_selection[0]))
                exit(0)
            else:
                jump_connect(instances[server_selection[1]], instances[server_selection[0]], args)
        else:
            print('Invalid number of instances.\n')
            exit(0)

    except (ValueError, IndexError):
        print('Invalid instance.\n')

    except (EOFError, KeyboardInterrupt, SyntaxError):
        exit(0)


def get_private_key(args: object, environment: int = 'prod') -> object:
    region = args.region
    secret_name = f'/{environment}/ssh'
    client = boto3.client('secretsmanager', region_name='{}'.format(region))

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    else:
        secret = get_secret_value_response['SecretString']

        secret_dict = json.loads(secret)
        private_key = secret_dict['PrivateKey']

        return private_key


def create_parser() -> argparse.ArgumentParser:
    """
    :return: class 'argparse.ArgumentParser'
    """
    parser = argparse.ArgumentParser(description="""
                                        SSH, 'ProxyJump', create tunnels, and run commands on your AWS Linux/Unix
                                        infrastructure. "awssh --profile prod-acc-2 --region us-east-2 'rev-proxy' -c
                                        top --users fduran" "awssh --profile prod-acc-2" will attempt ssh with default
                                        users. The default user list is centos, ubuntu, and ec2-user. Due to the
                                        nature of nargs, the option --users needs to be used last. For example: "awssh
                                        --users user1 user2 'rev-proxy'" will not properly filter the results by
                                        'instance-name'; instead try "awssh 'rev-proxy' --users user1 user2". To use
                                        two different users on proxy jump try: --users user1/user2. When the instance
                                        selected has no external IP, a "JumpHost" will be automatically chosen based
                                        on instances with external IPs that share the same ssh 'Key Name'. This is
                                        particularly useful if your project instances share the same 'SSH Key'. You
                                        can also explicitly direct the JumpHost by providing two selections from the
                                        list (i.e. Enter server number: <jump> <target>). MFA: when providing the
                                        --serial-number and --token-code options, awssh creates a profile [mfa] in
                                        your AWS credentials file (~/.aws/credentials or the file set by the
                                        AWS_SHARED_CREDENTIALS_FILE environment variable). You can continue using
                                        these temporary tokens until expiration with "awssh --profile mfa".
                                        """)

    parser.add_argument('filter', nargs='?', default='*', help='Optional instance name or key word as a filter. '
                                                               'If only one instance is found, it will connect to it '
                                                               'directly.')
    parser.add_argument('--users', nargs='+', help='Users to try (centos, ubuntu, and ec2-user are defaults). '
                                                   'To use two different users on proxy jump try: --user user1/user2.',
                        default=['centos', 'ubuntu', 'ec2-user'])
    parser.add_argument('--profile', help='Use a specific profile from your credentials file.')
    parser.add_argument('--region', help='AWS region (User default if none is provided).', default='default')
    parser.add_argument('-i', '--key-path', help='Absolute key path, overrides, --keys.')
    parser.add_argument('-c', '--command', help="Translates to 'ssh -tt <user>@<ip> <command>'. ")
    parser.add_argument('-r', '--remote-host',
                        help="Open a tunnel. Equivalent to "
                             "'ssh -L <local-port>:<remote-host>:<remote-port> <selected-aws-host>'. ")
    parser.add_argument('-p', '--remote-port', help='Port to use on the remote host (default is 5432).', default=5432)
    parser.add_argument('-l', '--local-port',
                        help='Port to use on the local host. Get overwritten by remote port if not defined.')
    parser.add_argument('--keys', help='Directory of the private keys (~/.ssh by default).', default='~/.ssh/')
    parser.add_argument('--timeout', help='SSH connection timeout.', default='5')
    parser.add_argument('--console-output', '-o', help='Display the instance console out before logging in.',
                        action='store_true')
    parser.add_argument('--version', '-v', help='Returns awssh\'s version.', action='store_true')
    parser.add_argument('--verbose', '-V', help='Prints instance details, login details, as well as MFA details.',
                        action='store_true')

    mfa_group = parser.add_argument_group(title='MFA', description="If MFA is required, provide both '--serial-number' "
                                                                   "and '--token-code'. Credentials are saved under "
                                                                   "[mfa] profile for valid use until expiration.")
    mfa_group.add_argument('--serial-number', help='The identification number of the MFA device that is associated '
                                                   'with the IAM user. Specify this value if the IAM user has a policy '
                                                   'that requires MFA authentication. You can find the device for an '
                                                   'IAM user viewing the user\'s security credentials.')
    mfa_group.add_argument('--token-code', help='The value provided by the MFA device, if MFA is required. If any '
                                                'policy requires the IAM user to submit an MFA code, specify this '
                                                'value. If MFA authentication is required, the user must provide a '
                                                'code when requesting a set of temporary security credentials. A user '
                                                'who fails to provide the code receives an "access denied" response '
                                                'when requesting resources that require MFA authentication.')

    return parser


if __name__ == '__main__':
    main()
