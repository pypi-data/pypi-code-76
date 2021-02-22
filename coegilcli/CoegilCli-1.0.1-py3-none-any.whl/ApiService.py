from pathlib import Path
from typing import Dict
import json
import requests
import os


def api_get(endpoint: str, query_params: Dict):
    config = _get_configuration()
    url = _build_url(config, endpoint)
    headers = _get_headers(config)
    r = requests.get(url, headers=headers, params=query_params)
    return _parse_result(r)


def api_save(action_method: str, endpoint: str, payload: Dict):
    config = _get_configuration()
    url = _build_url(config, endpoint)
    headers = _get_headers(config)
    if action_method == 'POST':
        r = requests.post(url, headers=headers, data=json.dumps(payload))
    elif action_method == 'PUT':
        r = requests.put(url, headers=headers, data=json.dumps(payload))
    elif action_method == 'DELETE':
        r = requests.delete(url, headers=headers, params=payload)
    else:
        raise Exception(f'Unknown action method.  Method={action_method}')
    return _parse_result(r)


def get_environment(config: Dict = None) -> str:
    config = _get_configuration() if config is None else config
    return config['environment']


def set_configuration(environment: str, api_key: str):
    file_name = _get_config_file_name()
    with open(file_name, "w") as f:
        payload = json.dumps({
            'apiKey': api_key,
            'environment': environment
        })
        f.write(payload)


def _get_headers(config: Dict) -> Dict:
    headers = {
        'api_version': str(2),
        'coegil_api_key': config['apiKey'],

        # Don't feel like handling compressed results int he CLI - Don't need to yet
        'compress_results': str(False)
    }
    return headers


def _parse_result(r: requests.Response):
    result = r.json()
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(result) from e
    return result['data']


def _get_configuration() -> Dict:
    file_name = _get_config_file_name()
    with open(file_name, "r") as f:
        return json.loads(f.read())


def _get_config_file_name() -> str:
    directory = os.path.join(str(Path.home()), '.coegil')
    Path(directory).mkdir(parents=True, exist_ok=True)
    return os.path.join(directory, 'credentials')


def _build_url(config: Dict, endpoint: str) -> str:
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint
    environment = get_environment(config)
    return f'https://api.{environment}.app-coegil.com{endpoint}'
