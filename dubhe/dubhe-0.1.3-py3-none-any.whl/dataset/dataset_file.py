from __future__ import annotations
from dubhe.utils import config
from dubhe.auth import auth
import datetime
from dubhe.utils import http_help
import os
import requests
import urllib
import json
import logging


class DatasetFile(object):
    def __init__(self, dataset_id: str, file_id: str, url: str, name: str, create: datetime.datetime, label: list):
        self.file_id = file_id
        self.url = url
        self.name = name
        self.create = create
        self.dataset_id = dataset_id
        self.label = label
        self.modify = datetime.datetime.min

    def download(self, au: auth.Auth):
        # todo: error check
        filepath = os.path.join(config.HOME, "datasets", self.dataset_id)
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        file = os.path.join(filepath, self.name)

        headers = {
            'token': au.access_token,
        }
        resp = requests.get(self.url, headers=headers)

        if resp.status_code != 200:
            return "download file error"

        with open(file, "wb") as code:
            code.write(resp.content)
        self.modify = datetime.datetime.fromtimestamp(os.stat(filepath).st_mtime, datetime.timezone.utc)
        return None

    def setCls(self, au: auth.Auth, key: str, cls: str) -> (str, int, str):
        # this func has not been tested
        url = urllib.parse.urljoin(au.endpoint, f'/v1/file/{self.file_id}/label/cls')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'token': au.access_token,
        }
        data = {
            'key': key,
            'cls': cls,
        }
        resp = requests.put(url, data=data, headers=headers)
        logging.debug("upload file got:" + resp.text)

        if resp.status_code != 200:
            return None, -1, f'response code = {resp.status_code}'

        try:
            resp_obj = json.loads(resp.text)
            resp_code = resp_obj['error_code']
            if resp_code != 200:
                return None, resp_code, f'response code={resp_code} msg={resp_obj["error_message"]}'

            return "ok", 0, None
        except Exception as e:
            return None, -2, f'unknown error {e}'

    @classmethod
    def _do_request_upload_geturl(cls, au: auth.Auth, dataset_id: str) -> (str, int, str):
        url = urllib.parse.urljoin(au.endpoint, f'/v1/dataset/{dataset_id}/file')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'token': au.access_token,
        }
        data = {}
        resp = requests.post(url, data=data, headers=headers)
        logging.debug("upload file got:" + resp.text)

        if resp.status_code != 200:
            return None, -1, f'response code = {resp.status_code}'

        try:
            resp_obj = json.loads(resp.text)
            resp_code = resp_obj['error_code']
            if resp_code != 200:
                return resp_code, f'response code={resp_code} msg={resp_obj["error_message"]}'

            upload_url = resp_obj['data']['url']
            return upload_url, 0, None
        except Exception as e:
            return None, -2, f'unknown error {e}'

    @classmethod
    def _do_upload_file(cls, au: auth.Auth, url: str, file: object, filename: str) -> (str, int, str):
        headers = {
            # should no header here and will auto file
            'token': au.access_token,
        }

        multiple_files = {
            'file': (filename, file)
        }

        resp = requests.post(url, files=multiple_files, headers=headers)
        logging.debug("upload file got:" + resp.text)

        if resp.status_code != 200:
            return None, -1, f'response code = {resp.status_code}'

        try:
            resp_obj = json.loads(resp.text)
            resp_code = resp_obj['error_code']
            if resp_code != 200:
                return None, resp_code, f'response code={resp_code} msg={resp_obj["error_message"]}'

            return resp_obj['data']['fileId'], 0, None
        except Exception as e:
            return None, -2, f'unknown error {e}'

    @classmethod
    def upload(cls, au: auth.Auth, dataset_id: str, file: object, filename: str) -> (DatasetFile, str):
        url, err = http_help.invoke_with_token(cls._do_request_upload_geturl, lambda f: au.renew_token(force=f),
                                               au=au, dataset_id=dataset_id)
        if err is None:
            file_id, err = http_help.invoke_with_token(cls._do_upload_file, lambda f: au.renew_token(force=f),
                                                   au=au, url=url, file=file, filename=filename)

            ds_file = DatasetFile(dataset_id=dataset_id, file_id=file_id, url=None, name=None, create=None, label=None)

        return ds_file, err
