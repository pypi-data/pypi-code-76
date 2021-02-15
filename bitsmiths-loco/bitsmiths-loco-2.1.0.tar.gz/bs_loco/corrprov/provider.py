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
import re
import traceback

from bs_lib.AutoTransaction import AutoTransaction
from bs_lib.Pod             import Pod
from bs_lib                 import QueryBuilder

from bs_loco.loco_template  import LocoTemplate
from bs_loco.xloco          import xLoco

from bs_loco.db.tables   import tMsg
from bs_loco.db.tables   import tMsgReq
from bs_loco.db.tables   import tNoType


class Provider:
    """
    This is the base class for all correspondence types.
    """
    MAX_MSG_ERROR_LOGS = 5

    def __init__(self):
        """
        Constructor.
        """
        self._pod   = None
        self._dao   = None
        self._cfg   = None
        self._cache = {}


    def __del__(self):
        """
        Destructor.
        """
        self.destroy()


    def initialize(self, pod: Pod, dao: object, cfg: dict):
        """
        Virtual method to initialize the loco trigger interface.

        :param pod: The pod to use.
        :param dao: The dao to use.
        :param cfg: Any configs needed for the trigger, can be None.
        """
        self.destroy()
        self._pod = pod
        self._dao = dao
        self._cfg = cfg
        self._log = pod.log

        self._cache = {
            'notype'  : {},
            'templ'   : {},
            'res'     : {},
            'keypair' : None,
            'allow'   : None,
        }

        dcp = dao.dCorrProv(pod.dbcon)

        dcp.select_one_deft(self.id(), self.corrtype_id())


    def destroy(self):
        """
        Virtual method to destroy the content management object.
        """
        self._pod = None
        self._dao = None
        self._cfg = None
        self._log = None
        self._cache.clear()


    def id(self) -> str:
        """
        Pure virtual method, the identifier of the content management overload.

        :return: The overload name.
        """
        raise Exception('id() not implemented.')


    def corrtype_id(self) -> str:
        """
        Pure virtual method, the identifier of the content management overload.

        :return: The overload name.
        """
        raise Exception('corrtype_id() not implemented.')


    def name(self) -> str:
        """
        Pure virtual method, the name of the content management overload.

        :return: The overload name.
        """
        return '%s.%s' % (self.corrtype_id(), self.id())


    def is_deadbeef(self) -> bool:
        """
        Virtual method to check if the interface is active but not configured.

        :return: True if this interface is active but not configure.
        """
        return False


    def send(self, msg_id) -> bool:
        """
        Send a message to a provider.

        :param msg_id: The message to send.
        :return: True of success or false if something went wrong.
        """
        self._log.debug('send - start [msgId:%d]' % (msg_id))

        dmsg = self._dao.dMsg(self._pod.dbcon)
        dreq = self._dao.dMsgReq(self._pod.dbcon)

        with AutoTransaction(self._pod) as at:
            try:
                dmsg.lock_one_deft(msg_id, self._pod.stdDBLock())

                if self.corrtype_id() != dmsg.rec.corrtype_id:
                    raise Exception('Internal error, provider received wrong message type. [corrtype_id:%s, msg:%s]' % (
                        self.corrtype_id(), str(dmsg.rec)))


                if dmsg.rec.status != tMsg.Status_Couplet.key_pending and\
                   dmsg.rec.status != tMsg.Status_Couplet.key_retry:
                    self._log.warning('  - skipping msg in unexepcted status [status:%s]' % (dmsg.rec.status))
                    return True

                if dmsg.rec.status == tMsg.Status_Couplet.key_retry:
                    dmsg.rec.retry_cnt += 1

                ok, err_msg = self._init_cache(dmsg.rec)

                if not ok:
                    dmsg.rec.status    = tMsg.Status_Couplet.key_template_error
                    dmsg.rec.msglog    = self._push_msg_log(dmsg.rec.msglog, err_msg)
                    dmsg.rec.fail_cnt += 1
                    dmsg.update()
                    at.commit()
                    return True

                ntrec = self._cache['notype'][dmsg.rec.notype_id]

                if ntrec.status != tNoType.Status_Couplet.key_active:
                    self._log.warning('  - skipping message, because the notification type is not active: [msg:%s]' % (
                        str(dmsg.rec)))
                    dmsg.rec.status = tMsg.Status_Couplet.key_cancelled
                    dmsg.rec.msglog = self._push_msg_log(dmsg.rec.msglog, 'Notification type is disabled')
                    dmsg.update()
                    at.commit()
                    return True

                dreq.select_one_deft(dmsg.rec.msgreq_id)

                if ntrec.max_life > 0:
                    dtnow = datetime.datetime.now()

                    if dreq.rec.time_to_send + datetime.timedelta(minutes=ntrec.max_life) < dtnow:
                        self._log.warning('  - skipping message, max life reached: [max_life:%d, now:%s, req_time:%s, msg:%s]' % (  # noqa
                            ntrec.max_life, str(dtnow), str(dreq.rec.time_to_send), str(dmsg.rec)))
                        dmsg.rec.status = tMsg.Status_Couplet.key_cancelled
                        dmsg.rec.msglog = self._push_msg_log(dmsg.rec.msglog, 'Max life reached [%d min]' % (ntrec.max_life))
                        dmsg.update()
                        at.commit()
                        return False

                try:
                    if dmsg.rec.corrprov_id == self.id() and dmsg.rec.payload:
                        payload = json.loads(dmsg.rec.payload)
                    else:
                        payload          = self._build_payload(dreq.rec)
                        dmsg.rec.payload = json.dumps(payload)

                    resource_list = self._load_msgreq_resources(dreq.rec)
                except Exception:

                    tb = traceback.format_exc()

                    self._log.error('Exception building payload or loading resources [msg_id:%d, provider:%s]' % (
                        msg_id, self.id()))

                    self._log.error(tb)

                    dmsg.rec.status    = tMsg.Status_Couplet.key_template_error
                    dmsg.rec.msglog    = self._push_msg_log(dmsg.rec.msglog, tb)
                    dmsg.rec.fail_cnt += 1
                    dmsg.update()
                    at.commit()
                    return False

                msg_addr = json.loads(dreq.rec.msg_addr)
                addr_list = self._addresses_allowed(msg_addr.get(self.corrtype_id()))

                if not addr_list:
                    self._log.warning('  - skipping message, because none of the addresses match\
 the allowed [msg:%s, addresses:%s]' % (str(dmsg.rec), str(msg_addr.get(self.corrtype_id()))))
                    dmsg.rec.status = tMsg.Status_Couplet.key_cancelled
                    dmsg.rec.msglog = self._push_msg_log(dmsg.rec.msglog, 'No addresses are allowed.')
                    dmsg.update()
                    at.commit()
                    return True

                ok, time_taken, errMsg = self._provider_send(payload,
                                                             resource_list,
                                                             dmsg.rec,
                                                             addr_list)

                dmsg.rec.corrprov_id = self.id()
                dmsg.rec.usrId       = self._pod.usr_id

                if ok:
                    dmsg.rec.time_sent  = datetime.datetime.now()
                    dmsg.rec.time_taken = time_taken.total_seconds()
                    dmsg.rec.status     = tMsg.Status_Couplet.key_sent
                else:
                    dmsg.rec.msglog    = self._push_msg_log(dmsg.rec.msglog, err_msg)
                    dmsg.rec.fail_cnt += 1
                    dmsg.rec.status    = tMsg.Status_Couplet.key_failed

                dmsg.update()

                self._upd_parent_status(dreq, dreq.rec)

                at.commit()

            except Exception as x:
                self._log.error('Exception caught sending [msg_id:%d, provider:%s]' % (msg_id, self.id()))
                self._log.exception(x)
                raise

        self._log.debug('send - done [msgId:%d, status:%s]' % (dmsg.rec.id, tMsg.Status_Couplet.get_value(dmsg.rec.status)))

        return dmsg.rec.status == tMsg.Status_Couplet.key_sent


    def _upd_parent_status(self, msg: tMsg, req: tMsgReq):
        """
        Updates the parent (MsgReq) table status.

        :param msg: The message record.
        :param msgreq: The message request parent.
        """
        if req.Status_Couplet == tMsgReq.Status_Couplet.key_processed:
            return

        lst        = []
        new_status = tMsgReq.Status_Couplet.key_busy

        self._dao.dMsgStatusCntByReq(self._pod.dbcon).exec_deft(req.id).fetch_all(lst)

        if len(lst) == 1:
            if lst[0].status == tMsg.Status_Couplet.key_cancelled:
                new_status = tMsgReq.Status_Couplet.key_cancelled
            elif lst[0].status == tMsg.Status_Couplet.key_sent:
                new_status = tMsgReq.Status_Couplet.key_processed
        else:
            all_done = True

            for item in lst:
                if item.status == tMsg.Status_Couplet.key_sent or item.status == tMsg.Status_Couplet.key_cancelled:
                    continue

                all_done = False
                break

            if all_done:
                new_status = tMsgReq.Status_Couplet.key_processed

        self._dao.dMsgReqUpdateStatus(self._pod.dbcon).exec_deft(req.id,
                                                                 new_status,
                                                                 datetime.datetime.now(),
                                                                 self._pod.usr_id)


    def _init_cache(self, msg: tMsg) -> tuple:
        """
        Loads all the objects needed for the message cache.

        :param msg: The message record.
        :returns: (bool succes_or_failure, str error_msg)
        """
        try:
            if msg.notype_id not in self._cache['notype']:
                ntd = self._dao.dNoType(self._pod.dbcon)
                ntd.select_one_deft(msg.notype_id)
                self._cache['notype'][ntd.rec.id] = ntd.rec

                ntempld = self._dao.dNoTempl(self._pod.dbcon)
                ntempld.select_one_deft(msg.notype_id, msg.corrtype_id)

                self._cache['templ'][ntd.rec.id] = self._validate_template(json.loads(ntempld.rec.templ))
                self._cache['res'][ntd.rec.id]   = self._load_template_resources(ntempld.rec.res_list)

            if self._cache['keypair'] is None:
                kpqry = self._dao.dNoDictSearch(self._pod.dbcon)
                kp    = {}
                kpqry.exec()

                while kpqry.fetch():
                    kp[kpqry.orec.id] = kpqry.orec.value or ''

                self._cache['keypair'] = kp

            if self._cache['allow'] is None:
                aqry  = self._dao.dCorrTypeAllowRegexForType(self._pod.dbcon)
                allow = []

                aqry.exec_deft(msg.corrtype_id, '', 'A')

                while aqry.fetch():
                    try:
                        allow.append(re.compile(aqry.orec.regex))
                    except Exception as x:
                        self._log.exception(x)
                        self._log.error('Failed to compile the allow regex: [%s]' % (str(aqry.orec)))
                        raise

                self._cache['allow'] = allow

        except Exception as x:
            self._log.error('Exception caught initializing cache for message: [%s]' % (str(msg)))
            self._log.exception(x)
            return False, str(x)

        return True, None


    def _push_msg_log(self, msglog: str, err_msg: str) -> str:
        """
        Pushes a message onto the message log.
        """
        if not msglog:
            return json.dumps([err_msg])

        try:
            logs = json.loads(msglog)

            logs.insert(0, err_msg)

            if len(logs) > 10:
                logs.pop()

            return json.dumps(logs)

        except Exception as x:
            return json.dumps([str(x)])


    def _load_msgreq_resources(self, req: tMsgReq) -> list:
        """
        Loads all the resources associated with the message.

        :param req: The message req.
        :return: The list of resources loaded or none.
        """
        if not req.cust_res:
            return None

        res = []
        crit = " and mr.corr_id_list ? '%s'" % self.corrtype_id()

        self._dao.dMsgReqResByMsgReq(self._pod.dbcon).exec_deft(req.id, crit).fetch_all(res)

        return res


    def _validate_template(self, templ: dict) -> dict:
        """
        Virtual methed that validates a template for this provider and make any changes as required.

        :param templ: The template configuration.
        :return: The validated template.
        """
        return templ


    def _load_template_resources(self, res_list: str):
        """
        Loads the template resources for by name.

        :param res_list: A json string of resource items.
        :return: The resource objects.
        """
        if not res_list:
            return None

        rlist = json.loads(res_list)

        if not rlist:
            return None

        res = []

        self._dao.dNoResSearch(self._pod.dbcon).exec_deft(QueryBuilder.dynList(rlist, 'nr', 'id')).fetch_all(res)

        return res


    def _build_payload(self, req: tMsgReq) -> dict:
        """
        Pure virtual method creates the message payload for sending.

        :param req: The message request record.
        :return: The payload object.
        """
        raise Exception('_provider_send() not implemented.')


    def _provider_send(self, payload: dict, res_list: list, msg: tMsg, addr_list: list) -> tuple:
        """
        Pure virtual method that sends the pay loda via the correspondence.

        :param payload: The generated payload.
        :param res_list: The list of additional resources to attatch to the message.
        :param msg: The message record.
        :param addr_list: The list of addresses to send to.
        :return: (bool successfailure, float time_taken, str err_msg)
        """
        raise Exception('_provider_send() not implemented.')


    def _template_subst(self, text: str, keypair: dict) -> str:
        """
        Performs standard string subsitution on the payload.

        :param text: The template text to substitute.
        :param keypair: The keypair values to substitute with.
        :return: The substituted string.
        """
        return LocoTemplate(text).substitute(keypair)


    def _build_msg_keypairs(self, req: tMsgReq) -> dict:
        """
        Builds the messasge specific keypairs with the template key pairs combined.

        :param req: The message req object.
        :return: The the msg key pairs.
        """
        res = {}

        templ_kpair = self._cache.get('keypair')

        if templ_kpair:
            res.update(templ_kpair)

        if req.msg_dict:
            kpair = json.loads(req.msg_dict)
            if not isinstance(kpair, dict):
                raise xLoco('Invalid keypair object [msgreq: %s]' % (str(req)))

            res.update(kpair)

        return res


    def _addresses_allowed(self, addr_list: list) -> list:
        """
        Ensure all addresses that are pass the allow list are only returned.

        :param addr_list: The list of addresses we need to check.
        :return: All the addresses that match the regex white list.
        """
        if not self._cache['allow']:
            return addr_list

        res = []

        for chk in addr_list:
            for regexp in self._cache['allow']:
                if regexp.match(chk):
                    res.append(chk)
                    break

        return res
