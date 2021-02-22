# eopayment - online payment library
# Copyright (C) 2011-2020 Entr'ouvert
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import re
import random

import pytz

from .common import (PaymentCommon, PaymentResponse, URL, PAID, DENIED,
                     CANCELLED, ERROR, ResponseError, _)
from six.moves.urllib.parse import urlencode, parse_qs

import logging
import warnings

__all__ = ['Payment']

TIPI_URL = 'https://www.tipi.budget.gouv.fr/tpa/paiement.web'
LOGGER = logging.getLogger(__name__)


class Payment(PaymentCommon):
    '''Produce requests for and verify response from the TIPI online payment
    processor from the French Finance Ministry.

    '''

    description = {
        'caption': 'TIPI, Titres Payables par Internet',
        'parameters': [
            {
                'name': 'numcli',
                'caption': _(u'Client number'),
                'help_text': _(u'6 digits number provided by DGFIP'),
                'validation': lambda s: str.isdigit(s) and (0 < int(s) < 1000000),
                'required': True,
            },
            {
                'name': 'service_url',
                'default': TIPI_URL,
                'caption': _(u'TIPI service URL'),
                'help_text': _(u'do not modify if you do not know'),
                'validation': lambda x: x.startswith('http'),
                'required': True,
            },
            {
                'name': 'normal_return_url',
                'caption': _('Normal return URL (unused by TIPI)'),
                'required': False,
            },
            {
                'name': 'automatic_return_url',
                'caption': _('Automatic return URL'),
                'required': True,
            },
            {
                'name': 'saisie',
                'caption': _('Payment type'),
                'required': True,
                'default': 'T',
                'choices': [
                    ('T', _('test')),
                    ('X', _('production')),
                    ('A', _('with user account')),
                    ('M', _('manual entry')),
                ],
            },
        ],
    }

    REFDET_RE = re.compile('^[a-zA-Z0-9]{6,30}$')

    def _generate_refdet(self):
        return '%s%010d' % (datetime.datetime.now(pytz.timezone('Europe/Paris')).strftime('%Y%m%d%H%M%S'),
                            random.randint(1, 1000000000))

    def request(self, amount, email, next_url=None, exer=None, orderid=None,
                refdet=None, objet=None, saisie=None, **kwargs):
        montant = self.clean_amount(amount, max_amount=9999.99)

        automatic_return_url = self.automatic_return_url
        if next_url and not automatic_return_url:
            warnings.warn("passing next_url to request() is deprecated, "
                          "set automatic_return_url in options", DeprecationWarning)
            automatic_return_url = next_url
        if automatic_return_url is not None:
            if (not isinstance(automatic_return_url, str)
                    or not automatic_return_url.startswith('http')):
                raise ValueError('URLCL invalid URL format')
        try:
            if exer is not None:
                exer = int(exer)
                if exer > 9999:
                    raise ValueError()
        except ValueError:
            raise ValueError('EXER format invalide')
        assert not (orderid and refdet), 'orderid and refdet cannot be used together'
        # check or generate refdet
        if refdet:
            try:
                if not self.REFDET_RE.match(refdet):
                    raise ValueError
            except (TypeError, ValueError):
                raise ValueError('refdet must be 6 to 30 alphanumeric characters string')
        if orderid:
            if self.REFDET_RE.match(orderid):
                refdet = orderid
            else:
                objet = orderid + (' ' + objet) if objet else ''
        if not refdet:
            refdet = self._generate_refdet()
        transaction_id = refdet
        # check objet or fix objet
        if objet is not None:
            try:
                objet = objet.encode('ascii')
            except Exception as e:
                raise ValueError('OBJET must be an alphanumeric string', e)
        try:
            mel = str(email)
            if '@' not in mel:
                raise ValueError('no @ in MEL')
            if not (6 <= len(mel) <= 80):
                raise ValueError('len(MEL) is invalid, must be between 6 and 80')
        except Exception as e:
            raise ValueError('MEL is not a valid email, %r' % mel, e)

        # check saisie
        saisie = saisie or self.saisie
        if saisie not in ('M', 'T', 'X', 'A'):
            raise ValueError('SAISIE invalid format, %r, must be M, T, X or A' % saisie)

        params = {
            'numcli': self.numcli,
            'refdet': refdet,
            'montant': montant,
            'mel': mel,
            'saisie': saisie,
        }
        if exer:
            params['exer'] = exer
        if objet:
            params['objet'] = objet
        if automatic_return_url:
            params['urlcl'] = automatic_return_url
        url = '%s?%s' % (self.service_url, urlencode(params))
        return transaction_id, URL, url

    def response(self, query_string, **kwargs):
        fields = parse_qs(query_string, True)
        if not set(fields) >= set(['refdet', 'resultrans']):
            raise ResponseError('missing refdet or resultrans')
        for key, value in fields.items():
            fields[key] = value[0]
        refdet = fields.get('refdet')
        if refdet is None:
            raise ResponseError('refdet is missing')

        result = fields.get('resultrans')
        if result == 'P':
            result = PAID
            bank_status = ''
        elif result == 'R':
            result = DENIED
            bank_status = 'refused'
        elif result == 'A':
            result = CANCELLED
            bank_status = 'canceled'
        else:
            bank_status = 'wrong return: %r' % result
            result = ERROR

        test = fields.get('saisie') == 'T'

        return PaymentResponse(
            result=result,
            bank_status=bank_status,
            signed=True,
            bank_data=fields,
            order_id=refdet,
            transaction_id=refdet,
            test=test)
