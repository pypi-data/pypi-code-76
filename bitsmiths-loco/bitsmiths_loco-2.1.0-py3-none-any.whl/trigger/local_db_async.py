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
import json

from bs_lib import PodAsync

import bs_loco

from bs_loco       import util
from bs_loco.xloco import xLoco

from bs_loco.db.tables  import tMsg
from bs_loco.db.tables  import tMsgReq

from .loco_trig_async import LocoTrigAsync


class LocalDBAsync(LocoTrigAsync):
    """
    The local database trigger implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        LocoTrigAsync.__init__(self)
        self._dao = None


    def id(self) -> str:
        """
        Overload.
        """
        raise 'local_db'


    def name(self) -> str:
        """
        Overload.
        """
        'Local DB'


    async def initialize(self, pod: PodAsync, cfg: dict):
        """
        Overload.
        """
        await LocoTrigAsync.initialize(self, pod, cfg)

        if not cfg or not cfg.get('dao'):
            raise xLoco('Local DB requires a dao config value.')

        self._dao = bs_loco.dao_by_name(cfg.get('dao'), 'dao_async')


    def destroy(self):
        """
        Overload.
        """
        LocoTrigAsync.destroy(self)
        self._dao = None


    async def _trigger(self,
                       notype    : str,
                       corr_addr : dict,
                       key_pair  : dict = None,
                       res       : dict = None,
                       meta_data : dict = None) -> int:
        """
        Overload.
        """
        mreq     = self._dao.dMsgReq(self._pod.dbcon)
        mres     = None
        nt       = self._dao.dNoType(self._pod.dbcon)
        dtnow    = datetime.datetime.now()
        corrlist = []
        cnt      = 0

        await nt.select_one_deft(notype)

        if nt.rec.pref_corr:
            corrlist = json.loads(nt.rec.pref_corr)

            for corr in corr_addr:
                if corr not in corrlist:
                    corrlist.append(corr)

        else:
            corrlist = list(corr_addr.keys())

        for corr in corrlist:
            if nt.rec.corr_cnt and cnt >= nt.rec.corr_cnt:
                self._pod.log.info('Max correspondece count reached [%d], skipped: %s' % (
                    nt.rec.corr_cnt, str(corrlist[cnt:])))
                break

            cnt += 1

        mreq.rec.clear()

        await mreq.insert_deft(
            notype,
            nt.rec.priority,
            tMsgReq.Status_Couplet.key_pending,
            dtnow,
            dtnow,
            datetime.datetime.min,
            json.dumps(corr_addr),
            '' if not key_pair else json.dumps(key_pair),
            True if res and res.get('resources') else False,
            '' if not meta_data else json.dumps(meta_data),
            self._pod.usr_id or '[Anonymous]')

        if res and res.get('resources'):
            for ritem in res['resources']:

                fnd = False

                for fc in ritem['for']:
                    if fc in corr:
                        fnd = True
                        break

                if not fnd:
                    continue

                if not mres:
                    mres = self._dao.dMsgReqRes(self._pod.dbcon)

                mres.rec.clear()

                if isinstance(ritem['content'], str):
                    content = bytes(ritem['content'], 'utf8')
                else:
                    content = ritem['content']

                await mres.insert_deft(
                    mreq.rec.id,
                    json.dumps(ritem['for']),
                    ritem['filename'],
                    ritem.get('mime') or util.mimetype_from_content(content),
                    content,
                    self._pod.usr_id)


        msg = self._dao.dMsg(self._pod.dbcon)

        for corr in corrlist:
            await msg.insert_deft(
                mreq.rec.id,
                corr,
                notype,
                mreq.rec.priority,
                tMsg.Status_Couplet.key_pending,
                0,
                0,
                datetime.datetime.min,
                0.0,
                '',
                '',
                '',
                self._pod.usr_id)

        return len(corrlist)
