import json

import requests



class ApiviewClient(object):

    def __init__(self):
        pass

    def get(self, url, params):
        response = requests.get(url, params=params)
        response_data = json.loads(response.content)
        return response_data

    def post(self, url, params):
        response = requests.post(url, json=params)
        response_data = json.loads(response.content)
        return response_data
