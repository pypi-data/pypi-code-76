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

import logging
import uuid
import warnings

from six.moves.urllib.parse import parse_qs, urlencode

from .common import (
    PaymentCommon,
    PaymentResponse,
    ResponseError,
    URL,
    PAID, ERROR, WAITING,
    force_text,
    _
)

__all__ = ['Payment']


SERVICE_URL = 'http://dummy-payment.demo.entrouvert.com/'
LOGGER = logging.getLogger(__name__)


class Payment(PaymentCommon):
    '''
       Dummy implementation of the payment interface.

       It is used with a dummy implementation of a bank payment service that
       you can find on:

           http://dummy-payment.demo.entrouvert.com/

       You must pass the following keys inside the options dictionnary:
        - dummy_service_url, the URL of the dummy payment service, it defaults
          to the one operated by Entr'ouvert.
        - automatic_return_url: where to POST to notify the service of a
          payment
        - origin: a human string to display to the user about the origin of
          the request.
        - siret: an identifier for the eCommerce site, fake.
        - normal_return_url: the return URL for the user (can be overriden on a
          per request basis).
    '''
    description = {
        'caption': 'Dummy payment backend',
        'parameters': [
            {
                'name': 'normal_return_url',
                'caption': _('Normal return URL'),
                'default': '',
                'required': True,
            },
            {
                'name': 'automatic_return_url',
                'caption': _('Automatic return URL'),
                'required': False,
            },
            {
                'name': 'dummy_service_url',
                'caption': _('URL of the dummy payment service'),
                'default': SERVICE_URL,
                'type': str,
            },
            {
                'name': 'origin',
                'caption': _('name of the requesting service, '
                           'to present in the user interface'),
                'type': str,
                'default': 'origin',
            },
            {
                'name': 'consider_all_response_signed',
                'caption': _(
                    'All response will be considered as signed '
                    '(to test payment locally for example, as you '
                    'cannot received the signed callback)'
                ),
                'type': bool,
                'default': False,
            },
            {
                'name': 'number',
                'caption': 'dummy integer input test',
                'type': int,
            },
            {
                'name': 'choice',
                'caption': 'dummy choice input test',
                'choices': ['a', 'b'],
            },
            {
                'name': 'choices',
                'caption': 'dummy choices input test',
                'choices': ['a', 'b'],
                'type': list,
            },
            {
                'name': 'direct_notification_url',
                'caption': _('direct notification url (replaced by automatic_return_url)'),
                'type': str,
                'deprecated': True,
            },
            {
                'name': 'next_url (replaced by normal_return_url)',
                'caption': _('Return URL for the user'),
                'type': str,
                'deprecated': True,
            },
            {
                'name': 'capture_day',
                'type': str,
            },
        ],
    }

    def request(self, amount, name=None, address=None, email=None, phone=None,
                orderid=None, info1=None, info2=None, info3=None,
                next_url=None, capture_day=None, subject=None, **kwargs):
        self.logger.debug(
            '%s amount %s name %s address %s email %s phone %s'
            ' next_url %s info1 %s info2 %s info3 %s kwargs: %s',
            __name__, amount, name, address, email, phone, info1, info2, info3, next_url, kwargs)
        transaction_id = str(uuid.uuid4().hex)
        normal_return_url = self.normal_return_url
        if next_url and not normal_return_url:
            warnings.warn("passing next_url to request() is deprecated, "
                          "set normal_return_url in options", DeprecationWarning)
            normal_return_url = next_url
        automatic_return_url = self.automatic_return_url
        if self.direct_notification_url and not automatic_return_url:
            warnings.warn("direct_notification_url option is deprecated, "
                          "use automatic_return_url", DeprecationWarning)
            automatic_return_url = self.direct_notification_url
        query = {
            'transaction_id': transaction_id,
            'amount': amount,
            'email': email,
            'return_url': normal_return_url or '',
            'direct_notification_url': automatic_return_url or '',
            'origin': self.origin
        }
        query.update(
            dict(name=name, address=address, email=email, phone=phone,
                 orderid=orderid, info1=info1, info2=info2, info3=info3))
        if capture_day is not None:
            query['capture_day'] = str(capture_day)
        if subject is not None:
            query['subject'] = subject
        for key in list(query.keys()):
            if query[key] is None:
                del query[key]
        url = '%s?%s' % (SERVICE_URL, urlencode(query))
        return transaction_id, URL, url

    def response(self, query_string, logger=LOGGER, **kwargs):
        form = parse_qs(force_text(query_string))
        if 'transaction_id' not in form:
            raise ResponseError('missing transaction_id')
        transaction_id = form.get('transaction_id', [''])[0]
        form[self.BANK_ID] = transaction_id

        signed = 'signed' in form
        if signed:
            content = 'signature ok'
        else:
            content = None
        signed = signed or self.consider_all_response_signed
        result = PAID if 'ok' in form else ERROR
        if 'waiting' in form:
            result = WAITING

        response = PaymentResponse(
            result=result,
            signed=signed,
            bank_data=form,
            return_content=content,
            order_id=transaction_id,
            transaction_id=transaction_id,
            bank_status=form.get('reason'),
            test=True)
        return response

    def validate(self, amount, bank_data, **kwargs):
        return {}

    def cancel(self, amount, bank_data, **kwargs):
        return {}
