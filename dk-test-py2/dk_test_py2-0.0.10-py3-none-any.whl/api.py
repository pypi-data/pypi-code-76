import requests

r = requests.session()


class Collpay:
    __sandbox_base_url = "https://collpay-dev.dev.squaredbyte.com"
    __production_base_url = "localhost"
    __public_key = ""
    __base_url = __production_base_url
    __env_production = 1
    __env_sandbox = 2
    __v1 = "v1"
    __api_version = __v1

    def __init__(self, public_key, env=__env_production, api_version=__v1):
        self.__public_key = public_key
        if env == self.__env_sandbox:
            self.__base_url = self.__sandbox_base_url
        self.__api_version = api_version

    def get_exchange_rate(self, _from, _to):
        data = {
            "from": _from,
            "to": _to
        }
        response = self.__make_request("exchange-rate", "post", data)
        return response

    def create_transaction(self, transaction_data):
        response = self.__make_request("transactions", "post", transaction_data)
        return response

    def get_transaction(self, transaction_id):
        if transaction_id == "":
            return {
                "success": False,
                "message": "Invalid transaction id"
            }
        url = f"transactions/{transaction_id}"
        response = self.__make_request(url, "get")
        return response

    def __make_request(self, url, method, data=None):
        try:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "Accept-Language": "en",
                "x-auth": self.__public_key
            }
            api_url = f"{self.__base_url}/api/{self.__api_version}/{url}"
            response = r.request(method, api_url, headers=headers, data=data)
            return response.json()

        except Exception as msg:
            return {
                "success": False,
                "message": msg
            }
