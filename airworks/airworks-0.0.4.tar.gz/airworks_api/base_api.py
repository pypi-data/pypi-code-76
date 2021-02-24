import json
import time
from json import JSONDecodeError
from urllib import request, parse


class ApiError(Exception):
    def __init__(self, error_code, error_msg):
        self.error_code = error_code
        self.error_msg = error_msg

    def __str__(self):
        return f"ErrorCode: {self.error_code}, ErrorMsg: {self.error_msg}"


class ApiResponse:
    def __init__(self, api: "BaseApi"):
        self.api = api


class BaseApi:
    base_url = ""
    token_api = "api_gateway/auth/get_token"

    app_method = "get"
    app_url = ""
    app_id = ""
    app_key = ""
    app_secret = ""

    def __init__(self):
        self.token_str = ""
        self.token_expired_time = 0

    @classmethod
    def to_response(cls, response):
        try:
            json_response = json.loads(response)
        except JSONDecodeError:
            raise ApiError(error_code=30000, error_msg="json解析错误")
        if json_response.get("error_code") != 0:
            raise ApiError(
                error_code=json_response["error_code"],
                error_msg=json_response.get("error_message"),
            )
        return json_response

    @classmethod
    def get(cls, url, params):
        query_string = parse.urlencode(params)
        u = request.urlopen(f"http://{cls.base_url}/{url}?{query_string}")
        return cls.to_response(u.read())

    @classmethod
    def post(cls, url, params):
        query_string = parse.urlencode(params)
        u = request.urlopen(f"http://{cls.base_url}/{url}", query_string.encode("utf8"))
        return cls.to_response(u.read())

    def refresh_token(self):
        token_response = self.post(
            self.token_api,
            {
                "app_id": self.app_id,
                "app_key": self.app_key,
                "app_secret": self.app_secret,
            },
        ).get('data')
        self.token_str = token_response.get("token")
        self.token_expired_time = token_response.get("expire_time")

    def _api_response(self, token_update=True, **kwargs):
        if not self.token_str or time.time() > self.token_expired_time:
            self.refresh_token()
        try:
            kwargs["token"] = self.token_str
            if self.app_method.lower() == "get":
                json_response = self.get(self.app_url, kwargs)
            elif self.app_method.lower() == "post":
                json_response = self.post(self.app_url, kwargs)
            else:
                raise ApiError(error_code=30001, error_msg="目前仅支持post和get的接口")
        except ApiError as e:
            if token_update and e.error_code == 40002:
                return self._api_response(False, **kwargs)
            else:
                raise e
        return json_response

    def api_response(self, **kwargs):
        return self._api_response(**kwargs)
