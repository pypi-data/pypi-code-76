# -*- coding: utf-8 -*-


import re
import base64
import json
import logging
import codecs
import requests
from .misc import quote_plus, urlencode, is_ssl, HTTPConnection, HTTPSConnection, ExceptionAuth, native_str

if is_ssl:
    import ssl


class ExceptionRecursiveRet(Exception):
    pass


class AuthenticationFailedException(Exception):
    pass


class ExceptionCodeRet(Exception):
    pass


class REST_ClientError(Exception):
    pass


PREFIX_CURSOR_UP = "__GSQL__MOVE__CURSOR___UP__"
PREFIX_CLEAN_LINE = "__GSQL__CLEAN__LINE__"
PREFIX_INTERACT = "__GSQL__INTERACT__"
PREFIX_RET = "__GSQL__RETURN__CODE__"
PREFIX_COOKIE = "__GSQL__COOKIES__"

FILE_PATTERN = re.compile("@[^@]*[^;,]")
PROGRESS_PATTERN = re.compile("\\[=*\\s*\\]\\s[0-9]+%.*")
COMPLETE_PATTERN = re.compile("\\[=*\\s*\\]\\s100%[^l]*")
TOKEN_PATTERN = re.compile("- Token: ([^ ]+) expire at: (.+)")

NULL_MODE = 0
VERTEX_MODE = 1
EDGE_MODE = 2
GRAPH_MODE = 3
JOB_MODE = 4
QUERY_MODE = 5
TUPLE_MODE = 6

CATALOG_MODES = {
    "Vertex Types": VERTEX_MODE,
    "Edge Types": EDGE_MODE,
    "Graphs": GRAPH_MODE,
    "Jobs": JOB_MODE,
    "Queries": QUERY_MODE,
    "User defined tuples": TUPLE_MODE
}


def _is_mode_line(line):
    return line.endswith(":")


def _get_current_mode(line):
    return CATALOG_MODES.get(line[:-1], NULL_MODE)


VERSION_COMMIT = {
    "2.4.0": "f6b4892ad3be8e805d49ffd05ee2bc7e7be10dff",
    "2.4.1": "47229e675f792374d4525afe6ea10898decc2e44",
    "2.5.0": "bc49e20553e9e68212652f6c565cb96c068fab9e",
    "2.5.2": "291680f0b003eb89da1267c967728a2d4022a89e",
    "2.6.0": "6fe2f50ab9dc8457c4405094080186208bd2edc4",
    "2.6.2": "47be618a7fa40a8f5c2f6b8914a8eb47d06b7995",
    "3.0.0": "c90ec746a7e77ef5b108554be2133dfd1e1ab1b2",
    "3.0.5": "a9f902e5c552780589a15ba458adb48984359165",
    "3.1.0": "e9d3c5d98e7229118309f6d4bbc9446bad7c4c3d",

}


class GSQL_Client(object):

    def __init__(self, server_ip="127.0.0.1", username="tigergraph", password="tigergraph", local=False, cacert="",
                 version="", protocol="https", gsPort="14240", commit="", graph="", token=""):
        self.request_session = requests.Session()
        self._logger = logging.getLogger("gsql_client.Client")
        self._server_ip = server_ip
        self.username = username
        self.password = password
        self.graph = graph
        self.gsPort = gsPort
        self.token = token
        if commit:
            self._client_commit = commit
        elif version in VERSION_COMMIT:
            self._client_commit = VERSION_COMMIT[version]
        else:
            self._client_commit = ""

        self._version = version

        if self._version and self._version >= "2.3.0":
            self._abort_name = "abortclientsession"
        else:
            self._abort_name = "abortloadingprogress"

        self.protocol = protocol
        if self.protocol == "https":
            self._context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            self._context.check_hostname = False
            self._context.verify_mode = ssl.CERT_REQUIRED
            if cacert:
                self._context.load_verify_locations(cacert)
            else:
                pass
                # Todo : Get CACERT from url provided
        else:
            self._context = None
        self.base64_credential = base64.b64encode(
            "{0}:{1}".format(self.username, self.password).encode("utf-8")).decode("utf-8")

        self.is_local = local

        if self.is_local:
            self._base_url = "/gsql/"
            if ":" not in server_ip:
                port = self.gsPort
                self._server_ip = "{0}:{1}".format(server_ip, port)
        else:
            self._base_url = "/gsqlserver/gsql/"  #
            if ":" not in server_ip:
                self._server_ip = "{0}:{1}".format(server_ip, self.gsPort)

        self.initialize_url()

        self.session = ""
        self.properties = ""
        if self.protocol == "https":
            self.gsqlUrl = "https://" + self._server_ip + self._base_url

        else:
            self.gsqlUrl = "http://" + self._server_ip + self._base_url
        self.cookie = {}
        self.authorization = 'Basic {0}'.format(self.base64_credential)

    def setGraph(self, graph):
        self.graph = graph

    def initialize_url(self):
        self.command_url = self._base_url + "command"
        self.version_url = self._base_url + "version"
        self.help_url = self._base_url + "help"
        self.login_url = self._base_url + "login"
        self.reset_url = self._base_url + "reset"
        self.file_url = self._base_url + "file"
        self.dialog_url = self._base_url + "dialog"
        self.conn = None
        self.info_url = self._base_url + "getinfo"
        self.abort_url = self._base_url + self._abort_name

    def get_cookie(self):

        cookie = {}

        if self.graph:
            cookie["graph"] = self.graph
        cookie["fromGsqlClient"] = True
        if self.session:
            cookie["sessionId"] = self.session

        cookie["serverId"] = "1_1613327897156"

        if self.properties:
            cookie["properties"] = self.properties

        if self._client_commit:
            cookie["commitClient"] = self._client_commit

        return json.dumps(cookie, ensure_ascii=True)

    def set_cookie(self, cookie_str):

        cookie = json.loads(cookie_str)
        self.session = cookie.get("sessionId", "")
        self.graph = cookie.get("graph", "")
        self.properties = cookie.get("properties", "")

    def setToken(self, token):
        self.token = token

    def _setup_connection(self, url, content, cookie=None, auth=True):

        if self.protocol == "https":
            ssl._create_default_https_context = ssl._create_unverified_context
            conn = HTTPSConnection(self._server_ip)
        else:
            conn = HTTPConnection(self._server_ip)
        encoded = quote_plus(content.encode("utf-8"))
        cookie_value = self.get_cookie() if cookie is None else cookie
        headers = {
            "Content-Language": "en-US",
            "Content-Length": str(len(encoded)),
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Java/1.8.0",
            "Cookie": cookie_value
        }

        if auth:
            headers["Authorization"] = self.authorization

        URI = self.protocol+"://"+self._server_ip+url

        res = self.request_session.post(URI,headers=headers,data=encoded)
        # conn.request("POST", url, encoded, headers)

        return res
    def request(self, url, content, handler=None, cookie=None, auth=True):
        response = None
        try:
            r = self._setup_connection(url, content, cookie, auth)
            # response = r.getresponse()
            response = r
            # ret_code = response.status
            ret_code = r.status_code
            if ret_code == 401:
                raise AuthenticationFailedException("Invalid Username/Password!")
            if handler:
                # reader = codecs.getreader("utf-8")(r.content)
                reader = r.text.split("\n")
                return handler(reader)
            else:
                return response.content.decode("utf-8")
        finally:
            if response:
                response.close()

    def _dialog(self, response):

        self._request(self.dialog_url, response)

    def command_interactive(self, url, content, ans="", out=False):

        def __handle__interactive(reader):

            res = []
            for line in reader:
                line = line.strip()
                if line.startswith(PREFIX_RET):
                    # ! print(line)
                    import time
                    time.sleep(5000)
                    _, ret = line.split(",", 1)
                    ret = int(ret)
                    if ret != 0:
                        raise ExceptionCodeRet(ret)
                elif line.startswith(PREFIX_INTERACT):
                    _, it, ik = line.split(",", 2)
                    if it in {"DecryptQb", "AlterPasswordQb", "CreateUserQb", "CreateTokenQb", "ClearStoreQb"} \
                            and ans:
                        self._dialog("{0},{1}".format(ik, ans))
                elif line.startswith(PREFIX_COOKIE):
                    _, cookie_s = line.split(",", 1)
                    self.set_cookie(cookie_s)
                    # print(cookie_s)
                elif line.startswith(PREFIX_CURSOR_UP):
                    values = line.split(",")
                    print("\033[" + values[1] + "A")
                elif line.startswith(PREFIX_CLEAN_LINE):
                    print("\033[2K")
                elif PROGRESS_PATTERN.match(line):
                    if COMPLETE_PATTERN.match(line):
                        line += "\n"
                    print("\r" + line)
                else:
                    if out:
                        print(line)
                    res.append(line)
            return res

        return self.request(url, content, __handle__interactive)

    def login(self, commit_try="", version_try=""):

        if self._client_commit == "" and commit_try == "":
            for k in VERSION_COMMIT:
                if (self.login(version_try=k, commit_try=VERSION_COMMIT[k]) == True):
                    break
        elif commit_try != "":
            self._client_commit = commit_try
            self._version = version_try
        response = None
        try:
            Cookies = {}
            Cookies['clientCommit'] = self._client_commit
            r = self._setup_connection(self.login_url, self.base64_credential, cookie=json.dumps(Cookies), auth=False)
            response = r.getresponse()
            ret_code = response.status
            # print(response.status)
            if ret_code == 200:
                content = response.read()
                res = json.loads(content.decode("utf-8"))
                # print(res)
                import time
                time.sleep(1)
                if "License expired" in res.get("message", ""):
                    raise Exception("TigerGraph Server License is expired! Please update your license!")

                compatible = res.get("isClientCompatible", True)
                if not compatible:
                    # print("This client is not compatible with target TigerGraph Server!  Please specify a correct version when creating this client!")
                    return False

                if res.get("error", False):
                    if "Wrong password!" in res.get("message", ""):
                        raise ExceptionAuth("Invalid Username/Password!")
                    else:
                        raise Exception("Login failed!")
                else:
                    self.session = response.getheader("Set-Cookie")
                    return True
        finally:
            if response:
                response.close()

    def _setup_connectionpp(self, method, endpoint, parameters, content,headers):
        url = native_str(endpoint)
        if parameters:
            param_str = native_str(urlencode(parameters))
            if param_str:  # not None nor Empty
                url += "?" + param_str

        _headers = {
            "Content-Language": "en-US",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json"
        }
        if headers:
            _headers.update(headers)
        if content:
            encoded = content.encode("utf-8")
            _headers["Content-Length"] = str(len(encoded))
        else:
            encoded = None

        if self.token:
            _headers["Authorization"] = "Bearer {0}".format(self.token)
        elif self.username and self.password:
            _headers["Authorization"] = 'Basic {0}'.format(self.base64_credential)

        if self.protocol == "https":
            ssl._create_default_https_context = ssl._create_unverified_context
            conn = HTTPSConnection(self._server_ip)
        else:
            conn = HTTPConnection(self._server_ip)
        conn.request(method, url, encoded, _headers)
        return conn

    def _errorCheck(self, res):
        if "error" in res and res["error"] and res["error"] != "false":
            raise Exception(res["message"], (res["code"] if "code" in res else None))

    def requestpp(self, method, endpoint, parameters=None, content=None,headers=None, resKey="", skipCheck=False):
        response = None
        try:
            r = self._setup_connectionpp(method, endpoint, parameters, content, headers)
            response = r.getresponse()
            ret_code = response.status
            if ret_code == 401:
                raise ExceptionAuth("Invalid token!")
            response_text = response.read().decode("utf-8")
            self._logger.debug(response_text)
            res = json.loads(response_text, strict=False)
            if not skipCheck:
                self._errorCheck(res)

            if resKey != "":
                return res[resKey]
            return res

        finally:
            if response:
                response.close()

    def get(self, endpoint, parameters=None,headers=None, resKey="", skipCheck=False):
        return self.requestpp("GET", self.gsqlUrl + endpoint, parameters, None, headers, resKey, skipCheck)

    def post(self, endpoint, parameters=None, content=None,headers=None, resKey="", skipCheck=False):
        return self.requestpp("POST", self.gsqlUrl + endpoint, parameters, content, headers, resKey, skipCheck)

    def delete(self, endpoint, parameters=None):
        return self.requestpp("DELETE", self.gsqlUrl + endpoint, parameters, None)

    def execute(self, content, ans="", out=False):
        return self.command_interactive(self.command_url, content, ans, out)


class REST_Client(object):
    def __init__(self, server_ip, protocol, cacert, token, username \
                 , restPort, password):
        self.token = token
        self.restPort = restPort
        self.username = username
        self.password = password
        self.base64_credential = base64.b64encode(
            "{0}:{1}".format(self.username, self.password).encode("utf-8")).decode("utf-8")
        self.protocol = protocol
        if self.protocol == "https":
            self._context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            self._context.check_hostname = False
            self._context.verify_mode = ssl.CERT_REQUIRED
            self._context.load_verify_locations(cacert)
        else:
            self._context = None
        server_ip = native_str(server_ip)

        if ":" in server_ip:
            self._server_ip = server_ip
        else:
            self._server_ip = server_ip + ":" + self.restPort

        self._logger = logging.getLogger("gsql_client.restpp.RESTPP")

    def _setup_connection(self, method, endpoint, parameters, content, headers):
        url = native_str(endpoint)
        if parameters:
            param_str = native_str(urlencode(parameters))
            if param_str:  # not None nor Empty
                url += "?" + param_str

        _headers = {
            "Content-Language": "en-US",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json"
        }
        if headers:
            _headers.update(headers)
        if content:
            encoded = content.encode("utf-8")
            _headers["Content-Length"] = str(len(encoded))
        else:
            encoded = None

        if self.token:
            _headers["Authorization"] = "Bearer {0}".format(self.token)
        elif self.username and self.password:
            _headers["Authorization"] = 'Basic {0}'.format(self.base64_credential)

        if self.protocol == "https":
            ssl._create_default_https_context = ssl._create_unverified_context
            conn = HTTPSConnection(self._server_ip)
        else:
            conn = HTTPConnection(self._server_ip)
        conn.request(method, url, encoded, _headers)
        return conn

    def _errorCheck(self, res):
        if "error" in res and res["error"] and res["error"] != "false":
            raise Exception(res["message"], (res["code"] if "code" in res else None))

    def request(self, method, endpoint, parameters=None, content=None,  headers=None, resKey="", skipCheck=False):
        response = None
        try:
            r = self._setup_connection(method, endpoint, parameters, content, headers)
            response = r.getresponse()
            ret_code = response.status
            if ret_code == 401:
                raise ExceptionAuth("Invalid token!")
            response_text = response.read().decode("utf-8")
            self._logger.debug(response_text)
            res = json.loads(response_text, strict=False)

            if not skipCheck:
                self._errorCheck(res)

            if resKey != '':
                return res[resKey]

            return res
        finally:
            if response:
                response.close()

    def setToken(self, token):
        self.token = token

    #def get(self, path, headers=None, resKey="results", skipCheck=False, params=None):
    def get(self, endpoint, parameters=None, headers=None, resKey="", skipCheck=False):
        return self.request("GET", endpoint, parameters, None, headers, resKey, skipCheck)

    def post(self, endpoint, parameters=None, content=None, headers=None, resKey="", skipCheck=False):
        return self.request("POST", endpoint, parameters, content, headers, resKey, skipCheck)

    def delete(self, endpoint, parameters=None):
        return self.request("DELETE", endpoint, parameters, None)

    def echo(self):
        return self.get("/echo")
