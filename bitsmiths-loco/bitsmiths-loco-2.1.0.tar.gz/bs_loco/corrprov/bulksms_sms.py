# **************************************************************************** #
#                           This file is part of:                              #
#                                BITSMITHS                                     #
#                           https://bitsmiths.co.za                            #
# **************************************************************************** #
#  Copyright (C) 2015 - 2021 Bitsmiths (Pty) Ltd.  All rights reserved.        #
#   * https://bitbucket.org/bitsmiths_za/bitsmiths                             #
#                                                                              #
#  Permission is hereby granted, free of charge, to any person obtaining a     #
#  copy of this software and associated documentation files (the "Software"),  #
#  to deal in the Software without restriction, including without limitation   #
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
#  and/or sell copies of the Software, and to permit persons to whom the       #
#  Software is furnished to do so, subject to the following conditions:        #
#                                                                              #
#  The above copyright notice and this permission notice shall be included in  #
#  all copies or substantial portions of the Software.                         #
#                                                                              #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     #
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  #
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
#  DEALINGS IN THE SOFTWARE.                                                   #
# **************************************************************************** #
import base64
import datetime
import json
import os.path
import ssl
import urllib
import urllib.parse
import urllib.request

from bs_lib.Pod   import Pod

from bs_loco.db.tables      import tMsg

from .provider_sms import ProviderSms

from bs_lib  import Common


class BulkSMSSms(ProviderSms):
    """
    The Bulk SMS provider
    """

    def __init__(self):
        """
        Constructor.
        """
        ProviderSms.__init__(self)


    def id(self) -> str:
        """
        Overload.
        """
        return 'bulksms'


    def initialize(self, pod: Pod, dao: object, cfg: dict):
        """
        Overload.
        """
        ProviderSms.initialize(self, pod, dao, cfg)

        Common.readDict(self._cfg, 'url',           str)
        Common.readDict(self._cfg, 'token',         str)
        Common.readDict(self._cfg, 'token-secret',  str)


    def destroy(self):
        """
        Overload.
        """
        self._client = None
        ProviderSms.destroy(self)


    def _provider_send(self, payload: dict, res_list: list, msg: tMsg, addr_list: list) -> tuple:
        """
        Overload.
        """
        try:
            dt_start = datetime.datetime.now()

            bs_tok = os.path.expandvars(self._cfg['token'])
            bs_sec = os.path.expandvars(self._cfg['token-secret'])

            for addr in addr_list:

                api_payload = {
                    "to"   : addr,
                    "body" : payload['msg'],
                }

                content = bytes(json.dumps(api_payload), 'utf8')
                auth    = base64.b64encode(bytes('%s:%s' % (bs_tok, bs_sec), 'utf8'))

                local_headers = {
                    'Content-Type'  : 'application/json',
                    'Authorization' : 'Basic %s' % str(auth, 'utf8'),
                }

                ctx                = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode    = ssl.CERT_NONE

                conn = urllib.request.Request(
                    self._cfg['url'],
                    data    = content,
                    method  = 'POST',
                    headers = local_headers)

                try:
                    with urllib.request.urlopen(conn, timeout=30.0, context=ctx) as resp:
                        resp.read()

                except urllib.request.HTTPError as ex:
                    raise Exception('BulkSMS failed: [errCode:%s, msg:%s]' % (ex.getcode(), ex.read()))

            dt_end = datetime.datetime.now()
        except Exception as x:
            self._log.error('Exception caught sending sms [%s]' % (str(msg)))
            self._log.exception(x)
            return (False, None, str(x))

        return (True, dt_end - dt_start, None)
