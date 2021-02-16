import json,time,pdb
from requests.exceptions import ReadTimeout
from platform import python_version

from ...seleya import session
from ...version import __version__
from ...config.default_config import *

timeout = 60
max_retries = 5
retry_interval = 2

client_info = json.dumps({"python_version": python_version(),
"client_version": __version__,
"module":"seleya_sdk"})

def __get_conn__():
    return server

def get_http_result(http_client, request_string, 
                    gw, max_retries=max_retries):
    for i in range(1, max_retries + 1):
        try:
            result = session.get("http://%s:%d/%s" % (http_client[0], http_client[1], request_string),
                                  headers={'accept': 'application/json', 
                                           'CLIENT_INFO': client_info},
                                  timeout=timeout)
            return result
        except Exception as e:
            time.sleep(retry_interval)

def post_http_result(http_client, request_string,  body, 
                     gw, max_retries=max_retries):
    for i in range(1, max_retries + 1):
        try:
            result = session.post("http://%s:%d/%s" % (http_client[0], http_client[1], request_string),
                                  data = body,
                                  headers={'accept': 'application/json',
                                           'Content-Type':'application/x-www-form-urlencoded',
                                           'CLIENT_INFO': client_info},
                                  timeout=timeout)
            return result
        except Exception as e:
            time.sleep(retry_interval)
    
def __get_result__(method, request_string, http_client, body=None, gw=True):
    try:
        if method == 'GET':
            result = get_http_result(http_client, request_string, gw)
        elif method == 'POST':
            result = post_http_result(http_client, request_string, body, gw)
            
        if result.status_code != 200:
            raise Exception(result.status_code)
        return result.text
    except ReadTimeout:
        raise Exception('Time-Out')
    except Exception as e:
        raise e