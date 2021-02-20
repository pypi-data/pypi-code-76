# Built-in
import base64
import hashlib
import hmac
import json
import urllib

# Home-brew
from bitex.auth import BitexAuth


class KrakenAuth(BitexAuth):
    """Customized implementation of BitexAuth for Kraken."""

    @property
    def b64_decoded_secret(self) -> bytes:
        return base64.b64decode(self.secret)

    def hash_json_dict(self, json_dict) -> bytes:
        urlencoded_params = urllib.parse.urlencode(json_dict)

        byte_encoded_params = (str(json_dict["nonce"]) + urlencoded_params).encode("utf-8")
        hashed_params = hashlib.sha256(byte_encoded_params).digest()
        return hashed_params

    def create_signature_hash(self, encoded_body: bytes, request_url) -> str:
        _, url_endpoint = request_url.split("/0/")
        hmac_message = url_endpoint.encode("utf-8") + encoded_body

        signature = hmac.new(self.b64_decoded_secret, hmac_message, hashlib.sha512)
        digested_signature = signature.digest()
        b64_encoded_signature = base64.b64encode(digested_signature)
        unicode_signature = b64_encoded_signature.decode("utf-8")
        return unicode_signature

    def __call__(self, request):
        decoded_body = self.decode_body(request)

        json_dict = {k: v for k, v in decoded_body}
        json_dict["nonce"] = self.nonce()

        hashed_params = self.hash_json_dict(json_dict)

        new_headers = {
            "API-Key": self.key,
            "API-Sign": self.create_signature(hashed_params, request.url),
        }

        request.headers.update(new_headers)
        request.body = json.dumps(json_dict).encode("utf-8")
        return request
