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
import json

from bs_lib import Pod

from bs_loco.xloco     import xLoco
from bs_loco           import constants

from .provider import Provider

# The below list is formatter as "<corrtype_id>-<provider_id>-<module_path>"

LOCO_PROVIDER_LIST = [
    'email-smtp-bs_loco.corr_prov.smtp_email.SmtpEmail',
    'email-logfile-bs_loco.corr_prov.logfile_email.LogfileEmail',
    'sms-awssns-bs_loco.corr_prov.awssns_sms.AwsSnsSms'
    'sms-bulksms-bs_loco.corr_prov.bulksms_sms.BulkSMSSms'
    'sms-logfile-bs_loco.corr_prov.logfile_sms.LogfileSms',
]


if os.environ.get('BITSMITHS_LOCO_CUST_PROVIDERS'):
    for cprov in os.environ.get('METTLE_MKFILE_CUST_GENES').split(os.path.pathsep):
        LOCO_PROVIDER_LIST.append(cprov)

_providers = {
    constants.CORRTYPE_EMAIL : {},
    constants.CORRTYPE_SMS   : {},
}

for prov in LOCO_PROVIDER_LIST:
    logging.info('Importing mettlemk makefile generator [%s]' % cgen)

    parts = prov.split('-')

    if len(parts) != 3:
        raise Exception('Provider Item expected to be in in format: <corrtype_id>-<provider_id>-<module_path>')

    if parts[0] not in _providers.keys():
        raise Exception(f'Provider Item [{parts[0]}] is not an expected correspondence type. Expected: [{_providers.keys()}]')

    _providers[parts[0]][parts[1]] = { 'path': parts[2], 'prov': None }


del LOCO_PROVIDER_LIST



def get_provider(pod: Pod, dao, corrtype_id: str) -> Provider:
    """
    Factory to load a correspondence provider by id.

    :param pod: The pod to use.
    :param dao: The dao module to use.
    :param corrtype_id: The correspondence type to load.
    """
    from bs_lib import common

    plist = []

    if not dao.dCorrProvForService(pod.dbcon).exec_deft(corrtype_id).fetch_all(plist):
        raise xLoco('No active providers configured! [%s] .' % corrtype_id)

    if len(plist) > 1:
        pod.log.warning('Multiple active providers detected. Selecting the most recently chagned.')

        pod.log.warning('  - selected: %s' % str(plist[0]))

        for x in plist[1:]:
            pod.log.warning('  - ignored : %s' % str(x))

    rec    = plist[0]
    res    = None
    ct_obj = _providers.get(rec.corrtype_id)

    if ct_obj:
        prov_obj = ct_obj.get(rec.corrprov_id)

        if prov_obj:
            if not prov_obj['prov']:
                prov, exc    = common.import_dyn_pluggin(prov_obj['path'], False, True)
                prov['prov'] = prov

            res = prov['prov']()

    if not res:
        raise xLoco('Provider not found. [%s].' % (str(rec)))

    if res.id() != rec.corrprov_id:
        raise Exception('Factory error, database corrprov_id does not match object corrprov_id [%s]' % (
            str(rec)))

    if res.corrtype_id() != rec.corrtype_id:
        raise Exception('Factory error, database corrtype_id does not match object corrtype_id [%s]' % (
            str(rec)))

    res.initialize(pod, dao, json.loads(rec.cfg))

    return res


__all__ = [ 'get_provider' ]
