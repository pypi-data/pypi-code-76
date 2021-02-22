# -*- coding: utf-8 -*-
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
import importlib
import logging
import pytz

import six

from .common import (  # noqa: F401
    URL, HTML, FORM, RECEIVED, ACCEPTED, PAID, DENIED,
    CANCELED, CANCELLED, ERROR, WAITING, EXPIRED, force_text,
    ResponseError, PaymentException,
)

__all__ = ['Payment', 'URL', 'HTML', 'FORM', 'SIPS', 'SYSTEMPAY',
           'TIPI', 'DUMMY', 'get_backend', 'RECEIVED', 'ACCEPTED', 'PAID',
           'DENIED', 'CANCELED', 'CANCELLED', 'ERROR', 'WAITING',
           'EXPIRED', 'get_backends', 'PAYFIP_WS', 'SAGA']

if six.PY3:
    __all__.extend(['KEYWARE', 'MOLLIE'])

SIPS = 'sips'
SIPS2 = 'sips2'
SYSTEMPAY = 'systempayv2'
TIPI = 'tipi'
DUMMY = 'dummy'
OGONE = 'ogone'
PAYBOX = 'paybox'
PAYZEN = 'payzen'
PAYFIP_WS = 'payfip_ws'
KEYWARE = 'keyware'
MOLLIE = 'mollie'
SAGA = 'saga'

logger = logging.getLogger(__name__)


def get_backend(kind):
    '''Resolve a backend name into a module object'''
    module = importlib.import_module('.' + kind, package='eopayment')
    return module.Payment

__BACKENDS = [DUMMY, SIPS, SIPS2, SYSTEMPAY, OGONE, PAYBOX, PAYZEN,
              TIPI, PAYFIP_WS, KEYWARE, MOLLIE, SAGA]


def get_backends():
    '''Return a dictionnary mapping existing eopayment backends name to their
       description.

          >>> get_backends()['dummy'].description['caption']
          'Dummy payment backend'

    '''
    return dict((backend, get_backend(backend)) for backend in __BACKENDS)


class Payment(object):
    '''
       Interface to credit card online payment servers of French banks. The
       only use case supported for now is a unique automatic payment.

           >>> options = {
                   'numcli': '12345',
               }
           >>> p = Payment(kind=TIPI, options=options)
           >>> transaction_id, kind, data = p.request('10.00', email='bob@example.com')
           >>> print (transaction_id, kind, data) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
           ('...', 1, 'https://www.payfip.gov.fr/tpa/paiement.web?...')

       Supported backend of French banks are:

        - TIPI/PayFiP
        - SIPS 2.0, for BNP, Banque Populaire (before 2010), CCF, HSBC, Crédit
          Agricole, La Banque Postale, LCL, Société Générale and Crédit du
          Nord.
        - SystemPay v2/Payzen for Banque Populaire and Caise d'Epargne (Natixis, after 2010)
        - Ogone
        - Paybox
        - Mollie (Belgium)
        - Keyware (Belgium)

       For SIPs you also need the bank provided middleware especially the two
       executables, request and response, as the protocol from ATOS/SIPS is not
       documented. For the other backends the modules are autonomous.

       Each backend need some configuration parameters to be used, the
       description of the backend list those parameters. The description
       dictionary can be used to generate configuration forms.

           >>> d = get_backend(SPPLUS).description
           >>> print d['caption']
           SPPlus payment service of French bank Caisse d'epargne
           >>> print [p['name'] for p in d['parameters']] # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
           ['cle', ..., 'moyen']
           >>> print d['parameters'][0]['caption']
           Secret key, a 40 digits hexadecimal number

    '''

    def __init__(self, kind, options, logger=None):
        self.kind = kind
        self.backend = get_backend(kind)(options, logger=logger)

    def request(self, amount, **kwargs):
        '''Request a payment to the payment backend.

          Arguments:
          amount -- the amount of money to ask
          email -- the email of the customer (optional)
          usually redundant with the hardwired settings in the bank
          configuration panel. At this url you must use the Payment.response
          method to analyze the bank returned values.

          It returns a triple of values, (transaction_id, kind, data):
            - the first gives a string value to later match the payment with
              the invoice,
            - kind gives the type of the third value, payment.URL or
              payment.HTML or payment.FORM,
            - the third is the URL or the HTML form to contact the payment
              server, which must be sent to the customer browser.
        '''
        logger.debug(u'%r' % kwargs)

        if 'capture_date' in kwargs:
            capture_date = kwargs.pop('capture_date')

            delay_param = False
            for parameter in self.backend.description['parameters']:
                if parameter['name'] == 'capture_day':
                    delay_param = True
                    break

            if not delay_param:
                raise ValueError('capture_date is not supported by the backend.')

            if not isinstance(capture_date, datetime.date):
                raise ValueError('capture_date should be a datetime.date object.')

            # backend timezone should come from some backend configuration
            backend_tz = pytz.timezone('Europe/Paris')
            utc_tz = pytz.timezone('Etc/UTC')
            backend_trans_date = utc_tz.localize(
                datetime.datetime.utcnow()).astimezone(backend_tz)
            capture_day = (capture_date - backend_trans_date.date()).days
            if capture_day <= 0:
                raise ValueError("capture_date needs to be superior to the transaction date.")

            kwargs['capture_day'] = force_text(capture_day)

        return self.backend.request(amount, **kwargs)

    def response(self, query_string, **kwargs):
        '''
          Process a response from the Bank API. It must be used on the URL
          where the user browser of the payment server is going to post the
          result of the payment. Beware it can happen multiple times for the
          same payment, so you MUST support multiple notification of the same
          event, i.e. it should be idempotent. For example if you already
          validated some invoice, receiving a new payment notification for the
          same invoice should alter this state change.

          Beware that when notified directly by the bank (and not through the
          customer browser) no applicative session will exist, so you should
          not depend on it in your handler.

          Arguments:
          query_string -- the URL encoded form-data from a GET or a POST

          It returns a quadruplet of values:

             (result, transaction_id, bank_data, return_content)

           - result is a boolean stating whether the transaction worked, use it
             to decide whether to act on a valid payment,
           - the transaction_id return the same id than returned by request
             when requesting for the payment, use it to find the invoice or
             transaction which is linked to the payment,
           - bank_data is a dictionnary of the data sent by the bank, it should
             be logged for security reasons,
           - return_content, if not None you must return this content as the
             result of the HTTP request, it's used when the bank is calling
             your site as a web service.

        '''
        return self.backend.response(query_string, **kwargs)

    def cancel(self, amount, bank_data, **kwargs):
        '''
           Cancel or edit the amount of a transaction sent to the bank.

           Arguments:
           - amount -- the amount of money to cancel
           - bank_data -- the transaction dictionary received from the bank
        '''
        return self.backend.cancel(amount, bank_data, **kwargs)

    def validate(self, amount, bank_data, **kwargs):
        '''
           Validate and trigger the transmission of a transaction to the bank.

           Arguments:
           - amount -- the amount of money
           - bank_data -- the transaction dictionary received from the bank
        '''
        return self.backend.validate(amount, bank_data, **kwargs)

    def get_parameters(self, scope='global'):
        res = []
        for param in self.backend.description.get('parameters', []):
            if param.get('scope', 'global') != scope:
                continue
            res.append(param)
        return res

    @property
    def has_free_transaction_id(self):
        return self.backend.has_free_transaction_id

    def payment_status(self, transaction_id, **kwargs):
        if not self.backend.payment_status:
            raise NotImplementedError('payment_status is not implemented on this backend')
        return self.backend.payment_status(transaction_id=transaction_id, **kwargs)

    @property
    def has_payment_status(self):
        return hasattr(self.backend, 'payment_status')
