import os
from typing import Optional

from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
from werkzeug.exceptions import Unauthorized
from pydantic import ValidationError

from nidhoggr.core.user import User


TOKEN_EXPIRE = int(os.getenv('TOKEN_EXPIRE'))
SECRET_KEY = os.getenv('SECRET_KEY')

auth = HTTPTokenAuth()


def generate_auth_token(*, user: User) -> str:
    serializer = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=TOKEN_EXPIRE)
    return serializer.dumps(user.json()).decode('ascii')


@auth.error_handler
def auth_failed():
    raise Unauthorized(description="Authentication failed")


@auth.verify_token
def verify_auth_token(token) -> Optional[User]:
    serializer = TimedJSONWebSignatureSerializer(SECRET_KEY)
    try:
        data = serializer.loads(token)
    except SignatureExpired:
        return None
    except BadSignature:
        return None

    try:
        user = User.parse_raw(data)
    except ValidationError:
        return None
    else:
        return user
