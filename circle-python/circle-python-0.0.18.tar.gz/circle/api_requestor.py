import json
import urllib
import uuid

import circle
from circle import http_client
from circle.circle_response import CircleResponse


class APIRequestor:
    def __init__(self, api_key=None, api_base=None, client=None):
        self.api_base = api_base or circle.api_base
        self.api_key = api_key or circle.api_key
        if client:
            self._client = client
        elif circle.default_http_client:
            """Users can change the default http client with circle.default_http_client"""
            self._client = circle.default_http_client
        else:
            """If no default http client is set, set one to avoid creating one for every request."""
            circle.default_http_client = http_client.new_default_http_client()
            self._client = circle.default_http_client

    def interpret_response(self, rbody, rcode, rheaders):
        try:

            resp = CircleResponse(rbody, rcode, rheaders)
        except Exception:
            raise Exception(
                f"Invalid response from API: {rbody} (HTTP response code: {rcode})",
                rbody,
                rcode,
                rheaders,
            )
        # if not 200 <= rcode < 300:
        #     self.handle_error_response(rbody, rcode, resp.data, rheaders)
        return resp

    def request_headers(self, api_key):
        user_agent = "Circle Python SDK"
        headers = {
            "Authorization": "Bearer %s" % api_key,
            "User-Agent": user_agent,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        return headers

    def request(self, method, url, params, headers=None):
        rbody, rcode, rheaders, api_key = self.request_raw(method.lower(), url, params)
        resp = self.interpret_response(rbody, rcode, rheaders)
        return resp, api_key

    def request_raw(self, method, url, params={}, supplied_headers=None):
        if self.api_key:
            api_key = self.api_key
        else:
            from circle import api_key

            api_key = api_key
        if api_key is None:

            # TODO: use custom AuthenticationError exception here
            raise Exception("Invalid api key")

        abs_url = "%s%s" % (self.api_base, url)

        if method in (
            "post",
            "patch",
        ):
            params.setdefault("idempotencyKey", uuid.uuid4().__str__())
            post_data = json.dumps(params)
        elif method in (
            "get",
            "delete",
        ):
            post_data = None
            # TODO: generate query params for get/delete methods
        else:
            # TODO: use a proper error here
            raise Exception("Invalid HTTP method.")

        headers = self.request_headers(api_key)
        if supplied_headers is not None:
            for key, val in supplied_headers.items():
                headers[key] = val

        rbody, rcode, rheaders = self._client.request_with_retries(
            method, abs_url, headers, post_data
        )

        return rbody, rcode, rheaders, api_key
