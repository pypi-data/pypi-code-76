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

import datetime
import time
import traceback

from bs_lib.auto_transaction import AutoTransaction
from bs_lib                  import common
from bs_lib                  import query_builder

import bs_loco

from bs_loco.config  import Config

from bs_loco import corrprov


class LocoServer:
    """
    This server monitor for new messages requests processes them to their
    various providers.
    """
    MODULE                = '[LocoServer]'
    PROC_INTERVAL_SLEEP   = 0.2
    MAX_PIPE_OUT_LEN      = 4096
    SCHEDULE_INTERVAL     = 10.0
    MSG_PROC_PER_INTERVAL = 1000

    PROC_TYPE_SEND_MSG    = 'loco-send-msg'


    def __init__(self, pod, dao_name: str, corrtype_list: list):
        """
        Constructor.

        :param pod: The pod to use.
        :param dao_name: The data access object library to use.
        :param corrtype_list: List of correspodence types to process for.
        """
        self._shutdown      = False
        self._pod           = pod
        self._log           = pod.log
        self._dao           = bs_loco.dao_by_name(dao_name)
        self._corrtype_list = corrtype_list
        self._prov_cache    = { '__cache__' : datetime.datetime.min }

        self._proc_interval   = 1.0
        self._prov_interval   = 60.0 * 60.0  # 1 hour


    def shutdown(self):
        """
        Instruct the server to shutdown.
        """
        self._shutdown = True


    def run(self):
        """
        Run the server.
        """
        self._shutdown  = False

        try:
            self._initialize()
            self._cache_providers(datetime.datetime.now())

            self._log.info("Loco Server - starting [procInterval:%.2f]" % (self._proc_interval))

            while not self._shutdown:
                self._process(datetime.datetime.now())

                if self._shutdown:
                    break

                pi = self._proc_interval

                while pi > 0.0:
                    pi -= self._proc_interval
                    time.sleep(self._proc_interval)

                    if self._shutdown:
                        break

            self._log.info("Loco Server - stopping")

        except Exception as x:
            self._log.error('Loco Server exception caught [error:%s, trace:%s]' % (str(x), traceback.format_exc()))
            raise
        finally:
            self._destroy()


    def run_once(self) -> int:
        """
        This is debug function that only runs the server loop once.

        :returns: The number of messages processed.
        """
        self._shutdown = False

        self._initialize()

        self._cache_providers(datetime.datetime.now())

        self._log.info("Loco Server - run_once start")

        cnt = self._process(datetime.datetime.now())

        self._shutdown = True

        self._destroy()

        self._log.info("Loco Server - run_once stop [cnt:%d]" % (cnt))

        return cnt


    def _initialize(self):
        """
        Initialize the generation server.
        """
        with AutoTransaction(self._pod):
            conf = Config(self._pod, self._dao)
            cfg  = conf.load([
                'server.proc-interval',
                'server.prov-interval',
            ])

            print(cfg)

            pi = common.read_dict(cfg, 'server.proc-interval', float)
            pv = common.read_dict(cfg, 'server.prov-interval', float)

            if pi < 0.2:
                self._log.warning('Interval value invalid [%.2f], using default of [%.2f]' % self._proc_interval)
            else:
                self._proc_interval = pi
                self._log.debug(' - server.proc-interval : %.2f' % self._proc_interval)

            if pv < 60.0:
                self._log.warning('Interval value invalid [%.2f], using default of [%.2f]' % self._prov_interval)
            else:
                self._prov_interval = pv
                self._log.debug(' - server.prov-interval : %.2f' % self._prov_interval)


    def _destroy(self):
        """
        Release any objects that are loaded.
        """
        pass


    def _process(self, dtnow: datetime.datetime) -> int:
        """
        Process any new messages.

        :param dtnow: To run the the specified time.
        :return: Number of messages processed.
        """
        msgs  = []
        idx   = 0

        with AutoTransaction(self._pod):
            self._dao.dMsgForProcessing(self._pod.dbcon).exec_deft(
                query_builder.dyn_list(self._corrtype_list, 'm', 'corrtype_id'),
                dtnow,
                self.MSG_PROC_PER_INTERVAL).fetch_all(msgs)

            if not msgs:
                return 0

            self._cache_providers(dtnow)

        self._log.info('Processing [%d] messages' % (len(msgs)))

        for msg in msgs:
            if self._shutdown:
                self._log.warning('Process shutdown detected at msg [idx:%d, id:%d], breaking loop.' % (idx, msg.id))

            if idx % 100 == 0:
                self._log.info(' ...[%d/%d]' % (idx, len(msgs)))

            if msg.corrtype_id not in self._prov_cache:
                raise Exception('Internal error, corrtype_id not found in provider cache!' % msg.corrtype_id)

            if not self._prov_cache[msg.corrtype_id].send(msg.id):
                self._log.warning("Msg failed to send, see provider log for detail. [%s]" % str(msg))

            idx += 1

        self._log.info(' ...[%d/%d]' % (idx, len(msgs)))

        return idx


    def _destroy_providers(self):
        """
        Destroys all the providers.
        """
        for pr in self._corrtype_list:
            if pr not in self._prov_cache:
                continue

            probj = self._prov_cache.pop(pr)
            probj.destroy()


    def _cache_providers(self, dtnow: datetime.datetime):
        """
        Cache the required providers.
        """
        if self._prov_cache['__cache__'] > dtnow:
            return

        self._destroy_providers()  # Note consider detecing for changes, and only reload the providers that have changed.

        with AutoTransaction(self._pod):
            for pr in self._corrtype_list:
                self._prov_cache[pr] = corrprov.get_provider(self._pod, self._dao, pr)

        self._prov_cache['__cache__'] = dtnow + datetime.timedelta(seconds = self._prov_interval)
