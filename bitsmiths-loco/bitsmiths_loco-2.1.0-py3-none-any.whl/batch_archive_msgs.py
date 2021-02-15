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

import mettle.io

from bs_lib import Pod

import bs_loco

from bs_loco.db.tables   import tMsg
from bs_loco.db.tables   import tMsgReq
from bs_loco.db.tables   import tMsgReqRes


class BatchArchiveMsgs:
    """
    Batch object to archive messages.
    """

    def __init__(self, pod: Pod, dao_name: str):
        """
        Constructor

        :param pod: The pod to use.
        :param dao_name: The dao objects to use.
        """
        self._pod = pod
        self._log = pod.log
        self._dao = bs_loco.dao_by_name(dao_name)


    def run(self, dtnow: datetime.datetime) -> None:
        """
        Main run method.

        :param dtnow: The time of this archive run
        """
        arch_date   = datetime.datetime(dtnow.year, dtnow.month, dtnow.day, 0, 0, 0) - datetime.timedelta(days=1)
        arch_qry    = self._dao.dMsgReqForArchive(self._pod.dbcon)
        msg_qry     = self._dao.dMsgByMsgReq(self._pod.dbcon)
        msgattr_qry = self._dao.dMsgReqResByMsgReq(self._pod.dbcon)
        cnt         = 0

        msg_hist  = self._dao.dMsgHist(self._pod.dbcon)
        msg       = self._dao.dMsg(self._pod.dbcon)
        msg_req   = self._dao.dMsgReq(self._pod.dbcon)
        msg_res   = self._dao.dMsgReqRes(self._pod.dbcon)

        list_msgs = tMsg.List()
        list_res  = tMsgReqRes.List()
        snap_req  = {}
        snap_prov = {}
        json_obj  = {}

        self._log.info('Archiving messages from: %s' % str(arch_date))

        arch_qry.exec_deft(arch_date)

        while arch_qry.fetch():
            cnt += 1
            self._log.debug(' - archiving [cnt:%d, msg_req:%s]' % (cnt, str(arch_qry.orec)))

            list_msgs.clear()
            list_res.clear()
            json_obj.clear()

            msg_qry.exec_deft(arch_qry.orec.id).fetch_all(list_msgs)
            msgattr_qry.exec_deft(arch_qry.orec.id, '').fetch_all(list_res)

            writer = mettle.io.PyJsonDictWriter(json_obj)

            arch_qry.orec._serialize(writer)
            list_msgs._serialize(writer)
            list_res._serialize(writer)

            self._update_snaps(arch_qry.orec, list_msgs, snap_req, snap_prov)

            msg_hist.insert_deft(arch_qry.orec.id,
                                 arch_qry.orec.status,
                                 arch_qry.orec.time_to_send,
                                 json.dumps(json_obj))

            for a in list_res:
                msg_res.delete_one_deft(a.id)

            for m in list_msgs:
                msg.delete_one_deft(m.id)

            msg_req.delete_one_deft(arch_qry.orec.id)

            if cnt % 10000 == 0:
                self._log.info(' - archived [%d] messages.' % cnt)
                self._commit_changes(snap_req, snap_prov)

        if cnt > 0 and not cnt % 10000 == 0:
            self._commit_changes(snap_req, snap_prov)

        self._log.info('Total messages archived [%d]' % cnt)


    def _commit_changes(self, snap_req: dict, snap_prov: dict):
        """
        Commits the current changes and continues

        :param snap_req: snapshots on msg requests
        :param snap_prov: snapshots on providers
        """
        smr = self._dao.dSnapMsgReq(self._pod.dbcon)
        sp  = self._dao.dSnapProv(self._pod.dbcon)

        for key, item in snap_req.items():
            smr.update(item)

        for key, item in snap_prov.items():
            item.avg_msg_time = item.tot_msg_time / item.msg_sent
            sp.update(item)

        self._pod.dbcon.commit()


    def _update_snaps(self, req_rec: tMsgReq, list_msgs: list, snap_req: dict, snap_prov: dict):
        """
        Update the statistic tables

        :param req_rec: message request rec
        :param list_msgs: messages list
        :param snap_req: snapshots on msg requests
        :param snap_prov: snapshots on providers
        """
        key = '%s.%s' % (req_rec.time_to_send.strftime('%Y%m%d'), req_rec.notype_id)

        if key not in snap_req.keys():
            smr = self._dao.dSnapMsgReq(self._pod.dbcon)

            if smr.try_select_one_deft(req_rec.time_to_send.date(), req_rec.notype_id):
                snap_req[key] = smr.rec
            else:
                smr.rec.valuedate = req_rec.time_to_send.date()
                smr.rec.notype_id = req_rec.notype_id

                smr.insert()

                snap_req[key] = smr.rec

        rec          = snap_req[key]
        rec.tot_req += 1

        if req_rec.status == tMsgReq.Status_Couplet.key_processed:
            rec.tot_proc += 1
        elif req_rec.status == tMsgReq.Status_Couplet.key_cancelled:
            rec.tot_cancelled += 1
        elif req_rec.status == tMsgReq.Status_Couplet.key_partially_cancelled:
            rec.tot_part_canc  += 1

        rec.tot_msgs += len(list_msgs)

        for msgitem in list_msgs:
            if msgitem.status == tMsg.Status_Couplet.key_sent:
                rec.tot_msgs_sent += 1
            else:
                rec.tot_msgs_failed += 1

            rec.tot_msgs_retrys += msgitem.retry_cnt

        # do provider snapshots
        for msgitem in list_msgs:
            if msgitem.corrprov_id == '':
                continue

            key = '%s.%s.%s' % (req_rec.time_to_send.strftime('%Y%m%d'), msgitem.corrtype_id, msgitem.corrprov_id)

            if key not in snap_prov.keys():
                sp = self._dao.dSnapProv(self._pod.dbcon)

                if sp.try_select_one_deft(req_rec.time_to_send.date(), msgitem.corrtype_id, msgitem.corrprov_id):
                    snap_prov[key] = sp.rec
                else:
                    sp.rec.valuedate    = req_rec.time_to_send.date()
                    sp.rec.corrprov_id  = msgitem.corrprov_id
                    sp.rec.corrtype_id  = msgitem.corrtype_id

                    sp.insert()

                    snap_prov[key] = sp.rec

            rec = snap_prov[key]

            if msgitem.status == tMsg.Status_Couplet.key_sent:
                rec.msg_sent     += 1
                rec.tot_msg_time += msgitem.time_taken
            else:
                rec.msg_failed += 1

            rec.msg_retry += msgitem.retry_cnt
