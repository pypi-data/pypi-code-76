import os
# import sys

import requests
# import string

from geodesic.oauth import AuthManager

HOST = os.getenv("HOST", "https://geodesic.seerai.space/")
SPACETIME_HOST = os.getenv("SPACETIME_HOST", "https://geodesic.seerai.space/spacetime")
ENTANGLEMENT_HOST = os.getenv(
    "ENTANGLEMENT_HOST", "https://geodesic.seerai.space/entanglement"
)
TESSERACT_HOST = os.getenv("TESSERACT_HOST", "https://geodesic.seerai.space/tesseract")
BOSON_HOST = os.getenv("TESSERACT_HOST", "https://geodesic.seerai.space/boson")
DEBUG = os.getenv("DEBUG", "false")

if DEBUG.lower() in ("1", "true", "yes", "external"):
    DEBUG = True
else:
    DEBUG = False


EXT = os.getenv("GEODESIC_EXTERNAL", "1")
if EXT.lower() in ("1", "true", "yes", "external"):
    EXTERNAL = True
else:
    EXTERNAL = False

    # For the REST API, as used by this client. :)
    if not SPACETIME_HOST.endswith(":8080"):
        SPACETIME_HOST += ":8080"
    if not ENTANGLEMENT_HOST.endswith(":8080"):
        ENTANGLEMENT_HOST += ":8080"
    if not TESSERACT_HOST.endswith(":8080"):
        TESSERACT_HOST += ":8080"
    if not BOSON_HOST.endswith(":8080"):
        BOSON_HOST += ":8080"

    EXTERNAL_HOSTS = {
        "https://geodesic.seerai.space/spacetime": SPACETIME_HOST,
        "https://geodesic.seerai.space/entanglement": ENTANGLEMENT_HOST,
        "https://geodesic.seerai.space/tesseract": TESSERACT_HOST,
        "https://geodesic.seerai.space/boson": BOSON_HOST,
    }

API_VERSION = 1

client = None


def get_client():
    global client
    if client is not None:
        return client

    client = Client()
    return client


class Client:
    def __init__(self):
        self._auth = AuthManager()
        self._session = None
        self._host = HOST
        self._api_version = API_VERSION

    def request(self, uri, method="GET", **params):

        url = HOST
        if url.endswith("/"):
            url = url[:-1]

        # Route request to correct endpoint
        if uri.startswith("/spacetime"):
            uri = uri.replace("/spacetime", "")
            url = SPACETIME_HOST + uri
        elif uri.startswith("/entanglement"):
            uri = uri.replace("/entanglement", "")
            url = ENTANGLEMENT_HOST + uri
        elif uri.startswith("/tesseract"):
            uri = uri.replace("/tesseract", "")
            url = TESSERACT_HOST + uri
        elif uri.startswith("/"):
            url = url + uri

        if uri.startswith("http"):
            url = uri

        if not EXTERNAL:
            for find, replace in EXTERNAL_HOSTS.items():
                url = url.replace(find, replace)

        if method == "GET":
            req = requests.Request("GET", url, params=params)
        elif method == "POST":
            req = requests.Request("POST", url, json=params)
        if EXTERNAL:
            req.headers["Authorization"] = "Bearer {0}".format(self._auth.id_token)

        if self._session is None:
            self._session = requests.Session()

        prepped = req.prepare()
        res = self._session.send(prepped)

        try:
            res = res.json()
            if "error" in res:
                raise Exception("an error occurred: {0}".format(res["error"]))
            return res
        except Exception as e:
            if not isinstance(res, dict):
                print("response: '{0}...'".format(res.text[:200]))
            raise Exception("an error occured: {0}".format(e))

    def get(self, uri, **query):
        return self.request(uri, method="GET", **query)

    def post(self, uri, **body):
        return self.request(uri, method="POST", **body)
