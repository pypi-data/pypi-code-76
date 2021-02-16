api_key = None
api_environment = None
default_http_client = None
api_base = {
    "sandbox": "https://api-sandbox.circle.com",
    "production": "https://api.circle.com",
}.get(api_environment if api_environment else "sandbox")


max_network_retries = 0

from circle.resources import *
