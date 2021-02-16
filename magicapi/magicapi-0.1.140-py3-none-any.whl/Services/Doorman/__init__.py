from typing import Optional
import requests
from functools import wraps
import time
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .CurrentUser import CurrentUser

from magicapi import g
import firebase_admin
from firebase_admin import auth

from .errors import DoormanAuthException
from magicapi.Decorators.firestore import need_firestore
from magicapi.FieldTypes import PhoneNumber

# from magicapi import settings
from magicapi import g
from magicapi.RouteClasses import MagicCallLogger

import redis

from magicdb import decorate_redis
from magicapi.Services.Sentry import capture_exception

R = None
LAST_SEEN_KEY = "last_seen"
if g.settings.use_doorman_redis:
    R = decorate_redis(
        r=redis.Redis(
            host=g.settings.doorman_redis_endpoint,
            port=g.settings.doorman_redis_port,
            password=g.settings.doorman_redis_password,
            decode_responses=True,
        ),
        error_thrower=capture_exception,
    )


LOCATION, PROJECT_ID, DOORMAN_ID = (
    g.settings.cloud_function_location or "us-central1",
    g.settings.firebase_project_id,
    g.settings.doorman_public_project_id,
)

ID_TOKEN_ENDPOINT: str = (
    f"https://{LOCATION}-{PROJECT_ID}.cloudfunctions.net/getIdToken"
)
DOORMAN_BACKEND_ENDPOINT: str = (
    "https://sending-messages-for-doorman.herokuapp.com/phoneLogic"
)

doorman_prefix = "/doorman"
bare_token_path = f"{doorman_prefix}/token"
token_url = (
    bare_token_path if g.settings.local else f"/{g.settings.stage}{bare_token_path}"
)
oath2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)
oath2_scheme_or_none = OAuth2PasswordBearer(tokenUrl=token_url, auto_error=False)

doorman_router = APIRouter(route_class=MagicCallLogger)


def need_doorman_vars(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        doorman_vars = [LOCATION, PROJECT_ID, DOORMAN_ID]
        if None in doorman_vars:
            raise DoormanAuthException(
                message="Not all Doorman credentials found in .env file. Need DOORMAN_PUBLIC_PROJECT_ID, "
                "FIREBASE_PROJECT_ID, and CLOUD_FUNCTION_LOCATION"
            )
        return f(*args, **kwargs)

    return wrapper


@doorman_router.post("/login_with_phone")
@need_doorman_vars
def login_with_phone(phone_number: PhoneNumber):
    body = {
        "action": "loginWithPhone",
        "phoneNumber": phone_number,
        "publicProjectId": DOORMAN_ID,
    }
    resp = requests.post(DOORMAN_BACKEND_ENDPOINT, json=body).json()
    return resp


def sign_in_with_magic_link(form_data):
    body = {"email": form_data.username, "magicLink": form_data.password}

    magic_link_id_token_endpoint = ID_TOKEN_ENDPOINT.replace(
        "getIdToken", "getIdTokenFromMagicLink"
    )

    id_resp = requests.post(magic_link_id_token_endpoint, json=body).json()
    id_token = id_resp.get("idToken")
    if not id_token:
        print(id_resp)
        raise DoormanAuthException(message=str(id_resp))

    return {"access_token": id_token, "token_type": "bearer"}


@doorman_router.post("/token")
@need_doorman_vars
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if "@" in form_data.username:
        return sign_in_with_magic_link(form_data)
    body = {
        "action": "verifyCode",
        "phoneNumber": form_data.username,
        "code": form_data.password,
        "publicProjectId": DOORMAN_ID,
    }
    resp = requests.post(DOORMAN_BACKEND_ENDPOINT, json=body).json()
    backend_token = resp.get("token")
    if not backend_token:
        print(resp)
        raise DoormanAuthException(message=str(resp))

    id_resp = requests.post(ID_TOKEN_ENDPOINT, json={"token": backend_token}).json()
    id_token = id_resp.get("idToken")
    if not id_token:
        print(id_resp)
        raise DoormanAuthException(message=str(id_resp))

    return {"access_token": id_token, "token_type": "bearer"}


def get_current_user_from_token(token: str):
    try:
        decoded = auth.verify_id_token(token)
        current_user = CurrentUser(**decoded)
        print(
            f"Current User: {current_user.uid}, name: {current_user.display_name}, phone_number: {current_user.phone_number}"
        )
        if R:
            R.zadd(LAST_SEEN_KEY, {current_user.uid: int(time.time())})
        return current_user
    except firebase_admin._token_gen.ExpiredIdTokenError as e:
        print("DOORMAN ERROR", e)
        raise DoormanAuthException(message=e)


@need_firestore
def get_current_user(token: str = Depends(oath2_scheme)):
    return get_current_user_from_token(token=token)


@need_firestore
def get_current_user_or_none(token: Optional[str] = Depends(oath2_scheme_or_none)):
    if not token:
        return None
    current_user = get_current_user_from_token(token)
    return current_user


@need_firestore
def get_current_user_raw(token: str = Depends(oath2_scheme)):
    try:
        decoded = auth.verify_id_token(token)
        return decoded
    except firebase_admin._token_gen.ExpiredIdTokenError as e:
        raise DoormanAuthException(message=e)


from datetime import datetime


def last_seen_from_uid(uid: str) -> Optional[datetime]:
    timestamp_str = R.zscore(LAST_SEEN_KEY, uid)
    if not timestamp_str:
        return None
    return datetime.fromtimestamp(int(timestamp_str))


GET_USER = Depends(get_current_user)
GET_USER_OR_NONE = Depends(get_current_user_or_none)

g.app.include_router(doorman_router, prefix=doorman_prefix, tags=["Doorman"])
