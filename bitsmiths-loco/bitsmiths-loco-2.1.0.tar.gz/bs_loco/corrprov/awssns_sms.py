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
import boto3
import datetime
import os.path

from bs_lib   import Pod
from bs_lib   import common

from bs_loco.db.tables import tMsg

from .provider_sms import ProviderSms


class AwsSnsSms(ProviderSms):
    """
    The AWS Simple Notification Service provider
    """

    def __init__(self):
        """
        Constructor.
        """
        ProviderSms.__init__(self)
        self._client = None


    def id(self) -> str:
        """
        Overload.
        """
        return 'awssns'


    def initialize(self, pod: Pod, dao: object, cfg: dict):
        """
        Overload.
        """
        ProviderSms.initialize(self, pod, dao, cfg)

        common.read_dict(self._cfg, 'aws_access_key_id',      str)
        common.read_dict(self._cfg, 'aws_secret_access_key',  str)
        common.read_dict(self._cfg, 'aws_region',             str)

        self._client = boto3.client("sns",
                                    aws_access_key_id     = os.path.expandvars(cfg['aws_access_key_id']),
                                    aws_secret_access_key = os.path.expandvars(cfg['aws_secret_access_key']),
                                    region_name           = os.path.expandvars(cfg['aws_region']))


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

            for addr in addr_list:
                self._client.publish(PhoneNumber=addr, Message=payload['msg'])

            dt_end = datetime.datetime.now()
        except Exception as x:
            self._log.error('Exception caught sending sms [%s]' % (str(msg)))
            self._log.exception(x)
            return (False, None, str(x))

        return (True, dt_end - dt_start, None)
