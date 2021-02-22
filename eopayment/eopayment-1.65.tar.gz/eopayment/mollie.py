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

from .common import _

import requests
from six.moves.urllib.parse import parse_qs, urljoin

from .common import (CANCELLED, ERROR, PAID, URL, PaymentCommon,
                     PaymentException, PaymentResponse, ResponseError, WAITING,
                     ACCEPTED)

__all__ = ['Payment']


class Payment(PaymentCommon):
    '''Implements Mollie API, see https://docs.mollie.com/reference/v2/.'''
    service_url = 'https://api.mollie.com/v2/'

    description = {
        'caption': 'Mollie payment backend',
        'parameters': [
            {
                'name': 'normal_return_url',
                'caption': _('Normal return URL'),
                'required': True,
            },
            {
                'name': 'automatic_return_url',
                'caption': _('Asychronous return URL'),
                'required': True,
            },
            {
                'name': 'service_url',
                'caption': _('URL of the payment service'),
                'default': service_url,
                'type': str,
                'validation': lambda x: x.startswith('https'),
            },
            {
                'name': 'api_key',
                'caption': _('API key'),
                'required': True,
                'validation': lambda x: x.startswith('test_') or x.startswith('live_'),
            },
            {
                'name': 'description_text',
                'caption': _('General description that will be displayed for all payments'),
                'required': True,
            },
        ],
    }

    def request(self, amount, **kwargs):
        amount = self.clean_amount(amount, cents=False)

        metadata = {k: v for k, v in kwargs.items()
                    if k in ('email', 'first_name', 'last_name') and v is not None}
        body = {
            'amount': {
                'value': amount,
                'currency': 'EUR',
            },
            'redirectUrl': self.normal_return_url,
            'webhookUrl': self.automatic_return_url,
            'metadata': metadata,
            'description': self.description_text,
        }

        resp = self.call_endpoint('POST', 'payments', data=body)

        return resp['id'], URL, resp['_links']['checkout']['href']

    def response(self, query_string, redirect=False, order_id_hint=None,
                 order_status_hint=None, **kwargs):
        if redirect:
            if order_status_hint in (PAID, CANCELLED, ERROR):
                return PaymentResponse(order_id=order_id_hint, result=order_status_hint)
            else:
                payment_id = order_id_hint
        elif query_string:
            fields = parse_qs(query_string)
            payment_id = fields['id'][0]
        else:
            raise ResponseError('cannot infer payment id')

        resp = self.call_endpoint('GET', 'payments/' + payment_id)

        status = resp['status']
        if status == 'paid':
            result = PAID
        elif status in ('canceled', 'expired'):
            result = CANCELLED
        elif status in ('open', 'pending'):
            result = WAITING
        elif status == 'authorized':
            result = ACCEPTED
        else:
            result = ERROR

        response = PaymentResponse(
            result=result,
            signed=True,
            bank_data=resp,
            order_id=payment_id,
            transaction_id=payment_id,
            bank_status=status,
            test=resp['mode'] == 'test'
        )
        return response

    def call_endpoint(self, method, endpoint, data=None):
        url = urljoin(self.service_url, endpoint)
        headers = {'Authorization': 'Bearer %s' % self.api_key}
        try:
            response = requests.request(method, url, headers=headers, json=data)
        except requests.exceptions.RequestException as e:
            raise PaymentException('%s error on endpoint "%s": %s' % (method, endpoint, e))
        try:
            result = response.json()
        except ValueError:
            self.logger.debug('received invalid json %r', response.text)
            raise PaymentException('%s on endpoint "%s" returned invalid JSON: %s' %
                                   (method, endpoint, response.text))
        self.logger.debug('received "%s" with status %s', result, response.status_code)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise PaymentException(
                '%s error on endpoint "%s": %s "%s"' % (method, endpoint, e,
                                                        result.get('detail', result)))
        return result
