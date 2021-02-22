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

import base64
import pytz
import datetime as dt
import hashlib
import hmac
import random
import re
import string
import six
from six.moves.urllib import parse as urlparse
import warnings

from .common import (PaymentCommon, PaymentResponse, PAID, DENIED, CANCELLED,
                     ERROR, FORM, Form, ResponseError, force_text, force_byte, _)
from .cb import translate_cb_error_code

__all__ = ['Payment']

VADS_TRANS_DATE = 'vads_trans_date'
VADS_AUTH_NUMBER = 'vads_auth_number'
VADS_AUTH_RESULT = 'vads_auth_result'
VADS_RESULT = 'vads_result'
VADS_EXTRA_RESULT = 'vads_extra_result'
VADS_CUST_EMAIL = 'vads_cust_email'
VADS_CUST_NAME = 'vads_cust_name'
VADS_CUST_PHONE = 'vads_cust_phone'
VADS_CUST_INFO1 = 'vads_order_info'
VADS_CUST_INFO2 = 'vads_order_info2'
VADS_CUST_INFO3 = 'vads_order_info3'
VADS_CUST_FIRST_NAME = 'vads_cust_first_name'
VADS_CUST_LAST_NAME = 'vads_cust_last_name'
VADS_URL_RETURN = 'vads_url_return'
VADS_AMOUNT = 'vads_amount'
VADS_SITE_ID = 'vads_site_id'
VADS_TRANS_ID = 'vads_trans_id'
SIGNATURE = 'signature'
VADS_CTX_MODE = 'vads_ctx_mode'
VADS_EFFECTIVE_CREATION_DATE = 'vads_effective_creation_date'
VADS_EOPAYMENT_TRANS_ID = 'vads_ext_info_eopayment_trans_id'


def isonow():
    return dt.datetime.utcnow().isoformat('T').replace('-', '') \
        .replace('T', '').replace(':', '')[:14]


def parse_utc(value):
    try:
        naive_dt = dt.datetime.strptime(value, '%Y%m%d%H%M%S')
    except ValueError:
        return None
    return pytz.utc.localize(naive_dt)


class Parameter:
    def __init__(self, name, ptype, code, max_length=None, length=None,
                 needed=False, default=None, choices=None, description=None,
                 help_text=None):
        self.name = name
        self.ptype = ptype
        self.code = code
        self.max_length = max_length
        self.length = length
        self.needed = needed
        self.default = default
        self.choices = choices
        self.description = description
        self.help_text = help_text

    def check_value(self, value):
        if self.length and len(value) != self.length:
            return False
        if self.max_length and len(value) > self.max_length:
            return False
        if self.choices and value not in self.choices:
            return False
        if value == '':
            return True
        value = value.replace('.', '')
        if self.ptype == 'n':
            return value.isdigit()
        elif self.ptype == 'an':
            return value.isalnum()
        elif self.ptype == 'an-':
            return value.replace('-', '').isalnum()
        elif self.ptype == 'an;':
            return value.replace(';', '').isalnum()
        return True


PARAMETERS = [
    # amount as euro cents
    Parameter('vads_action_mode', None, 47, needed=True, default='INTERACTIVE',
              choices=('SILENT', 'INTERACTIVE')),
    Parameter('vads_amount', 'n', 9, max_length=12, needed=True),
    Parameter('vads_capture_delay', 'n', 6, max_length=3, default=''),
    # Same as 'vads_capture_delay' but matches other backend naming for
    # deferred payment
    Parameter('capture_day', 'n', 6, max_length=3, default=''),
    Parameter('vads_contrib', 'ans', 31, max_length=255, default='eopayment'),
    # defaut currency = EURO, norme ISO4217
    Parameter('vads_currency', 'n', 10, length=3, default='978', needed=True),
    Parameter('vads_cust_address', 'an', 19, max_length=255),
    # code ISO 3166
    Parameter('vads_cust_country', 'a', 22, length=2, default='FR'),
    Parameter('vads_cust_email', 'an@', 15, max_length=127),
    Parameter('vads_cust_id', 'an', 16, max_length=63),
    Parameter('vads_cust_name', 'ans', 18, max_length=127),
    Parameter('vads_cust_phone', 'an', 23, max_length=63),
    Parameter('vads_cust_title', 'an', 17, max_length=63),
    Parameter('vads_cust_city', 'an', 21, max_length=63),
    Parameter('vads_cust_zip', 'an', 20, max_length=63),
    Parameter('vads_ctx_mode', 'a', 11, needed=True, choices=('TEST',
                                                              'PRODUCTION'),
              default='TEST'),
    # ISO 639 code
    Parameter('vads_language', 'a', 12, length=2, default='fr'),
    Parameter('vads_order_id', 'an-', 13, max_length=32),
    Parameter('vads_order_info', 'an', 14, max_length=255,
              description="Complément d'information 1"),
    Parameter('vads_order_info2', 'an', 14, max_length=255,
              description="Complément d'information 2"),
    Parameter('vads_order_info3', 'an', 14, max_length=255,
              description="Complément d'information 3"),
    Parameter('vads_page_action', None, 46, needed=True, default='PAYMENT',
              choices=('PAYMENT',)),
    Parameter('vads_payment_cards', 'an;', 8, max_length=127, default='',
              description='Liste des cartes de paiement acceptées',
              help_text='vide ou des valeurs sépareés par un point-virgule '
                        'parmi AMEX, AURORE-MULTI, BUYSTER, CB, COFINOGA, '
                        'E-CARTEBLEUE, MASTERCARD, JCB, MAESTRO, ONEY, '
                        'ONEY_SANDBOX, PAYPAL, PAYPAL_SB, PAYSAFECARD, '
                        'VISA'),
    # must be SINGLE or MULTI with parameters
    Parameter('vads_payment_config', '', 7, default='SINGLE',
              choices=('SINGLE', 'MULTI'), needed=True),
    Parameter('vads_return_mode', None, 48, default='GET',
              choices=('', 'NONE', 'POST', 'GET')),
    Parameter('signature', 'an', None, length=40),
    Parameter('vads_site_id', 'n', 2, length=8, needed=True,
              description='Identifiant de la boutique'),
    Parameter('vads_theme_config', 'ans', 32, max_length=255),
    Parameter(VADS_TRANS_DATE, 'n', 4, length=14, needed=True,
              default=isonow),
    # https://paiement.systempay.fr/doc/fr-FR/form-payment/reference/vads-trans-id.html
    Parameter('vads_trans_id', 'an', 3, length=6, needed=True),
    Parameter('vads_validation_mode', 'n', 5, max_length=1, choices=('', '0', '1'),
              default=''),
    Parameter('vads_version', 'an', 1, default='V2', needed=True,
              choices=('V2',)),
    Parameter('vads_url_success', 'ans', 24, max_length=1024),
    Parameter('vads_url_referral', 'ans', 26, max_length=127),
    Parameter('vads_url_refused', 'ans', 25, max_length=1024),
    Parameter('vads_url_cancel', 'ans', 27, max_length=1024),
    Parameter('vads_url_error', 'ans', 29, max_length=1024),
    Parameter('vads_url_return', 'ans', 28, max_length=1024),
    Parameter('vads_user_info', 'ans', 61, max_length=255),
    Parameter('vads_contracts', 'ans', 62, max_length=255),
    Parameter(VADS_CUST_FIRST_NAME, 'ans', 104, max_length=63),
    Parameter(VADS_CUST_LAST_NAME, 'ans', 104, max_length=63),
]
PARAMETER_MAP = dict(((parameter.name,
                       parameter) for parameter in PARAMETERS))


def add_vads(kwargs):
    new_vargs = {}
    for k, v in kwargs.items():
        if k.startswith('vads_'):
            new_vargs[k] = v
        else:
            new_vargs['vads_' + k] = v
    return new_vargs


def check_vads(kwargs, exclude=[]):
    for parameter in PARAMETERS:
        name = parameter.name
        if name not in kwargs and name not in exclude and parameter.needed:
            raise ValueError('parameter %s must be defined' % name)
        if name in kwargs and not parameter.check_value(kwargs[name]):
            raise ValueError('parameter %s value %s is not of the type %s' % (
                name, kwargs[name],
                parameter.ptype))


class Payment(PaymentCommon):
    '''
        Produce request for and verify response from the SystemPay payment
        gateway.

            >>> gw =Payment(dict(secret_test='xxx', secret_production='yyyy',
                                 site_id=123, ctx_mode='PRODUCTION'))
            >>> print gw.request(100)
            ('20120525093304_188620',
            'https://paiement.systempay.fr/vads-payment/?vads_url_return=http%3A%2F%2Furl.de.retour%2Fretour.php&vads_cust_country=FR&vads_site_id=&vads_payment_config=SINGLE&vads_trans_id=188620&vads_action_mode=INTERACTIVE&vads_contrib=eopayment&vads_page_action=PAYMENT&vads_trans_date=20120525093304&vads_ctx_mode=TEST&vads_validation_mode=&vads_version=V2&vads_payment_cards=&signature=5d412498ab523627ec5730a09118f75afa602af5&vads_language=fr&vads_capture_delay=&vads_currency=978&vads_amount=100&vads_return_mode=NONE',
            {'vads_url_return': 'http://url.de.retour/retour.php',
            'vads_cust_country': 'FR', 'vads_site_id': '',
            'vads_payment_config': 'SINGLE', 'vads_trans_id': '188620',
            'vads_action_mode': 'INTERACTIVE', 'vads_contrib': 'eopayment',
            'vads_page_action': 'PAYMENT', 'vads_trans_date': '20120525093304',
            'vads_ctx_mode': 'TEST', 'vads_validation_mode': '',
            'vads_version': 'V2', 'vads_payment_cards': '', 'signature':
            '5d412498ab523627ec5730a09118f75afa602af5', 'vads_language': 'fr',
            'vads_capture_delay': '', 'vads_currency': '978', 'vads_amount': 100,
            'vads_return_mode': 'NONE'})

    '''
    has_free_transaction_id = True
    service_url = "https://paiement.systempay.fr/vads-payment/"
    signature_algo = 'sha1'

    description = {
        'caption': 'SystemPay, système de paiement du groupe BPCE',
        'parameters': [
            {
                'name': 'normal_return_url',
                'caption': _('Normal return URL'),
                'default': '',
                'required': True,
            },
            {
                'name': 'automatic_return_url',
                'caption': _('Automatic return URL (ignored, must be set in Payzen/SystemPay backoffice)'),
                'required': False,
            },
            {'name': 'service_url',
                'default': service_url,
                'caption': 'URL du service de paiement',
                'help_text': 'ne pas modifier si vous ne savez pas',
                'validation': lambda x: x.startswith('http'),
                'required': True, },
            {'name': 'secret_test',
                'caption': 'Secret pour la configuration de TEST',
                'validation': lambda value: str.isalnum(value),
                'required': True, },
            {'name': 'secret_production',
                'caption': 'Secret pour la configuration de PRODUCTION',
                'validation': lambda value: str.isalnum(value), },
            {'name': 'signature_algo',
                'caption': 'Algorithme de signature',
                'default': 'sha1',
                'choices': (
                    ('sha1', 'SHA-1'),
                    ('hmac_sha256', 'HMAC-SHA-256'),
                )},
            {
                'name': 'manual_validation',
                'caption': 'Validation manuelle',
                'type': bool,
                'default': False,
                'scope': 'transaction'
            }
        ]
    }

    for name in ('vads_ctx_mode', VADS_SITE_ID, 'vads_order_info',
                 'vads_order_info2', 'vads_order_info3',
                 'vads_payment_cards', 'vads_payment_config', 'capture_day'):
        parameter = PARAMETER_MAP[name]

        def check_value(parameter):
            def validate(value):
                return parameter.check_value(value)
            return validate

        x = {'name': name,
             'caption': parameter.description or name,
             'validation': check_value(parameter),
             'default': parameter.default,
             'required': parameter.needed,
             'help_text': parameter.help_text,
             'max_length': parameter.max_length}
        description['parameters'].append(x)

    def __init__(self, options, logger=None):
        super(Payment, self).__init__(options, logger=logger)
        options = add_vads(options)
        self.options = options

    def make_vads_trans_id(self):
        # vads_trans_id must be 6 alphanumeric characters,
        # trans_id starting with 9 are reserved for the systempay backoffice
        # https://paiement.systempay.fr/doc/fr-FR/form-payment/reference/vads-trans-id.html
        gen = random.SystemRandom()
        if six.PY3:
            alphabet = string.ascii_letters + string.digits
        else:
            alphabet = string.letters + string.digits
        first_letter_alphabet = alphabet.replace('9', '')
        vads_trans_id = (
            gen.choice(first_letter_alphabet)
            + ''.join(gen.choice(alphabet) for i in range(5))
        )
        return vads_trans_id

    def request(self, amount, name=None, first_name=None, last_name=None,
                address=None, email=None, phone=None, orderid=None, info1=None,
                info2=None, info3=None, next_url=None, manual_validation=None,
                transaction_id=None, **kwargs):
        '''
           Create the URL string to send a request to SystemPay
        '''
        self.logger.debug('%s amount %s name %s address %s email %s phone %s '
                          'next_url %s info1 %s info2 %s info3 %s kwargs: %s',
                          __name__, amount, name, address, email, phone, info1,
                          info2, info3, next_url, kwargs)
        # amount unit is cents
        amount = '%.0f' % (100 * amount)
        kwargs.update(add_vads({'amount': force_text(amount)}))
        if int(amount) < 0:
            raise ValueError('amount must be an integer >= 0')
        normal_return_url = self.normal_return_url
        if next_url:
            warnings.warn("passing next_url to request() is deprecated, "
                          "set normal_return_url in options", DeprecationWarning)
            normal_return_url = next_url
        if normal_return_url:
            kwargs[VADS_URL_RETURN] = force_text(normal_return_url)
        if name is not None:
            kwargs['vads_cust_name'] = force_text(name)
        if first_name is not None:
            kwargs[VADS_CUST_FIRST_NAME] = force_text(first_name)
        if last_name is not None:
            kwargs[VADS_CUST_LAST_NAME] = force_text(last_name)

        if address is not None:
            kwargs['vads_cust_address'] = force_text(address)
        if email is not None:
            kwargs['vads_cust_email'] = force_text(email)
        if phone is not None:
            kwargs['vads_cust_phone'] = force_text(phone)
        if info1 is not None:
            kwargs['vads_order_info'] = force_text(info1)
        if info2 is not None:
            kwargs['vads_order_info2'] = force_text(info2)
        if info3 is not None:
            kwargs['vads_order_info3'] = force_text(info3)
        if orderid is not None:
            # check orderid format first
            name = 'vads_order_id'
            orderid = force_text(orderid)
            ptype = 'an-'
            p = Parameter(name, ptype, 13, max_length=32)
            if not p.check_value(orderid):
                raise ValueError(
                    '%s value %s is not of the type %s' % (name, orderid, ptype))
            kwargs[name] = orderid

        vads_trans_id = self.make_vads_trans_id()
        assert re.match(r'^[0-9a-zA-Z]{6}$', vads_trans_id)

        kwargs[VADS_TRANS_ID] = vads_trans_id
        fields = kwargs
        for parameter in PARAMETERS:
            name = parameter.name
            # import default parameters from configuration
            if name not in fields \
                    and name in self.options:
                fields[name] = force_text(self.options[name])
            # import default parameters from module
            if name not in fields and parameter.default is not None:
                if callable(parameter.default):
                    fields[name] = parameter.default()
                else:
                    fields[name] = parameter.default
        capture_day = fields.pop('capture_day')
        if capture_day:
            fields['vads_capture_delay'] = capture_day
        if manual_validation:
            fields['vads_validation_mode'] = '1'
        check_vads(fields)
        if transaction_id:
            fields[VADS_EOPAYMENT_TRANS_ID] = transaction_id
        else:
            transaction_id = '%s_%s' % (fields[VADS_TRANS_DATE], vads_trans_id)
        fields[SIGNATURE] = force_text(self.signature(fields))
        self.logger.debug('%s request contains fields: %s', __name__, fields)
        self.logger.debug('%s transaction id: %s', __name__, transaction_id)
        form = Form(
            url=self.service_url,
            method='POST',
            fields=[
                {
                    'type': u'hidden',
                    'name': force_text(field_name),
                    'value': force_text(field_value),
                }
                for field_name, field_value in fields.items()])
        return transaction_id, FORM, form

    RESULT_MAP = {
        '00': {'message': 'Paiement réalisé avec succés.', 'result': PAID},
        '02': {'message': 'Le commerçant doit contacter la banque du porteur.'},
        '05': {'message': 'Paiement refusé.', 'result': DENIED},
        '17': {'message': 'Annulation client.', 'result': CANCELLED},
        '30': {'message': 'Erreur de format.'},
        '96': {'message': 'Erreur technique lors du paiement.'},
    }

    EXTRA_RESULT_MAP = {
        '': {'message': 'Pas de contrôle effectué.'},
        '00': {'message': 'Tous les contrôles se sont déroulés avec succés.'},
        '02': {'message': 'La carte a dépassé l\'encours autorisé.'},
        '03': {'message': 'La carte appartient à la liste grise du commerçant.'},
        '04': {'messaǵe': 'Le pays d\'émission de la carte appartient à la liste grise du '
               'commerçant ou le pays d\'émission de la carte n\'appartient pas à la '
               'liste blanche du commerçant.'},
        '05': {'message': 'L’adresse IP appartient à la liste grise du marchand.'},
        '06': {'message': 'Le code bin appartient à la liste grise du marchand.'},
        '07': {'message': 'Détection d’une e-carte bleue.'},
        '08': {'message': 'Détection d’une carte commerciale nationale.'},
        '09': {'message': 'Détection d’une carte commerciale étrangère.'},
        '14': {'message': 'Détection d’une carte à autorisation systématique.'},
        '30': {'message': 'Le pays de l’adresse IP appartient à la liste grise.'},
        '99': {'message': 'Problème technique recontré par le serveur lors du traitement '
               'd\'un des contrôles locauxi.'},
    }

    @classmethod
    def make_eopayment_result(cls, fields):
        # https://paiement.systempay.fr/doc/fr-FR/payment-file/oneclick-payment/vads-result.html
        # https://paiement.systempay.fr/doc/fr-FR/payment-file/oneclick-payment/vads-auth-result.html
        # https://paiement.systempay.fr/doc/fr-FR/payment-file/oneclick-payment/vads-extra-result.html
        vads_result = fields.get(VADS_RESULT)
        vads_auth_result = fields.get(VADS_AUTH_RESULT)
        vads_extra_result = fields.get(VADS_EXTRA_RESULT)

        # map to human messages and update return
        vads_result_message = cls.RESULT_MAP.get(vads_result, {}).get('message')
        if vads_result_message:
            fields[VADS_RESULT + '_message'] = vads_result_message

        vads_extra_result_message = cls.EXTRA_RESULT_MAP.get(vads_extra_result, {}).get('message')
        if vads_extra_result_message:
            fields[VADS_EXTRA_RESULT + '_message'] = vads_extra_result_message

        vads_auth_result_message, auth_eopayment_result = translate_cb_error_code(vads_auth_result)
        if vads_auth_result_message:
            fields[VADS_AUTH_RESULT + '_message'] = vads_auth_result_message

        # now build eopayment resume
        if vads_result is None:
            return ERROR, 'absence de champ vads_result'
        if vads_result_message is None:
            return ERROR, 'valeur vads_result inconnue'

        result = cls.RESULT_MAP[vads_result].get('result', ERROR)
        message = vads_result_message
        if vads_auth_result_message and (vads_result != '00' or vads_result != vads_auth_result):
            message += ' ' + vads_auth_result_message
        if vads_result in ('00', '05', '30') and vads_extra_result_message and vads_extra_result != '':
            message += ' ' + vads_extra_result_message
        if result == ERROR and auth_eopayment_result not in (PAID, ERROR, None):
            result = auth_eopayment_result
        return result, message

    def response(self, query_string, **kwargs):
        fields = urlparse.parse_qs(query_string, True)
        if not set(fields) >= set([SIGNATURE, VADS_CTX_MODE, VADS_AUTH_RESULT]):
            raise ResponseError('missing %s, %s or %s' % (SIGNATURE, VADS_CTX_MODE,
                                                          VADS_AUTH_RESULT))
        for key, value in fields.items():
            fields[key] = value[0]
        copy = fields.copy()
        signature = self.signature(fields)
        result, message = self.make_eopayment_result(copy)
        self.logger.debug('checking systempay response on: %r', copy)
        signature_result = signature == fields[SIGNATURE]
        if not signature_result:
            self.logger.debug('signature check: %s <!> %s', signature,
                              fields[SIGNATURE])

        if not signature_result:
            message += ' signature invalide.'

        test = fields[VADS_CTX_MODE] == 'TEST'
        if VADS_EOPAYMENT_TRANS_ID in fields:
            transaction_id = fields[VADS_EOPAYMENT_TRANS_ID]
        else:
            transaction_id = '%s_%s' % (copy[VADS_TRANS_DATE], copy[VADS_TRANS_ID])
        # the VADS_AUTH_NUMBER is the number to match payment in bank logs
        copy[self.BANK_ID] = copy.get(VADS_AUTH_NUMBER, '')
        transaction_date = None
        if VADS_EFFECTIVE_CREATION_DATE in fields:
            transaction_date = parse_utc(fields[VADS_EFFECTIVE_CREATION_DATE])
        response = PaymentResponse(
            result=result,
            signed=signature_result,
            bank_data=copy,
            order_id=transaction_id,
            transaction_id=transaction_id,
            bank_status=message,
            transaction_date=transaction_date,
            test=test)
        return response

    def sha1_sign(self, secret, signed_data):
        return hashlib.sha1(signed_data).hexdigest()

    def hmac_sha256_sign(self, secret, signed_data):
        digest = hmac.HMAC(secret, digestmod=hashlib.sha256, msg=signed_data).digest()
        return base64.b64encode(digest)

    def signature(self, fields):
        self.logger.debug('got fields %s to sign' % fields)
        ordered_keys = sorted(
            [key for key in fields.keys() if key.startswith('vads_')])
        self.logger.debug('ordered keys %s' % ordered_keys)
        ordered_fields = [force_byte(fields[key]) for key in ordered_keys]
        secret = force_byte(getattr(self, 'secret_%s' % fields['vads_ctx_mode'].lower()))
        signed_data = b'+'.join(ordered_fields)
        signed_data = b'%s+%s' % (signed_data, secret)
        self.logger.debug(u'generating signature on «%s»', signed_data)
        sign_method = getattr(self, '%s_sign' % self.signature_algo)
        sign = sign_method(secret, signed_data)
        self.logger.debug(u'signature «%s»', sign)
        return force_text(sign)
