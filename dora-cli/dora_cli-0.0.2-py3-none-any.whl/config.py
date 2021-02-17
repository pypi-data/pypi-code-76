"""
Create an configuration file
"""
import json
from clint import resources
from clint.textui import puts
from clint.textui import colored
from clint.textui import prompt
from dora_cli import mask_secret
from dora_cli import logger

CONFIG_FILE="config.json"
PROVIDERS = [
    {'selector':1,'prompt':"Huawei Cloud",'return':"hwc"}
    # {'selector':2,'prompt':"Amazon Web Services",'return':"aws"}
    ]

resources.init('Dora Project', 'dora-cli')

def get_config(config_file:str=None) -> dict:
    """Get current configuration. 
    :param config_file: Init with external configuration file
    :return: Return None if there is no config file available
    """
    try:
        if config_file is None:
            _config = resources.user.read(CONFIG_FILE)
            if _config is None:
                raise ValueError('Not configured')
            config = json.loads(_config)
        else:
            config = json.loads(config_file)
    except Exception as err:
        logger.warning(err)
        return dict()
    return config

def show(config:dict) -> dict:
    """Print configuration values. 
    :param config: Configurations
    :return: Formated configurations
    """
    _config = dict()
    if config.get('provider'):
        _config["Cloud Provider"]=config['provider']
    if config.get('credentials'):
        _config["Region"]=config['credentials']['region_key']
        _config["Username"]=config['credentials']['username']
        _config["Access Key"]=mask_secret(config['credentials']['access_key'])
        _config["Secret Key"]=mask_secret(config['credentials']['secret_key'])
        if config['credentials'].get('token'):
            _config["Temp Token"]=mask_secret(config['credentials']['token'][-40:])
    if config.get('storages'):
        if config['storages'].get('bucket_name'):
            _config["Bucket"]=config['storages']['bucket_name']
        if config['storages'].get('shared_nfs'):
            _config["Mounting Point"]=config['storages']['shared_nfs']
    return json.dumps(_config,indent=2)

def define_provider(provider:str=None) -> list:
    """Configure cloud provider. 
    :param provider: Provider identifier
    :return: provier name and provider configuration client
    """
    _provider = provider
    if provider is None or provider not in [p['return'] for p in PROVIDERS]:
        _provider = prompt.options("Cloud Provider:", PROVIDERS)
    if _provider == 'hwc':
        from dora_cli import hwc
        return [_provider, hwc]
    if _provider == 'aws':
        from dora_cli import aws
        return [_provider, aws]
    raise ValueError("Provider not found!")

def setup(config:dict,provider:str=None, config_file:str=None) -> dict:
    """Setup configuration file. 
    :param config: Current values of configuration
    :param provider: Provider name
    :param config_file: Path of an external configuration file
    :return: configurations
    """
    _config = config
    if config is None:
        _config = get_config(config_file)
    _config['provider'], _profiver_conf = define_provider(provider)
    _config['credentials'] = _profiver_conf.credentials(_config.get('credentials'))
    _config['storages'] = _profiver_conf.storages(_config)
    show(_config)
    puts(colored.yellow(show(_config)))
    if prompt.yn("Save?"):
        resources.user.write(CONFIG_FILE, json.dumps(_config))
        puts(colored.green("Done"))
        return _config
    puts(colored.green("Ignored"))
    return _config
