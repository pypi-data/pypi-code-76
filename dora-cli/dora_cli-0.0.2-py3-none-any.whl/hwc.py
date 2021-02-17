"""
Configure Huawei Cloud provider
"""
import json
import os
import re
import subprocess
from time import sleep

from clint.textui import prompt
from clint.textui import puts
from clint.textui import colored
import docker as DockerClient
from obs import ObsClient
import requests

from dora_cli import prompt_secret
from dora_cli import logger

IMG_NAME="docker.pkg.github.com/doraproject/docker/ide:hwc"
IAM_HOST="https://iam.myhuaweicloud.com"
SFS_HOST="sfs-nas1.{region}.myhuaweicloud.com"
OBS_HOST="https://obs.{region}.myhuaweicloud.com"
HEADERS = {'Content-Type': 'application/json;charset=utf8'}

def tokens(config:dict) -> str:
    """Generate temporary token
    :param config: Dictionary with domain, name and password for authentication
    :return: token
    """
    url = f"{IAM_HOST}/v3/auth/tokens"
    payload = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "domain": {"name": config.get("domain")},
                        "name": config.get("username"),
                        "password": config.get("password")
                    }}}}}
    return requests.request("POST", url, headers=HEADERS, data=json.dumps(payload)).headers.get('X-Subject-Token')

def list_regions(access_token:str) -> list:
    """Generate list of all regions available
    :param token: Dictionary with domain, name and password for authentication
    :return: List of options with all regions
    """
    url = f"{IAM_HOST}/v3/regions"
    HEADERS['x-auth-token']=access_token
    res = json.loads(requests.request("GET", url, headers=HEADERS).text)
    logger.debug(res)
    regions = {_rg['id']:_rg['locales']['en-us'] for _rg in res['regions'] if _rg['type']=="public"}
    return [{'selector':key,'prompt':regions[value],'return':value}for key, value in enumerate(regions)]

def list_buckets(access_key:str, secret_key:str, region_key:str, create_option:bool=False):
    """Generate list of all buckets available
    :param access_key: Access Key authorization
    :param secret_key: Secret Key authorization
    :param region_key: Region Identifier
    :param create_option: Add option "0" to create a new bucket
    :return: List of options with all bucket options available
    """
    obs_client = ObsClient(
        access_key_id=access_key,
        secret_access_key=secret_key,
        server=OBS_HOST.format(region=region_key)
    )
    try:
        response = obs_client.listBuckets(True)
        logger.debug(response)
        bucket_list = list()
        if create_option:
            bucket_list.append([{'selector':0,'prompt':"Create a new bucket",'return':None}])
        for value in response['body'].get('buckets'):
            if value.get('location')==region_key:
                bucket_list.append({'selector':len(bucket_list),'prompt':value.get('name'),'return':value.get('name')})
        return bucket_list
    finally:
        obs_client.close()

def credentials(config:dict) -> dict :
    """Configure Huawei cloud credentials
    :param config: Current configuration values
    :return: Configuration values
    """
    if config is None:
        config = dict()
    _config = config
    puts(colored.green("Authorization"))
    _config['domain']=prompt.query("Account Name:",default=config.get('domain'))
    _config['username']=prompt.query("IAM username or email address:",default=config.get('username'))
    _config['password']=prompt_secret("Password:", default=config.get('password'))
    puts(colored.green("Credentials"))
    _config['access_key']=prompt_secret("Access Key ID:", default=config.get('access_key'))
    _config['secret_key']=prompt_secret("Secret Key ID:", default=config.get('secret_key'))
    if config.get('token') is None:
        _config['token'] = tokens(config)
    else:
        if not prompt.yn("Update Token?",default='n'):
            _config['token'] = tokens(_config)
        else:
            _config['token'] = config.get('token')
    if _config.get('region_key') is not None:
        if not prompt.yn(f"Update region?[{_config['region_key']}]",default='n'):
            _config['region_key'] = prompt.options("Region:", list_regions(_config['token']))
    else:
        _config['region_key'] = prompt.options("Region:", list_regions(_config['token']))
    return _config

def storages(config:dict) -> dict :
    """Configure Huawei cloud Storages
    :param config: Current configuration values
    :return: Configuration values
    """
    _creden = config['credentials']
    _config = config.get('storages')
    if _config is None:
        _config = dict()
    puts(colored.green("Storage"))
    if _config.get('bucket_name') is not None:
        if not prompt.yn(f"Update bucket?[{_config['bucket_name']}]",default='n'):
            _config['bucket_name'] = prompt.options("Bucket:", list_buckets(_creden['access_key'],_creden['secret_key'],_creden['region_key']))
    else:
        _config['bucket_name'] = prompt.options("OBS Bucket:", list_buckets(_creden['access_key'],_creden['secret_key'],_creden['region_key']))
    shared_nfs = _config.get('shared_nfs')
    if shared_nfs is not None:
        shared_nfs = shared_nfs.split(":/")[-1]
    shared_nfs = prompt.query("Scalable File Service mount point:",default=shared_nfs)
    _config['shared_nfs'] = f"{SFS_HOST.format(region=_creden['region_key'])}:/{shared_nfs}"
    return _config

def config_volumes(config:dict, directory:str='/shared') -> dict:
    """ Configure Image Volumes
        Ex: {
                '/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'},
                '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'}
            }
    :param config: Current configuration
    :return: A dictionary to configure volumes mounted inside the container.
    """
    _dir = f"{os.getcwd()}{directory}"
    logger.debug(_dir)
    # Create local shared directory
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    # Mount nfs
    try:
        _nfs =str(config['storages']['shared_nfs'])
        subprocess.run(
            ['mount','-t','nfs','-o','vers=3,timeo=600,nolock',_nfs,_dir],
            stdout=subprocess.PIPE).stdout.decode("utf-8")
    except Exception as err:
        logger.error(err)
        logger.warning("You are note using an shared file system!")
    # Mapping directories
    usr = config['credentials']['username']
    volumes = {
        f"{_dir}/data/{usr}/meta":{'bind': '/dora/meta', 'mode': 'rw'},
        f"{_dir}/data/{usr}/logs":{'bind': '/dora/logs', 'mode': 'rw'},
        f"{_dir}/data/{usr}/note":{'bind': '/dora/note', 'mode': 'rw'},
        f"{_dir}/data/{usr}/ide" :{'bind': '/root/.jupyter', 'mode': 'rw'}}
    # Create subdirectories
    for volume_path in volumes:
        if not os.path.exists(volume_path):
            os.makedirs(volume_path)
    return volumes

def run_container(config:dict, image:str=None):
    """Run container
    :param config: Current configuration values
    :param image: Image name and version
    """
    docker_cli = DockerClient.from_env()
    image_name = IMG_NAME
    if image is not None:
        image_name = image
    logger.debug(image_name)
    return docker_cli.containers.run(
        image=image_name,
        environment=dict(
            DORA_BKT=config['storages']['bucket_name'],
            DORA_USR=config['credentials']['username'],
            REGION_KEY=config['credentials']['region_key'],
            ACCESS_KEY=config['credentials']['access_key'],
            SECRET_KEY=config['credentials']['secret_key']),
        ports={
            '4040/tcp': 4040,
            '8888/tcp': 8888},
        volumes=config_volumes(config),
        detach=True, 
        auto_remove=True)

def jupyter_token(container, regex:str=r"""http:\/\/127\.0\.0\.1:8888/\?token=(.{48})""", attempts:int=60) -> str:
    """Get jupyter token
    :param container: Docker container instance
    :param regex: Regex pattern to find jupyter token in the output
    :param attempts: Number of attepts trys to find the token
    :return: Token string
    """
    for _ in range(attempts):
        try:
            log_msg = container.logs().decode("utf-8")
            logger.debug(log_msg)
            matches = re.finditer(regex,log_msg,re.IGNORECASE)
            metch = next(matches)
            logger.debug(metch.groups())
            return metch.group(1)
        except StopIteration as err:
            logger.debug(err)
            sleep(1)
    raise ValueError(f"Maximum number of attempts({attempts}) achieved!")

def start(config:dict, args:dict):
    """Start Docker image container
    :param config: Current configuration values
    :param args: Command line arguments
    """
    con = run_container(config, args['<docker-image>'])
    puts(colored.green(f"TOKEN:{jupyter_token(con)}"))
    return con
