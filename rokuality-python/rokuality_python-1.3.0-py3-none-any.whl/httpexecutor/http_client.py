import json
import requests
import os
from src.exceptions.server_failure_exception import ServerFailureException
from src.exceptions.not_authorized_exception import NotAuthorizedException


class HttpClient:

    DEFAULT_TIMEOUT = 90
    server_url = None

    def __init__(self, server_url):
        self.server_url = server_url

    def post_to_server(self, servlet_name, json_request):
        url = self.construct_url(self.server_url, servlet_name)
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data = json.dumps(json_request), headers = headers, timeout = self.DEFAULT_TIMEOUT)

        if response is None:
            raise ServerFailureException(
                "The server failed to respond at " + self.server_url + ". Is the server listening at this location?")

        response_json = json.loads(response.text)

        if (response.status_code == 401):
            raise NotAuthorizedException(response_json['results'])

        if not response.ok and not "results" in response_json:
            raise ServerFailureException(
                "The server responded at " + self.server_url + " with an unknown error!")

        return response_json

    def construct_url(self, server_url, servlet_name):
            finalized_url = None
            base_url = server_url
            query_string = ""

            if "?" in server_url:
                url_comps = server_url.split("?")
                base_url = url_comps[0]
                if len(url_comps) >= 2:
                    query_string = "?" + url_comps[1]
            
            finalized_url = base_url + "/" + servlet_name + query_string
            return finalized_url
