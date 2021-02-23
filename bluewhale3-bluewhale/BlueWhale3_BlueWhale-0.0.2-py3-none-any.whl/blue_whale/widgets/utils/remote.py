try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse
import os
import tempfile
import json

import shutil

import requests
import requests.exceptions

from orangecontrib.blue_whale.canvasmain import get_session, set_session
from orangecontrib.blue_whale.i18n_config import *
from collections import OrderedDict

try:
    FileNotFoundError
except:
    FileNotFoundError = IOError

TIMEOUT = 5
INDEX_URL = 'https://bo.dashenglab.com/api/client/'


def __(key):
    return i18n.t("bluewhale.remote." + key)


def _is_prefix(pref, whole):
    if len(pref) > len(whole):
        return False
    for a, b in zip(pref, whole):
        if a != b:
            return False
    return True


def _create_path(target):
    try:
        os.makedirs(target)
    except OSError:
        pass


def get_suffix(data={}):
    type_suffix = data.get("type")
    if type_suffix == "DATA":
        suffix = ".bw"
        path = 'datasets'
    elif type_suffix == "CASE":
        suffix = ".bws"
        path = 'case'
    else:
        return TypeError
    return suffix, path


class Server:
    """A class for listing or downloading files from the server."""
    def __init__(self, username=None, password=None, params=None, data_type=None):
        self.username = username
        self.password = password
        self.params = params
        self.data_type = data_type

        self.req = requests.Session()

        self.req.cookies['SESSION'] = get_session()

        a = requests.adapters.HTTPAdapter(max_retries=2)
        self.req.mount('https://', a)
        self.req.mount('http://', a)

        self._info = None

    def post_remote(self):
        self.req.headers.update({'Content-Type': 'application/json'})
        response = self.req.post(INDEX_URL + "resource/resource/permission", data=json.dumps(self.params))
        if response.status_code == 200:
            active_dict = {(name['id'],): name['name'] for name in response.json() if name['active']}
            remote_category_list = [category['categoryIds'] for category in response.json() if category['active']]
            category_dict = OrderedDict()
            for remote_category in remote_category_list:
                for category in remote_category:
                    category_dict[category['categoryName']] = (category['id'], )

            resource_dict = {name['id']: [(i['id'],) for i in name['categoryIds']] for name in response.json() if
                             name['active']}

            return active_dict, category_dict, resource_dict
        else:
            return {}, OrderedDict(), {}

    def _server_request(self, *path):
        auth = None
        if self.username and self.password:
            auth = (self.username, self.password)
        if self.params:
            self.data_type.update(self.params)
        if not self.req.cookies.get('SESSION'):
            return None
        return self.req.get(INDEX_URL + "/".join(path), auth=auth,
                            timeout=TIMEOUT, stream=True, params=self.data_type)

    def _open(self, *args):
        return self._server_request(*args)

    def open(self, *args):
        t = self._open(*args)
        if t is None:
            from PyQt5.QtWidgets import QMessageBox
            msg_box = QMessageBox(QMessageBox.Warning, __('warn'), __("warn_text"))
            msg_box.exec_()
            return None
        if t.status_code == 401:
            from PyQt5.QtWidgets import QMessageBox
            msg_box = QMessageBox(QMessageBox.Warning, __('warn'), __("warn.warn_err"))
            msg_box.exec_()
            set_session({"SESSION": None})
            return None
        if t.status_code == 200:
            return json.loads(t.text)

    def _download_server_info(self):
        t = self._open('resource')
        if t.status_code == 200:
            self._info = {}
            suffix, path = get_suffix(self.data_type)
            for d in json.loads(t.text)['content']:
                key = (d['id'], d['id']+suffix)
                self._info[key] = d
        else:
            self._info = False

    def listfiles(self, *args):
        return [a for a in self._info.keys() if _is_prefix(args, a)]

    def info(self, *path):
        """Return a dictionary containing repository file info."""
        self._download_server_info()
        return self._info.get(path, {})

    def allinfo(self, *path):
        """Return all info files in a dictionary, where keys are paths."""
        self._download_server_info()
        files = self.listfiles(*path)
        infos = {}
        for npath in files:
            infos[npath] = self.info(*npath)
        return infos

    def download(self, path, **kwargs):
        """
        Download a file and name it with target name. Callback
        is called once for each downloaded percentage.
        """
        callback = kwargs.get("callback", None)
        target = kwargs.get("target", None)
        _create_path(os.path.dirname(target))

        path = ['resource', 'data', 'download', path]
        req = self._open(*path)  # 下载的是一致的，选择之后，只需要拿出id
        if req.status_code == 404:
            raise FileNotFoundError
        elif req.status_code != 200:
            raise IOError

        size = req.headers.get('content-length')
        if size:
            size = int(size)

        f = tempfile.TemporaryFile()

        chunksize = 1024 * 8
        lastchunkreport = 0.0001

        readb = 0

        for buf in req.iter_content(chunksize):
            readb += len(buf)
            while size and float(readb) / size > lastchunkreport + 0.01:
                lastchunkreport += 0.01
                if callback:
                    callback()
            f.write(buf)

        f.seek(0)
        with open(target, "wb") as fo:
            shutil.copyfileobj(f, fo)

        if callback and not size:  # size was unknown, call callbacks
            for i in range(99):
                callback()

        if callback:
            callback()
