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

import requests
from six.moves.urllib.parse import parse_qs, urljoin

from .common import (CANCELLED, ERROR, PAID, URL, WAITING, PaymentCommon,
                     PaymentException, PaymentResponse, ResponseError, _)

__all__ = ['Payment']


class Payment(PaymentCommon):
    '''Implements EMS API, see https://dev.online.emspay.eu/.'''
    service_url = 'https://api.online.emspay.eu/v1/'

    description = {
        'caption': _('Keyware payment backend'),
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
            },
        ],
    }

    def request(self, amount, email=None, first_name=None, last_name=None, **kwargs):
        amount = int(self.clean_amount(amount, min_amount=0.01))

        body = {
            'currency': 'EUR',
            'amount': amount,
            'return_url': self.normal_return_url,
            'webhook_url': self.automatic_return_url,
            'customer': {
                'email_address': email,
                'first_name': first_name,
                'last_name': last_name,
            }
        }

        resp = self.call_endpoint('POST', 'orders', data=body)
        return resp['id'], URL, resp['order_url']

    def response(self, query_string, **kwargs):
        fields = parse_qs(query_string, keep_blank_values=True)
        order_id = fields['order_id'][0]
        resp = self.call_endpoint('GET', 'orders/' + order_id)

        # XXX: to add accepted we need to handle the capture mode (manual or
        # delayed), see
        # https://dev.online.emspay.eu/rest-api/features/authorizations-captures-and-voiding
        status = resp['status']
        if status == 'completed':
            result = PAID
        elif status in ('new', 'processing'):
            result = WAITING
        elif status in ('cancelled', 'expired'):
            result = CANCELLED
        else:
            result = ERROR

        response = PaymentResponse(
            result=result,
            signed=True,
            bank_data=resp,
            order_id=order_id,
            transaction_id=order_id,
            bank_status=status,
            test=bool('is-test' in resp.get('flags', []))
        )
        return response

    def cancel(self, amount, bank_data, **kwargs):
        order_id = bank_data['id']
        resp = self.call_endpoint('DELETE', 'orders/' + order_id)
        status = resp['status']
        if not status == 'cancelled':
            raise ResponseError('expected "cancelled" status, got "%s" instead' % status)
        return resp

    def call_endpoint(self, method, endpoint, data=None):
        url = urljoin(self.service_url, endpoint)
        try:
            response = requests.request(method, url, auth=(self.api_key, ''), json=data)
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
                '%s error on endpoint "%s": %s "%s"' % (method, endpoint, e, result))
        return result
