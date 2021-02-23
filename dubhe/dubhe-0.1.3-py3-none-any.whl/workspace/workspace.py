from __future__ import annotations
from dubhe.auth import auth
import requests
import urllib
import json
import logging
from dubhe.utils import propertypo

PROP_KEY = "active.workspace.id"


class Workspace(object):
    def __init__(self, au: auth.Auth, name: str, description: str, workspace_id: str = None):
        self.au = au
        self.name = name
        self.description = description
        self.workspace_id = workspace_id

    def _do_request_add(self) -> (int, str):
        url = urllib.parse.urljoin(self.au.endpoint, f'/v1/workspace')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'token': self.au.access_token,
        }
        data = {
            'name': self.name,
            'description': self.description
        }
        resp = requests.post(url, data=data, headers=headers)
        logging.debug("new workspace got:" + resp.text)

        if resp.status_code != 200:
            return -1, f'response code = {resp.status_code}'

        try:
            resp_obj = json.loads(resp.text)
            logging.debug("resp_obj =" + str(resp_obj))
            resp_code = resp_obj['error_code']
            if resp_code != 200:
                return resp_code, f'response code={resp_code} msg={resp_obj["error_message"]}'

            self.workspace_id = resp_obj['data']['workspace_id']
            return 0, None
        except Exception as e:
            return -2, f'unknown error {e}'

    def add(self) -> str:
        _, _, err = self.au.renew_token()
        if err is not None:
            return None, "renew token error"

        err_code, err_msg = self._do_request_add()
        if err_code == 497:  # token error
            _, _, err = self.au.renew_token(force=True)
            if err is not None:
                return None, "renew token error"

            _, err_msg = self._do_request_add()
        return err_msg

    @classmethod
    def _do_request_list_all(cls, au: auth.Auth) -> (list, int, str):
        url = urllib.parse.urljoin(au.endpoint, f'/v1/workspace')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'token': au.access_token,
        }
        data = {}
        resp = requests.get(url, data=data, headers=headers)
        logging.debug("renew got:" + resp.text)

        if resp.status_code != 200:
            print("renew token error:", resp.status_code)
            return None, -1, f'response code = {resp.status_code}'

        try:
            resp_obj = json.loads(resp.text)
            logging.debug("resp_obj =" + str(resp_obj))
            resp_code = resp_obj['error_code']
            if resp_code != 200:
                return None, resp_code, f'response code={resp_code} msg={resp_obj["error_message"]}'

            wpos = []
            wps = resp_obj['data']
            for wp in wps:
                wpo = Workspace(au, wp['name'], wp['description'], workspace_id=wp['workspace_id'])
                wpos.append(wpo)
            return wpos, 0, None
        except Exception as e:
            return None, -2, f'unknown error {e}'

    @classmethod
    def list_all(cls, au: auth.Auth) -> (list, str):
        _, _, err = au.renew_token()
        if err is not None:
            return None, "renew token error"

        wps, err_code, err_msg = cls._do_request_list_all(au)
        if err_code == 497:  # token error
            _, _, err = au.renew_token(force=True)
            if err is not None:
                return None, "renew token error"

            wps, err_code, err_msg = cls._do_request_list_all(au)
        return wps, err_msg

    @classmethod
    def load(cls, au: auth.Auth, workspace_id: str) -> (Workspace, str):
        wps, err = cls.list_all(au)
        if err is not None:
            return None, err

        for wp in wps:
            if wp.workspace_id == workspace_id:
                return wp, None

        return None, "not found"

    @classmethod
    def store_active(cls, id: str, au: auth.Auth, force=False) -> str:
        wp_id = None

        if force:
            wp_id = id
        else:
            wps, err = cls.list_all(au)
            if err is not None:
                return f'fetch workspace list error: {err}'

            for wp in wps:
                if wp.workspace_id == id:
                    wp_id = id
                    break

        if wp_id is None:
            return f'workspace {id} not found'
        else:
            ret = propertypo.PropertyPo.upsert(PROP_KEY, wp_id)
            if ret >= 0:
                return None
            else:
                return f'upsert db error: {ret}'

    @classmethod
    def load_active_id(cls, au: auth.Auth) -> str:
        po = propertypo.PropertyPo.load(PROP_KEY)
        if po is not None:
            return po.value
        else:
            return None
