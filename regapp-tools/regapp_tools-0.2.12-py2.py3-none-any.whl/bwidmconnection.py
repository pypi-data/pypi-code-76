'''Connection to bwidmm
this is a carbon copy of https://git.scc.kit.edu/feudal/feudalAdapterLdf/-/blob/master/ldf_adapter/backend/bwidm.py'''
# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy, logging-format-interpolation
# pylint: disable=missing-docstring, trailing-whitespace, trailing-newlines, too-few-public-methods

import logging
from sys import exit as s_exit
from urllib.parse import urljoin
from functools import reduce
import requests
import json

from .config import CONFIG

logger = logging.getLogger(__name__)

class BwIdmConnection:
    """Connection to the BWIDM API."""
    def __init__(self, config=None):
        self.session = requests.Session()
        if config:
            self.session.auth = (
                config['backend.bwidm.auth']['http_user'],
                config['backend.bwidm.auth']['http_pass']
            )

    def get(self, *url_fragments, **kwargs):
        logger.debug(F"Url fragments: {url_fragments}")
        return self._request('GET', url_fragments, **kwargs)

    def post(self, *url_fragments, **kwargs):
        return self._request('POST', url_fragments, **kwargs)

    def _request(self, method, url_fragments, **kwargs):
        """
        Arguments:
        method -- HTTP Method (type: str)
        url_fragments -- The components of the URL. Each is url-encoded separately and then they are
                         joined with '/'
        fail=True -- Raise exception on non-200 HTTP status
        **kwargs -- Passed to `requests.Request.__init__`
        """
        fail = kwargs.pop('fail', True)

        url_fragments = map(str, url_fragments)
        url_fragments = map(lambda frag: requests.utils.quote(frag, safe=''), url_fragments)
        url = reduce(lambda acc, frag: urljoin(acc, frag) if acc.endswith('/') else urljoin(acc+'/', frag),
                     url_fragments,
                     CONFIG['backend.bwidm']['url'])
        logger.debug(url+"\n")

        req = requests.Request(method, url, **kwargs)
        rsp = self.session.send(self.session.prepare_request(req))

        import simplejson
        try:
            resp_json = rsp.json()
            resp = json.dumps(resp_json, sort_keys=True, indent=4, separators=(',', ': '))
        except json.JSONDecodeError:
            resp = rsp.text
        except simplejson.errors.JSONDecodeError:
            resp = rsp.text

        # logger.debug(F"    => {resp}")

        if fail:
            if not rsp.ok:
                logger.error("RegApp responded with: {}".format(rsp.content.decode('utf-8')))
                s_exit(1)
            rsp.raise_for_status()

        return rsp

