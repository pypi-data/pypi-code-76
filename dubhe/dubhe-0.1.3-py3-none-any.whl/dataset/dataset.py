from __future__ import annotations
from dubhe.auth import auth
from dubhe.utils import http_help
from dubhe.utils import time
from dubhe.dataset import dataset_file
from dubhe.dataset import datasetpo
from dubhe.utils import config
import requests
import urllib
import json
import logging
import typing
import os


class Dataset(object):
    def __init__(self, au: auth.Auth, workspace_id: str, name: str, description: str, encrypted: bool,
                 dataset_id: str = None):
        self.au = au
        self.workspace_id = workspace_id
        self.name = name
        self.description = description
        self.encrypted = encrypted
        self.dataset_id = dataset_id

    @classmethod
    def _do_request_list_all(cls, au: auth.Auth, workspace_id: str) -> (list, int, str):
        url = urllib.parse.urljoin(au.endpoint, f'/v1/dataset/workspace/' + workspace_id)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'token': au.access_token,
        }
        data = {}
        resp = requests.get(url, data=data, headers=headers)
        logging.debug("renew got:" + resp.text)

        if resp.status_code != 200:
            logging.debug("get all dataset error:", resp.status_code)
            return None, -1, f'response code = {resp.status_code}'

        try:
            resp_obj = json.loads(resp.text)
            logging.debug("resp_obj =" + str(resp_obj))
            resp_code = resp_obj['error_code']
            if resp_code != 200:
                return None, resp_code, f'response code={resp_code} msg={resp_obj["error_message"]}'

            dspos = []
            dss = resp_obj['data']
            for ds in dss:
                dspo = Dataset(au, workspace_id, ds['name'], ds['description'], ds['encrypted'],
                               dataset_id=ds['dataset_id'])
                dspos.append(dspo)
            return dspos, 0, None
        except Exception as e:
            return None, -2, f'unknown error {e}'

    @classmethod
    def list_all(cls, au: auth.Auth, workspace_id: str) -> (list, str):
        _, _, err = au.renew_token()
        if err is not None:
            return None, "renew token error"

        dss, err_code, err_msg = cls._do_request_list_all(au, workspace_id)
        if err_code == 497:  # token error
            _, _, err = au.renew_token(force=True)
            if err is not None:
                return None, "renew token error"

            dss, err_code, err_msg = cls._do_request_list_all(au, workspace_id)
        return dss, err_msg

    def _do_request_add(self) -> (int, str):
        url = urllib.parse.urljoin(self.au.endpoint, f'/v1/dataset/workspace/{self.workspace_id}')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'token': self.au.access_token,
        }
        data = {
            'name': self.name,
            'description': self.description,
            'encrypted': self.encrypted
        }
        resp = requests.post(url, data=data, headers=headers)
        logging.debug("new dataset got:" + resp.text)

        if resp.status_code != 200:
            return -1, f'response code = {resp.status_code}'

        try:
            resp_obj = json.loads(resp.text)
            logging.debug("resp_obj =" + str(resp_obj))
            resp_code = resp_obj['error_code']
            if resp_code != 200:
                return resp_code, f'response code={resp_code} msg={resp_obj["error_message"]}'

            self.dataset_id = resp_obj['data']['dataset_id']
            return 0, None
        except Exception as e:
            return -2, f'unknown error {e}'

    def add(self) -> str:
        _, _, err = self.au.renew_token()
        if err is not None:
            return "renew token error"

        err_code, err_msg = self._do_request_add()
        if err_code == 497:  # token error
            _, _, err = self.au.renew_token(force=True)
            if err is not None:
                return "renew token error"

            _, err_msg = self._do_request_add()
        return err_msg

    @classmethod
    def _do_request_getfile_list(cls, au: auth.Auth, dataset_id: str, page: int, size: int) -> (list, int, str):
        url = urllib.parse.urljoin(au.endpoint, f'/v1/dataset/{dataset_id}/files')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'token': au.access_token,
        }
        query = {
            'page': page,
            'size': size
        }
        resp = requests.get(url, params=query, headers=headers)
        logging.debug("list got:" + resp.text)

        if resp.status_code != 200:
            return None, -1, f'response code = {resp.status_code}'

        try:
            resp_obj = json.loads(resp.text)
            logging.debug("resp_obj =" + str(resp_obj))
            resp_code = resp_obj['error_code']
            if resp_code != 200:
                return None, resp_code, f'response code={resp_code} msg={resp_obj["error_message"]}'

            files = []
            for data in resp_obj['data']:
                create_at = time.from_iso_format(data["createAt"])
                file = dataset_file.DatasetFile(dataset_id, data["file_id"], data["url"], data["name"], create_at, data["labels"])
                files.append(file)
            return files, 0, None
        except Exception as e:
            return None, -2, f'unknown erro' \
                             f'' \
                             f'r {e}'

    @classmethod
    def checkout(cls, callback, au: auth.Auth, dataset_id: str) -> str:
        page = 0
        size = 30

        datasetpo.DatasetPo.delete_by_dataset_id(dataset_id)

        # todo: use create time and local modify time to fast checkout
        while True:
            flist, err = http_help.invoke_with_retry(cls._do_request_getfile_list, lambda f: au.renew_token(force=f),
                                                     au=au, dataset_id=dataset_id, page=page, size=size)

            for file in flist:
                file.download(au)

                label = json.dumps(file.label)
                datasetpo.DatasetPo.upsert(dataset_id, file.file_id, file.name, file.create, file.modify, label)
                if callback is not None:
                    callback()

            if len(flist) < size:
                break

            page += 1

    @classmethod
    def load(cls, au: auth.Auth, workspace_id: str, dataset_id: str) -> Dataset:
        dss, err = cls.list_all(au, workspace_id)
        if err is not None:
            return None, err

        for ds in dss:
            if ds.dataset_id == dataset_id:
                return ds, None

    def getCount(self) -> int:
        return datasetpo.DatasetPo.get_count(self.dataset_id)

    def getId(self, index: int):
        # todo, add cache here?
        data_po = datasetpo.DatasetPo.load(self.dataset_id, index, 1)
        return data_po[0].file_id

    def openFile(self, index: int, key: str = "default") -> typing.BinaryIO:
        assert key == "default"  # only support default now
        data_po = datasetpo.DatasetPo.load(self.dataset_id, index, 1)
        if len(data_po) > 0:
            filepath = os.path.join(config.HOME, "datasets", self.dataset_id, data_po[0].filename)
            return open(filepath, mode='rb')
        else:
            return None

    def getClassification(self, index: int, key: str = "default") -> str:
        data_po = datasetpo.DatasetPo.load(self.dataset_id, index, 1)
        if len(data_po) > 0 and data_po[0].label is not None:
            label_objs = json.loads(data_po[0].label)
            for label in label_objs:
                if label['type'] == 'classification' and label['key'] == key:
                    return label['cls']
        else:
            return None

    def getDetection(self, index: int, key: str = "default") -> typing.List:
        pass

    def getMetadata(self, index: int, key: str = "default") -> str:
        data_po = datasetpo.DatasetPo.load(self.dataset_id, index, 1)
        if len(data_po) > 0 and data_po[0].label is not None:
            label_objs = json.loads(data_po[0].label)
            for label in label_objs:
                if label['type'] == 'metadata' and label['key'] == key:
                    return label['metaValue']
        else:
            return None







