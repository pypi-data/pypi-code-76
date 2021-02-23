from __future__ import annotations
import requests
import urllib
import json
import datetime
import logging
from dubhe.utils import time
from dubhe.auth import authpo


class Auth(object):
    def __init__(self, name: str, user_id: str, token: str, endpoint: str
                 , expiry: str = None, access_token: str = None, is_active: bool = False) -> type(None):
        self.name = name
        self.user_id = user_id
        self.token = token
        self.endpoint = endpoint
        self.expiry = time.from_iso_format(expiry) if expiry is not None else None
        self.access_token = access_token
        self.is_active = is_active

    def _do_renew_token(self) -> (str, datetime.datetime, str):
        url = urllib.parse.urljoin(self.endpoint, f'/v1/auth/{self.user_id}/renew')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        }
        data = {'refreshToken': self.token}
        resp = requests.post(url, data=data, headers=headers)
        logging.debug("renew got:" + resp.text)

        if resp.status_code != 200:
            print("renew token error:", resp.status_code)
            return None, None, f'response code = {resp.status_code}'

        try:
            resp_obj = json.loads(resp.text)
            logging.debug("resp_obj =" + str(resp_obj))
            if resp_obj['error_code'] != 200:
                return None, None, f'response code={resp_obj["error_code"]} msg={resp_obj["error_message"]}'

            exp_str = resp_obj['data']['expiryDate']
            self.expiry = time.from_iso_format(exp_str)
            self.access_token = resp_obj['data']['accessToken']
            return self.access_token, self.expiry, None
        except Exception as e:
            return None, None, f'unknown error {e}'

    def renew_token(self, store=True, force=False):
        renew = True
        if not force:
            if self.access_token is not None or self.expiry is not None:
                exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)  # 1min as buffer
                if self.expiry.time() > exp.time():
                    renew = False

        if renew:
            at, exp, err = self._do_renew_token()
            if store and err is None:
                self.store()
            return at, exp, err
        else:
            return self.access_token, self.expiry, None

    def store(self) -> int:
        if self.is_active:
            active_time = datetime.datetime.utcnow()
        else:
            active_time = 0

        ret = authpo.AuthPo.upsert(name=self.name
                                   , user_id=self.user_id
                                   , token=self.token
                                   , endpoint=self.endpoint
                                   , expiry=self.expiry
                                   , access_token=self.access_token
                                   , active_time=active_time)

        return ret

    @classmethod
    def load_all(cls) -> list:
        auths = authpo.AuthPo.load_all()

        max = datetime.datetime.min
        for auth in auths:
            try:
                if auth.active_time > max:
                    max = auth.active_time
            except Exception as e:
                pass

        auth_list = []
        for auth in auths:
            au = Auth(auth.name, auth.user_id, auth.token, auth.endpoint, auth.expiry, auth.access_token, False)
            if auth.active_time == max:
                au.is_active = True

            auth_list.append(au)

        return auth_list

    @classmethod
    def load_active(cls) -> Auth:
        auth = authpo.AuthPo.load_active()
        if auth:
            au = Auth(auth.name, auth.user_id, auth.token, auth.endpoint, auth.expiry, auth.access_token, True)
            return au
        else:
            return None
