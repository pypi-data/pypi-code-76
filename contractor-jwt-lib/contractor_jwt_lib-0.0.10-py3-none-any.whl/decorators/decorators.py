from functools import wraps
from flask import request

from jwt_library.jwt_ops.jwt import verify_token

def jwt_required(iss, aud, client_ids):
   def decorator(func):
       @wraps(func)
       def wrapper(*args, **kwargs):
            try:
                token = request.headers.get("Authorization")
                payload = verify_token(token, iss=iss, aud=aud, client_ids=client_ids)
            except Exception as e:
                return str(e), 401
            if payload:
                return func(*args, **kwargs)
       return wrapper
   return decorator