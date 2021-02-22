import http.client
import urllib.parse as urlparse
import json


class UpdatePayoutAccount:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = "/payoutaccount/update/" + app + "/"

    def Process(self, request):
        #json_data = json.loads(request)
        headers = {"Content-type": "application/json",
                   "Accept": "application/json"}

        id = ""
        if "id" in request:
            id = request["id"]
        else:
            return {
                "code": 400,
                "error": "id is required for update"
            }

        url_info = urlparse.urlparse(self.endpoint + id)
        if url_info.scheme == "https":
            conn = http.client.HTTPSConnection(
                url_info.hostname, url_info.port or 443)
        else:
            conn = http.client.HTTPSConnection(
                url_info.hostname, url_info.port or 80)

        try:
            conn.request('POST', self.route, request, headers)
            response = conn.getresponse()
            if response.status == 200:
                return json.loads(response.read().decode())
            else:
                return {
                    "code": response.status,
                    "error": response.reason
                }
        finally:
            conn.close()
