import json

import requests

from Optimizers import config


def optimize(data, timelimit=60):
    try:
        req = {
            'timelimit': timelimit,
            'key': config.server_key
        }
        req.update(data)
        solution = json.loads(
            requests.put(config.server_url, data=json.dumps(req), headers={"Content-Type": "application/json"}).text)
        return solution
    except Exception as err:
        return {"status": f'error: connecting to server {err}'}
