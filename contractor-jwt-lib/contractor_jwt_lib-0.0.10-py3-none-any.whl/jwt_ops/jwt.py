import requests

from jose import jwk, jwt
from jose.utils import base64url_decode
from okta_jwt.utils import verify_exp, verify_aud, check_presence_of, verify_iat, verify_iss, verify_cid

JWKS_CACHE = {}
PREFIX = 'Bearer '

def create_signed_jwt(key, claims=None):
    # k = {"k": "<private key>", "kty": "RSA"}
    Token = jwt.JWT(claims=claims)
    Token.make_signed_token(key)
    return Token.serialize()

def decode_jwt(key, payload):
    ST = jwt.JWT(key=key, jwt=payload)
    return ST

def get_claims(token):
    return token.claims()

def verify_token(header, iss, aud, client_ids):

    # Client ID's list
    clid_list = []

    try:
        token = fetch_token_from_header(header)
    except ValueError as ve:
        raise ve

    if not isinstance(client_ids, list):
        clid_list = client_ids.split(',')
    else:
        clid_list = client_ids

    check_presence_of(token, iss, aud, clid_list)

    # Decoding header and payload from token
    header = jwt.get_unverified_header(token)
    payload = jwt.get_unverified_claims(token)

    # Verifying claims
    verify_claims(payload, iss, aud, clid_list)

    jwks_key = fetch_jwk_for(header, payload)
    key = jwk.construct(jwks_key)
    message, encoded_sig = token.rsplit('.', 1)
    decoded_sig = base64url_decode(encoded_sig.encode('utf-8'))

    valid = key.verify(message.encode(), decoded_sig)

    if valid == True:
        return payload
    else:
        raise Exception('Invalid Token')

def fetch_jwk_for(header, payload):
    # Extracting kid from Header
    if 'kid' in header:
        kid = header['kid']
    else:
        raise ValueError('Token header is missing "kid" value.')

    global JWKS_CACHE

    if JWKS_CACHE:
        if kid in JWKS_CACHE:
            return JWKS_CACHE[kid]

    # Fetching jwk
    url = fetch_metadata_for(payload)['jwks_uri']

    try:
        jwks_response = requests.get(url)

        # Consider any status other than 2xx an error
        if not jwks_response.status_code // 100 == 2:
            raise Exception(jwks_response.text, jwks_response.status_code)
    except requests.exceptions.RequestException as e:
        # A serious problem happened, like an SSLError or InvalidURL
        raise Exception("Error: {}".format(str(e)))

    jwks = list(filter(lambda x: x['kid'] == kid, jwks_response.json()['keys']))
    if not len(jwks):
        raise Exception("Error: Could not find jwk for kid: {}".format(kid))
    jwk = jwks[0]

    # Adding JWK to the Cache
    JWKS_CACHE[kid] = jwk

    return jwk

def fetch_metadata_for(payload):
    # Extracting client_id and issuer from the Payload
    client_id = payload['cid']
    issuer    = payload['iss']

    # Preparing URL to get the metadata
    url = "{}/.well-known/oauth-authorization-server?client_id={}".format(issuer, client_id)

    try:
        metadata_response = requests.get(url)

        # Consider any status other than 2xx an error
        if not metadata_response.status_code // 100 == 2:
            raise Exception(metadata_response.text, metadata_response.status_code)

        json_obj = metadata_response.json()
        return json_obj

    except requests.exceptions.RequestException as e:
        # A serious problem happened, like an SSLError or InvalidURL
        raise Exception("Error: {}".format(str(e)))

def verify_claims(payload, issuer, audience, cid_list):
    """ Validates Issuer, Client IDs, Audience
    Issued At time and Expiration in the Payload
    """
    verify_iss(payload, issuer)
    verify_cid(payload, cid_list)
    verify_aud(payload, audience)
    verify_exp(payload)
    verify_iat(payload)

def fetch_token_from_header(token):
    if not token or not token.startswith(PREFIX):
        raise ValueError('Invalid token')

    return token[len(PREFIX):]

def fetch_payload_from_token(token):
    return jwt.get_unverified_claims(token)