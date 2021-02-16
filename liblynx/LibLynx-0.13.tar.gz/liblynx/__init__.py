__version__ = "0.13"
import logging
import os
import time
from email.utils import parsedate
import requests


def make_url(path):
    BASE = os.environ.get("LIBLYNX_BASE") or "https://sandbox.liblynx.com"
    return "%s%s" % (BASE, path)


class APICallException(Exception):
    pass


def if_success(arequest, msg, successcode=200):
    if arequest.status_code == successcode:
        logging.debug("%s worked" % msg)
        return arequest.json()
    else:
        raise APICallException(
            "%s failed. status: %s %s" % (msg, arequest.status_code, arequest.text)
        )


class Connect:
    def __init__(self, client_id=None, client_secret=None):
        client_id = client_id or os.environ.get("LIBLYNX_CLIENT_ID")
        if not client_id:
            raise Exception(
                "client_id not specified nor found from ENV LIBLYNX_CLIENT_ID"
            )
        self.client_id = client_id
        client_secret = client_secret or os.environ.get("LIBLYNX_CLIENT_SECRET")
        if not client_secret:
            raise Exception(
                "client_secret not specified nor found from ENV LIBLYNX_CLIENT_SECRET"
            )
        self.client_secret = client_secret
        self.CACHE = {}

    def __getattr__(self, attr):
        value, expiry = self.CACHE.get(attr, (None, 0))
        if time.time() > expiry:
            getter = "_get_%s" % attr
            logging.debug("%s expired, trying getattr with %s" % (attr, getter))
            getter = self.__getattribute__(getter)
            if getter:
                value, expiry = getter()
                logging.debug(
                    "got new value for %s expires at %s" % (attr, time.ctime(expiry))
                )
                self.CACHE[attr] = (value, expiry)
        return value

    def _get_access_token(self):
        r = requests.post(
            make_url("/oauth/v2/token"),
            {"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret),
        )
        if r.status_code == 200:
            r_json = r.json()
            logging.debug("access_token acquired for %s", self.client_id)
            expiry = time.time() + (r_json["expires_in"] - 60)
            return r_json["access_token"], expiry
        logging.error("access_token failed %s %s", r.status_code, r.text)

    def _get_endpoint(self):
        logging.debug("api endpoint expired getting a new one")
        headers = {
            "Authorization": "Bearer %s" % self.access_token,
            "Accept": "application/json",
        }
        r = requests.get(make_url("/api"), headers=headers)
        if r.status_code == 200:
            # Make it one hour less than the expiry
            expires = time.mktime(parsedate((r.headers.get("Expires")))) - (60 * 60)
            api = r.json()
            logging.debug("new api endpoint acquired")
            return api, expires
        else:
            raise APICallException(
                "api endpoint failed %s %s" % (r.status_code, r.text)
            )

    def api(self, msg, href, method="GET", data=None, successcode=200):
        headers = {
            "Authorization": "Bearer %s" % self.access_token,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if method == "GET":
            r = requests.get(href, headers=headers)
        elif method == "PUT":
            r = requests.put(href, json=data, headers=headers)
        elif method == "POST":
            r = requests.post(href, json=data, headers=headers)
        elif method == "DELETE":
            r = requests.delete(href, headers=headers)
            return True
        return if_success(r, msg, successcode)

    def new_identification(self, ip, url, user_agent):
        return self.api(
            "new identification",
            self.endpoint["_links"]["@new_identification"]["href"],
            "POST",
            {"ip": ip, "url": url, "user_agent": user_agent},
            201,
        )

    def identification(self, anid):
        href = self.endpoint["_links"]["@get_identification"]["href"].replace(
            "{id}", anid
        )
        return self.api("get identification", href)


# c.api("new account", c.endpoint["_links"]["@new_account"]["href"], "POST", {"account_name":"LCI Evaluation %s", "subscriptions":[{"title":"Foo", "start": "2020-11-01 10:56:58", "end": "2020-12-01 10:56:58"}]})
