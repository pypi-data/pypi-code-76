"""
FASTGenomics Base Library
"""

__copyright__ = "Copyright, Comma Soft AG"
__version__ = "0.2.0"
__maintainer__ = "Ralf Karle"
__email__ = "ralf.karle@comma-soft.com"

import base64
import datetime
import hashlib
import json
import logging
import string
import subprocess
import time
from enum import Enum
from logging import exception
from os import path, makedirs, environ, remove
from random import choice
from subprocess import CompletedProcess
from typing import List, Union
from urllib.parse import urlparse

import requests
from requests.adapters import Retry
from requests.exceptions import HTTPError
from requests.sessions import HTTPAdapter
from tqdm import tqdm

FG_CLI_VERSION = __version__
user_agent = f"fg-cli/{FG_CLI_VERSION}"

PSEUDOMIZE_EMAIL_ADDRESSES = True
AWS_ACCOUNT_CREATION_WAIT_TIME = 10  # wait for 10 sec

logger = logging.getLogger(__name__)
log_level = logging.WARN


def get_homedir() -> str:
    """ get the homedir """
    return path.normpath(
        path.expanduser("~/.fgcli"))


def run_zip(files_or_directory: List[str], zip_filename, zip_password: str) -> str:
    """ zip all files in a directory and protect the zip with a password

    """

    configuration = ToolConfiguration()
    configuration.load()

    zip_filename = path.abspath(path.expanduser(zip_filename))

    if path.exists(zip_filename):
        raise Exception(f"Zipfile '{zip_filename}' already does exist.")

    sevenZip = configuration.sevenzip_path
    if sevenZip == "":
        sevenZip = "7z"

    params = [
        sevenZip,
        "a",
        zip_filename
    ]
    for file in files_or_directory:
        params.append(file)
    params.append(f"-p{zip_password}")
    params.append("-y")
    params.append("-r")
    params.append("-w")

    if len(configuration.sevenzip_additional_cli_options) > 0:
        for o in configuration.sevenzip_additional_cli_options:
            params.append(o)

    logger.info(
        f"{' '.join(params)}")
    subprocess.run(params, shell=False, check=True)

    return zip_filename


class FASTGenomicsAccount:
    """ a fastgenomics account data """

    def __init__(self):
        """ constructs a fastgenomics account """
        self.fastgenomics_url = ""
        self.fastgenomics_user = ""
        self.fastgenomics_passphrase = ""
        self.fastgenomics_login_method = ""

    def to_json(self):
        """ converts the account to json """
        return json.dumps(self, default=lambda o: o.__dict__)

    def from_json(self, json_data: str):
        """ constructs the account from json """
        d = json.loads(json_data)
        self.__dict__ = d


class ToolConfiguration:
    """ the tool configuration """

    def __init__(self):
        """  constructs a tool configuration """
        self.lfs_vault_directory: str = ""

        self.azcopy_path: str = ""
        self.azcopy_additional_cli_options: str = ""
        self.awscli_path: str = ""
        self.awscli_additional_cli_options: str = ""
        self.sevenzip_path: str = ""
        self.sevenzip_additional_cli_options: str = ""

    @staticmethod
    def get_filename() -> str:
        """ get the file name of the configuration file """
        return path.join(get_homedir(), "config.json")

    @staticmethod
    def ensure_config_json():
        """ ensure there is a default config.json """
        homedir = get_homedir()
        if not path.exists(homedir):
            makedirs(homedir)

        filename = ToolConfiguration.get_filename()
        if path.exists(filename):
            return None

        paths = {}
        tools = {}

        azcopy = {"path": "", "additional_cli_options": []}
        tools["azcopy"] = azcopy

        awscli = {"path": "", "additional_cli_options": ["--sse"]}
        tools["awscli"] = awscli

        seven_zip = {"path": "", "additional_cli_options": ["-m0=LZMA2:d64k:fb32",
                                                            "-ms=8m",
                                                            "-mmt=30",
                                                            "-mx=1"
                                                            ]}
        tools["7z"] = seven_zip

        paths["lfs_vault_directory"] = path.join(get_homedir(), "lfs-vault")

        c = {
            "paths": paths,
            "tools": tools
        }

        j = json.dumps(c, indent=4)

        with open(filename, 'w') as f:
            f.write(j)

    def load(self):
        """ load the config """
        filename = path.join(get_homedir(), "config.json")

        if not path.exists(filename):
            logger.info(f"creating empty configuration file '{filename}'")
            ToolConfiguration.ensure_config_json()

        logger.info(f"load configuration file '{filename}'")

        if not path.exists(filename):
            raise Exception(f"Configuration file '{filename}' not found.")
        with open(filename, 'r') as f:
            data = f.read()

        obj = json.loads(data)

        paths = obj["paths"]
        tools = obj["tools"]

        self.lfs_vault_directory = paths["lfs_vault_directory"]

        self.azcopy_path = tools["azcopy"].get("path", "")
        self.azcopy_additional_cli_options = tools["azcopy"].get(
            "additional_cli_options", [])

        self.awscli_path = tools["awscli"].get("path", "")
        self.awscli_additional_cli_options = tools["awscli"].get(
            "additional_cli_options", [])

        self.sevenzip_path = tools["7z"].get("path", "")
        self.sevenzip_additional_cli_options = tools["7z"].get(
            "additional_cli_options", [])


class LargeFileStorageAccessInformation:
    """ access information of a large file storage """

    def __init__(self, upload_user_id: str, storage_id: str, title: str, download_uri: str, download_account: dict,
                 user_accesstoken: str, upload_uri: str, upload_account: dict, created_at_utc: datetime,
                 expires_on_utc: datetime, provider_type: str) -> None:
        self.upload_user_id: str = upload_user_id
        self.storage_id: str = storage_id
        self.title: str = title
        self.provider_type: str = provider_type
        self.download_uri: str = download_uri
        self.download_account: dict = download_account
        self.user_accesstoken: str = user_accesstoken
        self.upload_uri: str = upload_uri
        self.upload_account: dict = upload_account
        self.created_at_utc: datetime = created_at_utc
        self.expires_on_utc: datetime = expires_on_utc


class LargeFileStorageInformation:
    """ general information of a large file storage """

    def __init__(self, storage_id: str, title: str, created_at_utc: datetime, expires_on_utc: datetime, dataset_id: str,
                 provider_type: str) -> None:
        self.storage_id: str = storage_id
        self.title: str = title
        self.createdAtUtc: str = created_at_utc
        self.expiresOnUtc: str = expires_on_utc
        self.dataset_id: str = dataset_id
        self.provider_type: str = provider_type


class LargeFileStorageState(Enum):
    """ the states of a large file storage """
    ERROR = 0x0,
    UPLOADING = 0x1,
    READY = 0x100


class FASTGenomicsClient:
    """ the FASTGenomics Client """

    def __init__(self):
        """ constructs a the FASTGenomics client """
        self.session = requests.Session()
        retry = Retry(total=5,
                      read=5,
                      connect=5,
                      backoff_factor=0.3
                      )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.fastgenomics_account = None
        self.configuration = None

    def _aws_run_cli_command(self, arguments: List[str], aws_account: Union[dict, None] = None,
                             capture_output: bool = False, check=True) -> CompletedProcess:
        """ run a aws cli command """
        configuration = self._get_configuration()

        my_env = environ.copy()

        if aws_account is not None and len(aws_account) > 0:
            my_env['AWS_ACCESS_KEY_ID'] = aws_account['awsAccessKeyId']
            my_env['AWS_SECRET_ACCESS_KEY'] = aws_account['awsSecretAccessKey']
            my_env['AWS_DEFAULT_REGION'] = aws_account['awsRegion']

        aws = "aws"
        if configuration.awscli_path != "":
            aws = configuration.awscli_path

        params = [aws]
        for a in arguments:
            params.append(a)

        logger.debug(
            f"{' '.join(params)}")

        try:

            if capture_output:
                result = subprocess.run(
                    params, shell=False, check=check, env=my_env, stdout=subprocess.PIPE, universal_newlines=True)
            else:
                result = subprocess.run(
                    params, shell=False, check=check, env=my_env)

        except IOError as err:
            if err.errno == 2:
                if aws == "aws":
                    logger.error(
                        f"Failed to run aws cli tool '{aws}': You may have to install aws cli tool or validate the "
                        f"configuration file '{ToolConfiguration.get_filename()}'")
                else:
                    logger.error(
                        f"Failed to run aws cli tool '{aws}': You may have to install aws cli tool and edit the path "
                        f"in the configuration file '{ToolConfiguration.get_filename()}")
            else:
                logger.error(f"Failed to run aws cli tool '{aws}': {err}")
            raise
        except Exception as err:
            logger.error(f"Failed to run aws cli tool '{aws}': {err}")
            raise

        return result

    def _get_aws_region(self) -> str:
        """ get the AWS region using AWS cli """
        process = self._aws_run_cli_command(
            ["configure", "get", "region"], None, check=False, capture_output=True)
        if process.returncode != 0:
            raise Exception("Failed to AWS region")

        region: str = process.stdout
        return region.strip()

    def _aws_create_account(self, user_name: str, aws_path: str) -> str:
        """ create a IAM account in AWS """
        region = self._get_aws_region()
        assert region != "", "No AWS region found. Please check AWS configuration."

        configuration = self._get_configuration()

        org_user_name = user_name.lower()
        if PSEUDOMIZE_EMAIL_ADDRESSES:
            user_name = "fg-" + \
                        FASTGenomicsClient._pseudomize_email_address(user_name)
        else:
            user_name = "fg-" + user_name.lower()

        logger.info(
            f"getting AWS user '{user_name}' known as '{org_user_name}'")
        process = self._aws_run_cli_command(
            ["iam", "get-user", "--user-name", user_name], None, check=False, capture_output=True)
        if process.returncode == 0:
            user_info = json.loads(process.stdout)
            return user_info['User']['Arn']

        if process.returncode != 254:  # not found
            raise Exception(f"Failed to get AWS user '{org_user_name}'")

        if not aws_path.startswith("/"):
            aws_path = "/" + aws_path
        if not aws_path.endswith("/"):
            aws_path = aws_path + "/"

        logger.info(
            f"creating AWS user '{user_name}' known as '{org_user_name}'")
        process = self._aws_run_cli_command(
            ["iam", "create-user", "--path", aws_path, "--user-name", user_name], None, capture_output=True, check=True)
        logger.debug(process.stdout)
        user_info = json.loads(process.stdout)

        logger.info(
            f"creating access keys for AWS user '{user_name}' known as '{org_user_name}'")
        process = self._aws_run_cli_command(
            ["iam", "create-access-key", "--user-name", user_name], None, capture_output=True, check=True)

        logger.debug(process.stdout)
        accessKey = json.loads(process.stdout)

        account = {
            "email": org_user_name,
            "awsAccessKeyId": accessKey['AccessKey']['AccessKeyId'],
            "awsSecretAccessKey": accessKey['AccessKey']['SecretAccessKey'],
            "awsRegion": region,
            "awsArn": user_info['User']['Arn'],
            "awsUserName": user_info['User']['UserName']
        }

        json_filename = path.join(
            configuration.lfs_vault_directory, "aws-account-" + org_user_name + ".json")

        logger.info(
            f"storing account information of {user_name} in '{json_filename}'")

        with open(json_filename, 'w') as f:
            f.write(json.dumps(account, indent=4))

        logger.info("waiting for user account to propegate")
        # the just create user can not be used directly because it needs to propegate through AWS services
        # so we just check to get the user and wait a little while
        time.sleep(AWS_ACCOUNT_CREATION_WAIT_TIME)

        self._aws_run_cli_command(
            ["iam", "get-user", "--user-name", user_name], None, check=True, capture_output=True)

        return user_info['User']['Arn']

    def aws_configure_cloud(self) -> dict:
        """
        configure the AWS Cloud

        * create a IAM User 'FASTGenomics-ServicePrincipal' as Service Prinicpal for FG Backend
        * create a Managed Policy to 'FASTGenomics-S3Bucket-Read-Write-Policy' as policy for this user

        returns:
        {
            "awsAccessKeyId": "xxxxd",
            "awsSecretAccessKey": "yyyyy"
        }
        """
        account = self._get_fastgenomics_account()

        aws_path = urlparse(account.fastgenomics_url).hostname
        if not aws_path.startswith("/"):
            aws_path = "/" + aws_path
        if not aws_path.endswith("/"):
            aws_path = aws_path + "/"

        configuration = self._get_configuration()

        user_name = "FASTGenomics-ServicePrincipal"
        policy_name = "FASTGenomics-S3Bucket-Read-Write-Policy"
        logger.info(
            f"creating AWS user '{user_name}'")
        process = self._aws_run_cli_command(
            ["iam", "create-user", "--path", aws_path, "--user-name", user_name], None, capture_output=True, check=True)
        logger.debug(process.stdout)
        user_info = json.loads(process.stdout)

        logger.info(
            f"creating Access Keys for '{user_name}'")
        process = self._aws_run_cli_command(
            ["iam", "create-access-key", "--user-name", user_name], None, capture_output=True, check=True)

        logger.debug(process.stdout)
        accessKey = json.loads(process.stdout)
        awsAccessKeyId = accessKey['AccessKey']['AccessKeyId']
        awsSecretAccessKey = accessKey['AccessKey']['SecretAccessKey']

        json_filename = path.join(
            configuration.lfs_vault_directory, "aws-account-" + user_name + ".json")

        logger.info(
            f"storing account information of {user_name} in '{json_filename}'")
        with open(json_filename, 'w') as f:
            f.write(json.dumps(process.stdout, indent=4))

        statements = []
        s = {
            "Sid": "ObjectManagement",
            "Effect": "Allow",
            "Action": ["s3:GetObject",
                       "s3:GetObjectVersion",
                       "s3:DeleteObjectVersion",
                       "s3:DeleteObject"
                       ],
            "Resource": "arn:aws:s3:::*/*"
        }
        statements.append(s)
        s = {
            "Sid": "BucketManagement",
            "Effect": "Allow",
            "Action": ["s3:CreateBucket",
                       "s3:DeleteBucket",
                       "s3:ListBucket",
                       "s3:GetBucketPolicy",
                       "s3:PutBucketPolicy"
                       ],
            "Resource": "arn:aws:s3:::*"
        }
        statements.append(s)

        policy = {
            "Version": "2012-10-17",
            "Statement": statements
        }

        policy_doc = json.dumps(policy)

        logger.info(
            f"creating policy for limit access to s3 buckets")
        process = self._aws_run_cli_command(
            ["iam", "create-policy", "--policy-name", policy_name, "--policy-document", policy_doc, "--description",
             "Policy for FASTGenomics Access to manage S3 buckets", "--path", aws_path], None, capture_output=True,
            check=True)
        logger.debug(process.stdout)
        policy = json.loads(process.stdout)
        policy_arn = policy["Policy"]["Arn"]

        logger.info(
            f"attaching policy '{policy_name}' to user {user_name}")
        process = self._aws_run_cli_command(
            ["iam", "attach-user-policy", "--user-name",
                user_name, "--policy-arn", policy_arn], None,
            capture_output=True, check=True)

        r = {
            "awsAccessKeyId": awsAccessKeyId,
            "awsSecretAccessKey": awsSecretAccessKey
        }
        return r

    @staticmethod
    def _pseudomize_email_address(email_address):
        """ pseudomize the normalized email address """
        emailhash = hashlib.sha256(
            email_address.lower().encode('utf-8')).digest()
        return base64.urlsafe_b64encode(emailhash).decode("utf-8").rstrip("=")

    @staticmethod
    def generate_password() -> str:
        """ generate a password """
        characters = string.ascii_letters + string.digits + "()+-.,#!$§%&"
        password = "".join(choice(characters) for x in range(32))
        return password

    @staticmethod
    def set_log_level(level):
        """ set the loglevel """
        global log_level
        log_level = level
        log_format = '[%(asctime)s] - %(message)s'
        logging.basicConfig(level=log_level, format=log_format)

    @staticmethod
    def version():
        """ get the version """
        return {
            "fg.py": f"{FG_CLI_VERSION}"
        }

    def _get_bearer_token(self) -> str:
        """ get a bearer token """
        account = self._get_fastgenomics_account()
        try:
            headers = {'Content-type': 'application/json',
                       'Accept': 'application/json',
                       'User-Agent': user_agent}

            if account.fastgenomics_login_method == "pat":
                url = self._get_url("ids/api/v1/token/pat")

                request_data = {
                    "email": account.fastgenomics_user,
                    "personalAccessToken": account.fastgenomics_passphrase
                }

                request_json = json.dumps(request_data)

                response = self.session.post(
                    url, data=request_json, headers=headers)
                self._handle_response(response)
                jsonResponse = response.json()
            else:
                url = self._get_url("ids/api/v1/token/resourceowner")

                request_data = {
                    "email": account.fastgenomics_user,
                    "password": account.fastgenomics_passphrase
                }

                request_json = json.dumps(request_data)

                response = self.session.post(
                    url, data=request_json, headers=headers)
                self._handle_response(response)
                jsonResponse = response.json()
        except HTTPError as http_err:
            raise Exception(
                f"Failed to retrieve access_token ({account.fastgenomics_login_method}): {http_err}")
        except Exception as err:
            raise Exception(
                f"Failed to retrieve access_token ({account.fastgenomics_login_method}): {err}")

        return jsonResponse['accessToken']

    def _handle_response(self, response: requests.Response):
        """ handle a response """
        if response.status_code == 200:
            return

        response_text = response.text.strip("\"")
        message = response_text
        try:
            if response_text != "":
                if response_text.startswith("{"):
                    apiError = response.json()
                    if apiError is not None:
                        if 'message' in apiError:
                            message = apiError['message']
                        elif 'detail' in apiError:
                            message = apiError['Detail']
                        else:
                            message = response_text
                    else:
                        message = response_text
                if response_text.startswith("<"):
                    message = response_text

        except:
            response.raise_for_status()

        raise IOError(f"{message} - status {response.status_code}")

    @staticmethod
    def _get_cli_profile_path() -> str:
        """ get the cli profile path """
        return path.normpath(get_homedir())

    @staticmethod
    def __get_credentials_filename():
        """ get the filename of the credentials.json """
        filename = path.join(
            FASTGenomicsClient._get_cli_profile_path(), "credentials.json")
        return filename

    def _get_configuration(self) -> ToolConfiguration:
        """ get the tool configuration """
        if self.configuration is not None:
            return self.configuration
        try:
            self.configuration = ToolConfiguration()
            self.configuration.load()

            if not path.exists(self.configuration.lfs_vault_directory):
                makedirs(self.configuration.lfs_vault_directory)
        except:
            logger.error("Failed to load configuration")
            raise

        return self.configuration

    def _get_fastgenomics_account(self) -> FASTGenomicsAccount:
        """ get the FASTGenomics account """
        if self.fastgenomics_account is not None:
            return self.fastgenomics_account

        filename = FASTGenomicsClient.__get_credentials_filename()
        logger.debug(f"Reading account file {filename}'")
        if not path.exists(filename):
            raise Exception(
                "You are not logged in! Please login using 'fg login'")

        with open(filename, 'r') as f:
            data = f.read()
        account = FASTGenomicsAccount()
        self.fastgenomics_account = account.from_json(data)
        return account

    def login(self, user: str, passphrase: str, login_method: str = "pat", url: str = "https://beta.fastgenomics.org"):
        """ login to FASTGenomics and store credentials in users profile

        Parameters:
        -----------
        user         : the FASTGenomics user name
        passphrase   : if login_method is "pat" the personal access token (pat) else the password of the use
        login_method : pat | password
        url          : the url of the plattform
        """
        directory = FASTGenomicsClient._get_cli_profile_path()
        if not path.exists(directory):
            makedirs(directory)

        if login_method.lower() == "pat":
            login_method = "pat"
        else:
            login_method = "password"

        if not url.endswith("/"):
            url = url + "/"

        filename = FASTGenomicsClient.__get_credentials_filename()
        account = FASTGenomicsAccount()
        account.fastgenomics_url = url
        account.fastgenomics_user = user
        account.fastgenomics_passphrase = passphrase
        account.fastgenomics_login_method = login_method

        content = account.to_json()
        logger.info(f"Writing profile '{filename}'")
        with open(filename, 'w') as f:
            f.write(content)

        self.fastgenomics_account = account

        try:
            self._get_bearer_token()
        except Exception as err:
            self.logout()
            raise Exception(f"Log in failed!: {err}")

    def logout(self):
        """ logout from FASTGenomics and remove credentials file """
        filename = FASTGenomicsClient.__get_credentials_filename()
        if path.exists(filename):
            remove(filename)
        self.fastgenomics_account = None

    def is_logged_in(self) -> bool:
        try:
            self._get_fastgenomics_account()
        except:
            return False
        return True

    def _get_url(self, relative_url: str) -> str:
        """ get a absolute FASTGenomics url """
        if relative_url.startswith("/"):
            relative_url = relative_url[1:]
        return self._get_fastgenomics_account().fastgenomics_url + relative_url

    def get_dataset_details_url(self, dataset_id: str, tab: str) -> str:
        """ get the FASTGenomics url of dataset details tab """
        if tab == "":
            return self._get_url(f"datasets/detail-{dataset_id}")
        return self._get_url(f"datasets/detail-{dataset_id}#{tab}")


class FASTGenomicsLargeFileStorageClient(FASTGenomicsClient):
    """ the FASTGenomics Client for large file storage """

    def __init__(self):
        """ constructs the client """
        super().__init__()

    def __store_storage_access_information(self, sai: dict):
        """ store large file storage access information to vault """
        configuration = self._get_configuration()
        json_filename = path.join(
            configuration.lfs_vault_directory, sai['storageId'] + ".json")
        logger.info(f"storing accessinformation in file {json_filename}")
        with open(json_filename, 'w') as f:
            f.write(json.dumps(sai, indent=4))

    def __store_account(self, account: dict, email: str, provider_type: str):
        """ store an account to vault """
        if account is None or len(account) == 0:
            return

        configuration = self._get_configuration()
        email = email.lower()
        json_filename = path.join(
            configuration.lfs_vault_directory, f"{provider_type}-account-{email}.json")

        logger.info(
            f"storing account information of {email} in '{json_filename}'")

        with open(json_filename, 'w') as f:
            f.write(json.dumps(account, indent=4))

    def __get_stored_account(self, email: str, provider_type: str):
        """ get a stored account from vault """
        configuration = self._get_configuration()

        email = email.lower()
        json_filename = path.join(
            configuration.lfs_vault_directory, f"{provider_type}-account-{email}.json")
        if path.exists(json_filename):
            logger.info(
                f"reading upload account from file '{json_filename}'")
            with open(json_filename, 'r') as f:
                data = f.read()
            return json.loads(data)
        return None

    def __create_large_file_storage(self, provider_type: str, full_filename: str, title: str,
                                    recipientInformation: dict,
                                    uploaderinformation: dict) -> LargeFileStorageAccessInformation:
        """
        create a large file storage
        """

        filename = path.basename(full_filename)
        filesize = path.getsize(full_filename)

        logger.info(
            f"creating large file storage for file '{filename}'")

        try:
            bearer_token = self._get_bearer_token()

            url = self._get_url("webclient/api/lfs")

            recipient_email = recipientInformation['userEmail']
            logger.info(f"title            : {title}")
            logger.info(f"filename         : {filename}")
            logger.info(f"filesize         : {filesize}")
            logger.info(f"provider type    : {provider_type}")
            logger.info(
                f"recipient email  : {recipient_email}")

            request_data = {
                "title": title,
                "fileName": filename,
                "filesize": filesize,
                "providerType": provider_type,
                "recipientInformation": recipientInformation,
                "uploaderInformation": uploaderinformation
            }

            request_json = json.dumps(request_data)

            headers = {
                'Content-type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f"Bearer {bearer_token}",
                'User-Agent': user_agent
            }

            response = self.session.post(
                url, data=request_json, headers=headers)
            self._handle_response(response)
            sai = response.json()

            self.__store_storage_access_information(sai)
            self.__store_account(sai['uploadAccount'],
                                 self._get_fastgenomics_account().fastgenomics_user,
                                 provider_type)
            self.__store_account(sai['downloadAccount'], recipient_email,
                                 provider_type)

            storage_access_info = LargeFileStorageAccessInformation(
                sai['uploadUserId'],
                sai['storageId'],
                sai['title'],
                sai['downloadUri'],
                sai['downloadAccount'],
                sai['userAccessToken'],
                sai['uploadUri'],
                sai['uploadAccount'],
                sai['createdAtUtc'],
                sai['expiresOnUtc'],
                provider_type
            )

            logger.debug(
                f"created storage id: {storage_access_info.storage_id}")
            logger.debug(
                f"expires on utc    : {storage_access_info.expires_on_utc}")

        except HTTPError as http_err:
            raise Exception(f"Failed to create large file storage: {http_err}")
        except Exception as err:
            raise Exception(f"Failed to create large file storage: {err}")

        return storage_access_info

    def __update_state(self, sai: LargeFileStorageAccessInformation, state: LargeFileStorageState):
        """ update the state in database """

        if state == LargeFileStorageState.ERROR:
            logger.info(f"setting status of storage {sai.storage_id} to ERROR")
            url = self._get_url(
                f"webclient/api/lfs/{sai.storage_id}/state/Error")
        elif state == LargeFileStorageState.READY:
            logger.info(f"setting status of storage {sai.storage_id} to READY")
            url = self._get_url(
                f"webclient/api/lfs/{sai.storage_id}/state/Ready")
        else:
            raise exception(f"unknown state '{state}'")

        bearer_token = self._get_bearer_token()

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f"Bearer {bearer_token}",
            'User-Agent': user_agent
        }

        response = self.session.patch(url, headers=headers)
        self._handle_response(response)
        return

    def __upload_to_azure(self, sai: LargeFileStorageAccessInformation, full_filename: str):
        """ upload the file to Azure using azcopy """
        logger.info(
            f"uploading '{full_filename}' to azure storage with id '{sai.storage_id}'")

        configuration = self._get_configuration()

        azcopy = "azcopy"
        if configuration.azcopy_path != "":
            azcopy = configuration.azcopy_path

        params = [azcopy, "copy", full_filename,
                  sai.upload_uri]
        if len(configuration.azcopy_additional_cli_options) > 0:
            for o in configuration.azcopy_additional_cli_options:
                params.append(o)

        try:
            logger.info(
                f"{' '.join(params)}")
            subprocess.run(params, shell=False, check=True)
        except IOError as err:
            if err.errno == 2:
                if azcopy == "azcopy":
                    logger.error(
                        f"Failed to run azcopy '{azcopy}': You may have to install azcopy or validate the configuration file '{ToolConfiguration.get_filename()}'")
                else:
                    logger.error(
                        f"Failed to run azcopy '{azcopy}': You may have to install azcopy and edit the path in the configuration file '{ToolConfiguration.get_filename()}")
            else:
                logger.error(f"Failed to run azcopy tool '{azcopy}': {err}")
            raise
        except Exception as err:
            logger.error(f"Failed to run azcopy tool '{azcopy}': {err}")
            raise

        return

    def __upload_to_aws(self, sai: LargeFileStorageAccessInformation, full_filename: str):
        """ upload the file to AWS """
        logger.info(
            f"uploading '{full_filename}' to aws bucket with id '{sai.storage_id}'")

        my_env = environ.copy()

        account = sai.upload_account
        if sai.upload_account is None or len(sai.upload_account) == 0:
            account = self.__get_stored_account(
                self._get_fastgenomics_account().fastgenomics_user,
                sai.provider_type)
        else:
            logger.info("using AWS upload account returned from FASTgenomics")

        if account is not None and len(account) > 0:
            my_env['AWS_ACCESS_KEY_ID'] = account['awsAccessKeyId']
            my_env['AWS_SECRET_ACCESS_KEY'] = account['awsSecretAccessKey']
            my_env['AWS_DEFAULT_REGION'] = account['awsRegion']
        else:
            logger.info(f"using default AWS account")

        configuration = self._get_configuration()

        aws = "aws"
        if configuration.awscli_path != "":
            aws = configuration.awscli_path

        params = [aws, "s3", "cp", full_filename,
                  sai.upload_uri]
        if len(configuration.awscli_additional_cli_options) > 0:
            for o in configuration.awscli_additional_cli_options:
                params.append(o)

        logger.info(
            f"{' '.join(params)}")

        subprocess.run(params,
                       shell=False, check=True, env=my_env)

        return

    def __create_dataset_and_attach_lfs(self, sai: LargeFileStorageAccessInformation, title: str) -> str:
        """ create a dataset and attach the lfs """
        bearer_token = self._get_bearer_token()

        # create the dataset
        logger.info("creating dataset")
        url = self._get_url("webclient/api/datasets")

        request_data = {
            "title": title,
            "files": []
        }

        request_json = json.dumps(request_data)

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f"Bearer {bearer_token}",
            'User-Agent': user_agent
        }

        response = self.session.post(url, data=request_json, headers=headers)
        self._handle_response(response)
        dataset = response.json()

        dataset_id = dataset["id"]
        logger.info(f"created dataset '{dataset_id}'")

        # attach the lfs
        logger.info("attaching lfs to dataset")
        url = self._get_url(
            f"webclient/api/lfs/{sai.storage_id}/dataset/{dataset_id}")
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f"Bearer {bearer_token}",
            'User-Agent': user_agent
        }

        response = self.session.put(url, headers=headers)
        self._handle_response(response)

        dataset_url = self.get_dataset_details_url(dataset_id, "Files")
        logger.info(f"dataset url: {dataset_url}")
        return dataset_id

    def __store_report(self, storage_info: LargeFileStorageInformation, sai: LargeFileStorageAccessInformation,
                       recipient_email: str, zip_password: str, full_filename: str, signed_downloadurl: str):
        """ store the report file for a large file storage to vault """
        configuration = self._get_configuration()

        report_filename = path.join(
            configuration.lfs_vault_directory, f"{storage_info.storage_id}-report.txt")

        logger.info(f"saving report {report_filename}")

        report = {}
        report["Storage id"] = sai.storage_id
        report["Title"] = sai.title
        report["User access token"] = sai.user_accesstoken
        report["Dataset id"] = storage_info.dataset_id
        report["Dataset url"] = self.get_dataset_details_url(
            storage_info.dataset_id, "Files")
        report["Download URI"] = sai.download_uri
        report["Zip password"] = zip_password
        report["Cloud provider"] = sai.provider_type
        if signed_downloadurl != "":
            report["Signed Download URL"] = signed_downloadurl

        download_account = {}
        if sai.download_account is not None and len(sai.download_account) > 0:
            download_account = sai.download_account
        else:
            download_account = self.__get_stored_account(
                recipient_email, sai.provider_type)

        if download_account is not None:
            for key in download_account:
                report[f"Account {key}"] = download_account[key]

        with open(report_filename, "w") as f:
            for key in report:
                value = report[key]
                print(f"{key:28}:\t{value}", file=f)
            print("", file=f)
            if signed_downloadurl != "" and sai.provider_type.lower() == "aws":
                print("The signed download url is valid for 7 days only.", file=f)
                print("", file=f)

            print("", file=f)

            print("Download the file from FASTGenomics:", file=f)
            print("", file=f)
            print("  Open browser and navigate to :", file=f)
            v = report["Dataset url"]
            print(f"  {v}  ", file=f)
            print(
                f"  Click download button of large file storage and provide your user access token", file=f)
            v = report["User access token"]
            print(f"  {v}  ", file=f)
            print(f"  Click on the link to download the file.", file=f)
            print("", file=f)
            print(
                f"  Extract files using 7-zip. Use this password to enable extraction", file=f)
            v = report["Zip password"]
            print(f"  {v}  ", file=f)
            print(f"  Click on the link to download the file.", file=f)

            if signed_downloadurl != "":
                print("", file=f)
                print("Download the file by curl", file=f)
                print("", file=f)
                filename = path.basename(full_filename)
                print(
                    f"  curl -o \"{filename}\" \"{signed_downloadurl}\" ", file=f)
                print("", file=f)
                print(
                    f"  Extract files using 7-zip. Use this password to enable extraction", file=f)
                v = report["Zip password"]
                print(f"  {v}  ", file=f)
                print(f"  Click on the link to download the file.", file=f)

            if sai.provider_type.lower() == "azure":
                print("", file=f)
                print("Download the file by azcopy", file=f)
                print("", file=f)
                filename = path.basename(full_filename)
                uri = report["Download URI"]
                print(
                    f"  azcopy copy \"{uri}\" \"{filename}\"", file=f)
                print("", file=f)
                print(
                    f"  Extract files using 7-zip. Use this password to enable extraction", file=f)
                v = report["Zip password"]
                print(f"  {v}  ", file=f)
                print(f"  Click on the link to download the file.", file=f)

            elif sai.provider_type.lower() == "aws":
                print("", file=f)
                print("Download the file by aws cp", file=f)
                print("", file=f)
                print("  Configure AWS using this credentials. (aws configure)", file=f)
                aws_id = report.get("Account awsAccessKeyId", "")
                aws_key = report.get("Account awsSecretAccessKey", "")
                aws_region = report.get("Account awsRegion", "")
                print(f"  AWS Access Key ID     : {aws_id}", file=f)
                print(f"  AWS Access Access Key : {aws_key}", file=f)
                print(f"  AWS Region            : {aws_region}", file=f)

                filename = path.basename(full_filename)
                uri = report["Download URI"]
                print(
                    f"  aws cp \"{uri}\" \"{filename}\"", file=f)

                print("", file=f)
                print(
                    f"  Extract files using 7-zip. Use this password to enable extraction", file=f)
                v = report["Zip password"]
                print(f"  {v}  ", file=f)
                print(f"  Click on the link to download the file.", file=f)

    def upload_file_to_lfs(self, provider_type: str, full_filename: str, title: str, recipient_email: str,
                           zip_password: str, include_signed_downloadurl: bool) -> LargeFileStorageInformation:
        """ upload a file to lfs
                create a dataset in fastgenomics

            Parameters:
            provider_type: str
                the type of the cloud provider "Azure" or "AWS"

            full_filename: str
                the file to be uploaded to the lfs

            title: str
                the title of the dataset which will be created

            recipient_email: str
                the email of the recipient of the data

            zip_password: str
                the password of the zip file

            include_signed_downloadurl: bool
                include the signed download url in report
        """

        uploaderInformation = self._ensure_uploader_account(provider_type)
        recipientInformation = self._ensure_recipient_account(
            provider_type, recipient_email)

        sai = self.__create_large_file_storage(
            provider_type, full_filename, title, recipientInformation, uploaderInformation)

        try:
            if provider_type.lower() == "azure":
                self.__upload_to_azure(sai, full_filename)
            elif provider_type.lower() == "aws":
                self.__upload_to_aws(sai, full_filename)
            else:
                raise Exception(f"Unknown cloud provider {provider_type}")

            logger.info("upload successfully done.")
            logger.info(
                f"UserAccessToken: {sai.user_accesstoken}")
            logger.info(
                f"Download URI   : {sai.download_uri}")

        except Exception as err:
            logger.error("Failed to create large file storage")
            self.__update_state(sai,
                                LargeFileStorageState.ERROR)
            raise

        self.__update_state(sai,
                            LargeFileStorageState.READY)

        if include_signed_downloadurl:
            signed_download_url = self.get_download_url(
                sai.storage_id, sai.user_accesstoken)
        else:
            signed_download_url = ""

        dataset_id = self.__create_dataset_and_attach_lfs(sai, title)
        info = LargeFileStorageInformation(
            sai.storage_id, sai.title, sai.created_at_utc, sai.expires_on_utc, dataset_id, sai.provider_type)

        self.__store_report(info, sai, recipient_email,
                            zip_password, full_filename, signed_download_url)
        return info

    def _ensure_uploader_account(self, provider_type: str) -> dict:
        """ ensure that the uploader account exists (especially for AWS) """
        account = self._get_fastgenomics_account()
        uploadEmail = account.fastgenomics_user
        domain = urlparse(account.fastgenomics_url).hostname

        uploader_information = {}
        uploader_information['userEmail'] = uploadEmail
        if provider_type.lower() == "aws":
            arn = self._aws_create_account(uploadEmail, domain)
            uploader_information['userArn'] = arn

        return uploader_information

    def _ensure_recipient_account(self, provider_type: str, recipient_email: str) -> dict:
        """ ensure that the recipient account exists (especially for AWS) """
        recipient_information = {}
        recipient_information['userEmail'] = recipient_email

        account = self._get_fastgenomics_account()
        domain = urlparse(account.fastgenomics_url).hostname
        if provider_type.lower() == "aws":
            arn = self._aws_create_account(recipient_email, domain)
            recipient_information['userArn'] = arn

        return recipient_information

    def get_download_url(self, storage_id: str, access_token: str) -> str:
        """ get the download url of a storage """
        assert storage_id != "", "You have have to provide a storage id"
        assert access_token != "", "You have have to provide an access token"

        bearer_token = self._get_bearer_token()

        logging.info(f"getting download url for storage {storage_id}")
        url = self._get_url(
            f"webclient/api/lfs/{storage_id}/content/{access_token}")

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f"Bearer {bearer_token}",
            'User-Agent': user_agent
        }
        response = self.session.get(
            url, headers=headers)
        self._handle_response(response)

        return response.text.strip("\"")


class FASTGenomicsDatasetClient(FASTGenomicsClient):
    """ the FASTGenomics client for datasets """

    def __init__(self):
        """ constructs the client """
        super().__init__()

    def add_file_to_dataset(self, dataset_id: str, full_filename: str, filetype: str, show_progress_bar=None) -> dict:
        """ add a file to a dataset

            Parameters:
            -----------
            dataset_id : str
                the id of the dataset

            full_fileName: str
                the full filename of the file to be uploaded

            filetype : str
                type of file - "ExpressionData" or "MetaData"

            Returns:
            --------
            {
                "file" :
                "url"  :
                "type" :
            }
        """

        if dataset_id == "":
            raise Exception("Dataset id is empty")

        if not path.exists(full_filename):
            raise FileNotFoundError(
                f"File to upload '{full_filename}' not found.")

        if not path.isfile(full_filename):
            raise IOError(
                f"Path '{full_filename}' is no file.")

        if filetype.lower() != "expressiondata" and filetype.lower() != "metadata":
            raise Exception(f"Invalid value for file type {filetype}")

        filename = path.basename(full_filename)
        filesize = path.getsize(full_filename)

        if filesize <= 0:
            raise AssertionError(f"The file '{full_filename}' is empty!")

        bearer_token = self._get_bearer_token()

        # register the upload
        logger.info(f"register upload of file {filename} {filesize} bytes")
        url = self._get_url("webclient/api/fileuploads")

        request_data = {
            "name": filename,
            "size": filesize
        }
        request_json = json.dumps(request_data)

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f"Bearer {bearer_token}",
            'User-Agent': user_agent
        }
        response = self.session.post(
            url, data=request_json, headers=headers)
        self._handle_response(response)
        uploadId = response.json()

        # attach to dataset
        logging.info(f"attaching upload {uploadId} to dataset {dataset_id}")
        url = self._get_url(f"webclient/api/datasets/{dataset_id}/files")

        request_data = {
            "uploadId": uploadId,
            "type": filetype}
        request_json = json.dumps(request_data)

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f"Bearer {bearer_token}",
            'User-Agent': user_agent
        }
        response = self.session.post(
            url, data=request_json, headers=headers)
        self._handle_response(response)

        # upload the file in chunks
        chunk_size = 1024 * 1024
        bytes_transferred = 0
        chunkId = 1

        show_bar = show_progress_bar is not False and (show_progress_bar or log_level <= logging.INFO)

        progress_bar = None
        if show_bar:
            progress_bar = tqdm(
                total=filesize, desc=f"uploading file {filename}")

        with open(full_filename, "rb") as f:
            chunk = f.read(chunk_size)
            while chunk:
                url = self._get_url(
                    f"webclient/api/fileuploads/{uploadId}/chunk/{chunkId}")
                headers = {
                    'Authorization': f"Bearer {bearer_token}",
                    'User-Agent': user_agent
                }
                response = self.session.post(url, data=chunk, headers=headers)
                self._handle_response(response)
                if progress_bar is not None:
                    progress_bar.update(len(chunk))
                bytes_transferred = bytes_transferred + len(chunk)
                chunkId = chunkId + 1
                chunk = f.read(chunk_size)

        if progress_bar is not None:
            progress_bar.close()

        url = self._get_url(f"/datasets/detail-{dataset_id}#Files")

        r = {
            "dataset_id": dataset_id,
            "file_name": full_filename,
            "file_size": filesize,
            "file_type": filetype,
            "url": url
        }
        return r

    def delete_dataset(self, dataset_id: str):
        """ delete a dataset """
        assert dataset_id != "", "You have have to provide a dataset id"

        bearer_token = self._get_bearer_token()

        logging.info(f"deleting dataset {dataset_id}")
        url = self._get_url(f"webclient/api/datasets/{dataset_id}")

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f"Bearer {bearer_token}",
            'User-Agent': user_agent
        }
        response = self.session.delete(
            url, headers=headers)
        self._handle_response(response)

    def create_dataset(self, title: str) -> requests.Response:
        logging.info(f"creating dataset {title}")
        bearer_token = self._get_bearer_token()
        url = self._get_url(f"webclient/api/datasets")
        request_data = {
            "title": title,
            "files": []
        }
        request_json = json.dumps(request_data)
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f"Bearer {bearer_token}",
            'User-Agent': user_agent
        }
        response = self.session.post(url, data=request_json, headers=headers)
        self._handle_response(response)
        return response
