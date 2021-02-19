import base64
import functools
import json
import logging
import urllib.request

import jwt

logger = logging.getLogger(__name__)
ACCESS_TOKEN_HEADER = "HTTP_X_AMZN_OIDC_ACCESSTOKEN"
IDENTITY_HEADER = "HTTP_X_AMZN_OIDC_IDENTITY"
DATA_HEADER = "HTTP_X_AMZN_OIDC_DATA"


@functools.lru_cache(maxsize=None)
def get_public_key(region, key_id):
    url = public_key_endpoint(region, key_id)
    with urllib.request.urlopen(url) as res:
        return res.read()


def public_key_endpoint(region, key_id):
    return f"https://public-keys.auth.elb.{region}.amazonaws.com/{key_id}"


def verify(data: str, region: str, kid: str, alg: str) -> dict:
    pubkey = get_public_key(region, kid)
    return jwt.decode(data, pubkey, algorithms=[alg])


def extract_headers(data: str, encoding="utf-8") -> dict:
    try:
        jwt_headers = data.split(".")[0]
        decoded_jwt_headers = base64.b64decode(jwt_headers + "=" * 10)
        decoded_jwt_headers = decoded_jwt_headers.decode(encoding=encoding)
        decoded_json = json.loads(decoded_jwt_headers)
        return decoded_json
    except Exception as e:
        logger.error(e)
        return None


class JWTIdentifier:
    def __init__(self, region: str) -> None:
        self.region = region

    def verify(self, data: str) -> dict:
        jwt_headers = extract_headers(data)
        return verify(data, self.region, jwt_headers["kid"], jwt_headers["alg"])

    def identify(self, request) -> dict:
        if DATA_HEADER not in request.META:
            logger.debug("not idp")
            return
        data = request.META[DATA_HEADER]
        info = self.verify(data)
        return info
