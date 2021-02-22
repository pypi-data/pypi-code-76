"""
JWT utilities that simplify and BIG-ify working with the JWT API.
"""
import datetime
import jwt

# JWT issuer
JWT_ISSUER = 'https://big-ideas.bitsinglass.com/iss'
JWT_AUDIENCE = 'https://big-ideas.bitsinglass.com/aud'


def encode_token(secret_key, token_type, **kwargs):
    """
    Creates a JWT token used to carry the state through the Google OAuth2 dance. In addition to the type
    and the data passed in kwargs, this method also embeds the number of claims that get then verified
    when the token is decoded.

    :param secret_key: the key used to sign the JWT token
    :param token_type: the user defined token type used to interpret data passed through kwargs
    :return: the JWT token.
    """
    now = datetime.datetime.utcnow()
    payload = {
        'exp': now + datetime.timedelta(seconds=5*60),
        'nbf': now,
        'iat': now,
        'iss': JWT_ISSUER,
        'aud': JWT_AUDIENCE,
        'type': token_type
    }
    payload.update(kwargs)
    return jwt.encode(payload, secret_key, algorithm="HS256")


def decode_token(secret_key, token):
    """
    Decodes the JWT token created with the `encode_token` method.

    :param secret_key: the key used to sign the JWT token.
    :param token: the token to decode.
    :return: a dictionary with the previously encoded data.
    """
    return jwt.decode(
        token,
        secret_key,
        audience=JWT_AUDIENCE,
        issuer=JWT_ISSUER,
        algorithms=["HS256"],
        options={"require": ["exp", "iss", "nbf", "iat", "aud"]}
    )
