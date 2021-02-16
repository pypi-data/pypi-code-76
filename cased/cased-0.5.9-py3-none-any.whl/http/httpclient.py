import requests


class HTTPClient:
    @classmethod
    def make_request(cls, method, url, key, data=None):

        user_agent = "cased-guard"

        headers = {
            "Authorization": "Bearer " + key,
            "User-Agent": user_agent,
        }

        if method == "get":
            res = requests.get(url, params=data, headers=headers)
        elif method == "post":
            res = requests.post(url, json=data, headers=headers)
        elif method == "put":
            res = requests.put(url, json=data, headers=headers)
        elif method == "patch":
            res = requests.patch(url, json=data, headers=headers)
        elif method == "head":
            res = requests.head(url, headers=headers)
        elif method == "delete":
            res = requests.delete(url, headers=headers)
        else:
            raise Exception(
                """Unsupported method given. This is likely a bug in the
                Cased API library."""
            )

        log_debug(
            "Request sent. URL: {} | Params: {} | Headers: {}".format(
                url, str(data), str(headers)
            )
        )

        return res