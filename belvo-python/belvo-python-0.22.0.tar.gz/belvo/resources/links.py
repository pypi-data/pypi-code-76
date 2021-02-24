import warnings
from typing import Dict, List, Optional, Union

from belvo.enums import AccessMode
from belvo.resources.base import Resource
from belvo.utils import read_file_to_b64


class Links(Resource):
    endpoint = "/api/links/"

    def create(
        self,
        institution: str,
        username: str,
        password: str,
        *,
        username2: str = None,
        username3: str = None,
        password2: str = None,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        access_mode: Optional[AccessMode] = None,
        username_type: str = None,
        certificate: str = None,
        private_key: str = None,
    ) -> Union[List[Dict], Dict]:

        data = {
            "institution": institution,
            "username": username,
            "password": password,
            "save_data": save_data,
            "access_mode": access_mode and access_mode.value,
            "username2": username2,
            "username3": username3,
            "password2": password2,
            "token": token,
            "encryption_key": encryption_key,
            "username_type": username_type,
            "certificate": certificate and read_file_to_b64(certificate),
            "private_key": private_key and read_file_to_b64(private_key),
        }

        clean_data = {key: value for key, value in data.items() if value}

        return self.session.post(self.endpoint, data=clean_data, raise_exception=raise_exception)

    def update(
        self,
        link: str,
        *,
        password: str = None,
        password2: str = None,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        username_type: str = None,
        certificate: str = None,
        private_key: str = None,
    ) -> Union[List[Dict], Dict]:

        data = {
            "password": password,
            "save_data": save_data,
            "password2": password2,
            "token": token,
            "encryption_key": encryption_key,
            "username_type": username_type,
            "certificate": certificate and read_file_to_b64(certificate),
            "private_key": private_key and read_file_to_b64(private_key),
        }

        clean_data = {key: value for key, value in data.items() if value}

        return self.session.put(
            self.endpoint, id=link, data=clean_data, raise_exception=raise_exception
        )

    def token(
        self, link: str, scopes: str, *, raise_exception: bool = False
    ) -> Union[List[Dict], Dict]:
        from belvo.resources import WidgetToken

        warnings.warn(
            "Please make use of `client.WidgetToken.create(link=<link:uuid>)` "
            "to request a link scoped token instead.",
            DeprecationWarning,
        )

        token = WidgetToken(self.session)
        return token.create(scopes=scopes, link=link, raise_exception=raise_exception)
