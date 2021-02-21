from yurl import URL
import requests
import jwt
import json
from copy import copy
from PyDoge.utils import get_time_now, Map


class HttpService:
    def __init__(self, config, generate_token=False, cache=None, token_key=None, token_service=None):
        self.config = config
        self.generate_token = generate_token
        self.cache = cache
        self.token_key = token_key
        self.token_service = token_service

    def get_name(self): return None
    def get_method(self): return None

    def get_url(self, data=None):
        cfg = self.config
        service = cfg.services[self.get_name()]
        dependency = cfg.dependencies[service['dependency']][cfg.env]
        serv = copy(service)
        del serv['dependency']
        url_options = {**serv, **dependency}
        return URL(**url_options)

    def get_request_data(self, data=None): return data
    def get_expected_response_code(self): return 200

    def get_content_type(self): return {'Content-Type': 'application/json'}

    def get_consumer_id(self): return {
        'x-global-consumer-id': self.config.consumer_id
    } if 'consumer_id' in self.config.__dict__.keys() else None

    def get_token(self):
        if self.generate_token:
            token = self.cache.get(self.token_key)
            valid = True

            if token is not None:
                token = Map(json.loads(token))
                valid = token.exp >= get_time_now()

            if token is None or not valid:
                access_token = Map(self.token_service()).access_token
                decoded = Map(jwt.decode(access_token, verify=False))
                token = {'value': access_token, 'exp': decoded.exp}
                json_string = json.dumps(token)
                self.cache.set(self.token_key, json_string)
                token = Map(token)

            return {'Authorization': f'Bearer {token.value}'}

        return None

    def get_headers(self):
        headers = self.get_content_type()

        consumer_id = self.get_consumer_id()
        if consumer_id is not None:
            headers.update(consumer_id)

        token = self.get_token()
        if token is not None:
            headers.update(token)

        return headers

    def request(self, data=None):
        url = self.get_url(data)

        headers = self.get_headers()

        response = getattr(requests, self.get_method())(
            url,
            json=self.get_request_data(data),
            headers=headers
        )

        if response.status_code != self.get_expected_response_code():
            raise Exception(
                f'{self.get_name()} error: {response.status_code} - {response.text}')

        return response.json() if 'Content-Type' in headers and headers['Content-Type'] == 'application/json' else response.text
