import json
from hashlib import md5

import requests


class Client:
    url: str = "http://localhost:55000/"

    def send(self, geometries):
        dic = {}
        # TODO: put transformation and hash function common to both front and backend in a pip package.
        hash_number = int.from_bytes(md5(json.dumps(geometries).encode()).digest(), byteorder="big") % 10 ** 16
        dic.update(geometry_set_id=hash_number, geometries=geometries)
        response = requests.post(self.url + "/store", json=dic)
        return response.json()["message"]
