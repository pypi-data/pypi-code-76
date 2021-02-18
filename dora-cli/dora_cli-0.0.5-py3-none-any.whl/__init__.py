"""
Command line interface
"""
import getpass
import logging
import os

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, os.environ.get('LOG_LEVEL','INFO')))
logger.debug(__name__)

def mask_secret(secret:str, mask:str='*', show:int=4) -> str:
    """Mask secret values with an character. 
    :param secret: string you need to mask.
    :param mask: Character used as mask.
    :param show: Number of not ofuscated characters at the end of the secret.
    :return: Masked secret
    """
    data_mask = ''.join([mask for _ in range(len(secret)-show)])
    return f"[{data_mask + str(secret)[len(secret)-show:len(secret)]}]"

def prompt_secret(prompt:str,default:str=None) -> str:
    """Promt user to input a secret value. 
    :param prompt: Prompt value.
    :param default: Default value
    :return: user inputed value
    """
    _secret = str()
    if default is not None and default != '':
        _secret = mask_secret(default)
    user_input = getpass.getpass(prompt=f"{prompt}{_secret}")
    if user_input is None or user_input == '':
        return default
    return user_input
