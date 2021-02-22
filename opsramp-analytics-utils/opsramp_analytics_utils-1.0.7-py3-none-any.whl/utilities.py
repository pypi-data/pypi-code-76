import os
import json

from datetime import datetime

import jwt
import flask
import requests


BASE_API_URL = os.getenv('API_SERVER', '')


def get_jwt_token():
    jwt_token = flask.request.cookies.get('OPSRAMP_JWT_TOKEN', '')

    return jwt_token


def get_headers():
    headers = {
        'Authorization': f'Bearer {get_jwt_token()}'
    }

    return headers


def get_msp_id():
    msp_id = None
    jwt_token = get_jwt_token()
    if jwt_token:
        decoded = jwt.decode(jwt_token, options={"verify_signature": False})
        msp_id = decoded['orgId']

    return msp_id


def call_get_requests(url, params=None):
    headers = get_headers()
    resp = requests.get(url, headers=headers, params=params)

    return resp


def call_post_requests(url, params=None, data=None):
    headers = get_headers()
    resp = requests.post(url, headers=headers, params=params, data=data)

    return resp


def save_archive(oap_name, state, size='A3', route=None, tag='tag'):
    service_url = os.getenv("VIEW_SERVICE", 'http://localhost:8000')
    url = service_url + '/archives'
    data = {
        'oap': oap_name,
        'tag': tag,
        'state': json.dumps(state),
        'size': size,
        'route': route
    }

    res = requests.post(url, json=data).json()

    return res


def get_archives(oap_name):
    service_url = os.getenv("VIEW_SERVICE", 'http://localhost:8000')
    url = service_url + '/archives'

    params = { 'oap': oap_name }
    print (url, params, '='*10)
    res = requests.get(url, params=params).json()

    return [{'label': datetime.strptime(ii['created'], '%Y-%m-%dT%H:%M:%S').strftime('%m/%d/%Y %H:%M:%S'), 'value': ii['id']} for ii in res]


def get_archive(archive_id):
    service_url = os.getenv("VIEW_SERVICE", 'http://localhost:8000')
    url = f'{service_url}/archives/{archive_id}'
    archive = requests.get(url).json()

    return archive


def generate_pdf(oap_name, data, size='A3', route=None):
    url = os.getenv("PDF_SERVER", 'http://localhost:8000/generate-report')

    post_data = {
        'report': oap_name,
        'params': json.dumps(data),
        'route': route,
        'size': size
    }

    res = requests.post(url, data=post_data).json()

    return res
