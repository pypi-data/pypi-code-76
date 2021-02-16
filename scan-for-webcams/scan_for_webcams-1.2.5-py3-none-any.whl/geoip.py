import requests


class Locater:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://geo.ipify.org/api/v1"

    def locate(self, ip):
        data = dict()
        data['apiKey'] = self.api_key
        data['ipAddress'] = ip
        r = requests.get(self.url, data=data)
        res = r.json()
        country = res['location']['country']
        reigon = res['location']['reigon']
        return country, reigon
