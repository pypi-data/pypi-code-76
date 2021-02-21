from typing import Dict, Optional
from flask import Flask
from inbot_common.models.user import UserSchema, User
from marshmallow import ValidationError


def _str_no_value(s: Optional[str]) -> bool:
    # Returns True if the given string is None or empty
    if not s:
        return True
    if len(s.strip()) == 0:
        return True
    return False


def load_user(app: Flask, user_data: Dict) -> User:
    try:
        schema = UserSchema()
        # In order to call 'GET_PROFILE_URL' we make sure the user id exists
        if _str_no_value(user_data.get('user_id')):
            user_data['user_id'] = user_data.get('email')
        # Add profile_url from optional 'GET_PROFILE_URL' configuration method.
        # This methods currently exists for the case where the 'profile_url' is not included
        # in the user metadata.
        if _str_no_value(user_data.get('profile_url')) and app.config['GET_PROFILE_URL']:
            user_data['profile_url'] = app.config['GET_PROFILE_URL'](user_data['user_id'])
        data, errors = schema.load(user_data)
        return data
    except ValidationError as err:
        return err.messages


def dump_user(user: User) -> Dict:
    schema = UserSchema()
    try:
        data, errors = schema.dump(user)
        return data
    except ValidationError as err:
        return err.messages


def put_user(app, user_info):
    try:
        return dump_user(load_user(app, user_info))
    except Exception as e:
        print(e)
        return None
