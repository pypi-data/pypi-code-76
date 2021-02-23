import json
import requests
from jwcrypto.jwk import JWK
from revjwt.algorithms import KMSAlgorithm
from jwt.api_jws import PyJWS
from jwt.exceptions import (
    DecodeError,
    InvalidAlgorithmError,
    InvalidSignatureError,
    InvalidTokenError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAudienceError,
    InvalidIssuedAtError,
    InvalidIssuerError,
    MissingRequiredClaimError,
)

class JWS(PyJWS):
    def __init__(self, options=None):
        super().__init__(options)
        self._algorithms = {'RS256': KMSAlgorithm()}

    def decode_complete(
        self,
        jwt,
        key="",
        algorithms=['RS256'],
        options=None,
        **kwargs,
    ):
        if options is None:
            options = {}
        merged_options = {**self.options, **options}
        verify_signature = merged_options["verify_signature"]

        if verify_signature and not algorithms:
            raise DecodeError(
                'It is required that you pass in a value for the "algorithms" argument when calling decode().'
            )

        payload, signing_input, header, signature = self._load(jwt)

        json_payload = json.loads(payload.decode())
        try:
            host, version = json_payload['iss'].split('/')
        except:
            host, version = None, 'v1'
        kid = header['kid']
        env = host.split('.')[0][-4:]
        if env in ['-stg', '-dev']:
            host = 'https://auth-stg.revtel-api.com'
        else:
            host = 'https://auth.revtel-api.com'

        if version == 'v3':
            url = f'{host}/{version}/certs'
            resp = requests.get(url).json()['keys']
            key = [key for key in resp if key['kid'] == kid][0]
        else:
            resp = requests.get('https://keys.revtel-api.com/pub.json').json()
            key = [key for key in resp if key['kid'] == kid][0]
        key = JWK.from_json(json.dumps(key))
        key = key.export_to_pem()

        if verify_signature:
            self._verify_signature(signing_input, header, signature, key, algorithms)

        return {
            "payload": payload,
            "header": header,
            "signature": signature,
        }


_jws = JWS()
encode = _jws.encode
decode = _jws.decode_complete
