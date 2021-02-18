import requests
from cguard.util import log_level
import shutil
import hashlib


class HTTPClient:
    @classmethod
    def _cguard_hash(cls):
        filepath = shutil.which("cased")
        cguard = open(filepath, "rb")
        digest = hashlib.sha256(cguard.read()).hexdigest()
        cguard.close()
        return digest

    @classmethod
    def _check_for_server_error(cls, res):
        if res.status_code == 500:
            print(
                "Server error. Is a Slack channel configured for this Guard application?"
            )
            exit(1)

    @classmethod
    def make_request(cls, method, url, data=None, key=None):

        user_agent = "cased-guard"
        headers = {
            "User-Agent": user_agent,
            "X-Guard-Hash": cls._cguard_hash(),
            "Content-Type": "application/json",
        }

        if key:
            value = "Bearer " + key
            headers["Authorization"] = value

        if method == "get":
            res = requests.get(url, params=data, headers=headers, timeout=20)
        elif method == "post":
            res = requests.post(url, json=data, headers=headers, timeout=20)
        elif method == "put":
            res = requests.put(url, json=data, headers=headers, timeout=20)
        elif method == "patch":
            res = requests.patch(url, json=data, headers=headers, timeout=20)
        elif method == "head":
            res = requests.head(url, headers=headers, timeout=20)
        elif method == "delete":
            res = requests.delete(url, headers=headers, timeout=20)
        else:
            raise Exception(
                """Unsupported method given. This is likely a bug in the
                cased program. Please contact"""
            )

        cls._check_for_server_error(res)

        if log_level() == "debug":
            print(
                "Request sent. URL: {} | Params: {} | Headers: {}".format(
                    url, str(data), str(headers)
                )
            )

        return res