# -*- coding: utf-8
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

import codecs
from collections import OrderedDict
import datetime
import logging
import hashlib
import hmac
import re
import requests
import uuid

import pytz

from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA

import six
from six.moves.urllib import parse as urlparse
from six.moves.urllib import parse as urllib

import base64
import warnings

from .common import (PaymentCommon, PaymentResponse, FORM, PAID, CANCELLED,
                     DENIED, ERROR, Form, ResponseError, force_text,
                     force_byte, _)
from . import cb

__all__ = ['sign', 'Payment']

PAYBOX_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDe+hkicNP7ROHUssGNtHwiT2Ew
HFrSk/qwrcq8v5metRtTTFPE/nmzSkRnTs3GMpi57rBdxBBJW5W9cpNyGUh0jNXc
VrOSClpD5Ri2hER/GcNrxVRP7RlWOqB1C03q4QYmwjHZ+zlM4OUhCCAtSWflB4wC
Ka1g88CjFwRw/PB9kwIDAQAB
-----END PUBLIC KEY-----'''

VARS = {
    'PBX_SITE': 'Numéro de site (fourni par Paybox)',
    'PBX_RANG': 'Numéro de rang (fourni par Paybox)',
    'PBX_IDENTIFIANT': 'Identifiant interne (fourni par Paybox)',
    'PBX_TOTAL': 'Montant total de la transaction',
    'PBX_DEVISE': 'Devise de la transaction',
    'PBX_CMD': 'Référence commande côté commerçant',
    'PBX_PORTEUR': 'Adresse E - mail de l’acheteur',
    'PBX_RETOUR': 'Liste des variables à retourner par Paybox',
    'PBX_HASH': 'Type d’algorit hme de hachage pour le calcul de l’empreinte',
    'PBX_TIME': 'Horodatage de la transaction',
    'PBX_HMAC': 'Signature calculée avec la clé secrète',
}

PAYBOX_ERROR_CODES = {
    '00000': {'message': 'Paiement réalisé avec succés.', 'result': PAID},
    '00001': {
        'message': 'Demande annulée par l\'usager.',
        'result': CANCELLED,
    },
    '001xx': {
        'message': 'Paiement refusé par le centre d’autorisation [voir '
        '§12.112.1 Codes réponses du centre d’autorisationCodes réponses du '
        'centre d’autorisation]. En cas d’autorisation de la transaction par '
        'le centre d’autorisation de la banque ou de l’établissement financier '
        'privatif, le code erreur “00100” sera en fait remplacé directement '
        'par “00000”.'
    },
    '00003': {
        'message': 'Erreur Paybox. Dans ce cas, il est souhaitable de faire une '
        'tentative sur le site secondaire FQDN tpeweb1.paybox.com.'
    },
    '00004': {'message': 'Numéro de porteur ou cryptogramme visuel invalide.'},
    '00006': {'message': 'Accès refusé ou site/rang/identifiant incorrect.'},
    '00008': {'message': 'Date de fin de validité incorrecte.'},
    '00009': {'message': 'Erreur de création d’un abonnement.'},
    '00010': {'message': 'Devise inconnue.'},
    '00011': {'message': 'Montant incorrect.'},
    '00015': {'message': 'Paiement déjà effectué.'},
    '00016': {
        'message': 'Abonné déjà existant (inscription nouvel abonné). Valeur '
        '‘U’ de la variable PBX_RETOUR.'
    },
    '00021': {'message': 'Carte non autorisée.', 'result': DENIED},
    '00029': {
        'message': 'Carte non conforme. Code erreur renvoyé lors de la documentation de la variable « PBX_EMPREINTE ».'
    },
    '00030': {
        'message': 'Temps d’attente > 15 mn par l’internaute/acheteur au niveau de la page de paiements.'
    },
    '00031': {'message': 'Réservé'},
    '00032': {'message': 'Réservé'},
    '00033': {
        'message': 'Code pays de l’adresse IP du navigateur de l’acheteur non autorisé.',
        'result': DENIED,
    },
    '00040': {
        'message': 'Opération sans authentification 3-DSecure, bloquée par le filtre.',
        'result': DENIED,
    },
    '99999': {
        'message': 'Opération en attente de validation par l’émetteur du moyen de paiement.'
    },
}

ALGOS = {
    'SHA512': hashlib.sha512,
    'SHA256': hashlib.sha256,
    'SHA384': hashlib.sha384,
    'SHA224': hashlib.sha224,
}

URLS = {
    'test':
        'https://preprod-tpeweb.paybox.com/cgi/MYchoix_pagepaiement.cgi',
    'prod':
        'https://tpeweb.paybox.com/cgi/MYchoix_pagepaiement.cgi',
    'backup':
        'https://tpeweb1.paybox.com/cgi/MYchoix_pagepaiement.cgi',
}

PAYBOX_DIRECT_URLS = {
    'test': 'https://preprod-ppps.paybox.com/PPPS.php',
    'prod': 'https://ppps.paybox.com/PPPS.php',
    'backup': 'https://ppps1.paybox.com/PPPS.php'
}

PAYBOX_DIRECT_CANCEL_OPERATION = '00055'
PAYBOX_DIRECT_VALIDATE_OPERATION = '00002'

PAYBOX_DIRECT_VERSION_NUMBER = '00103'

PAYBOX_DIRECT_SUCCESS_RESPONSE_CODE = '00000'

# payment modes
PAYMENT_MODES = {'AUTHOR_CAPTURE': 'O',
                 'IMMEDIATE': 'N'}


def sign(data, key):
    '''Take a list of tuple key, value and sign it by building a string to
       sign.
    '''
    logger = logging.getLogger(__name__)
    algo = None
    logger.debug('signature key %r', key)
    logger.debug('signed data %r', data)
    for k, v in data:
        if k == 'PBX_HASH' and v in ALGOS:
            algo = ALGOS[v]
            break
    assert algo, 'Missing or invalid PBX_HASH'
    tosign = ['%s=%s' % (k, force_text(v)) for k, v in data]
    tosign = '&'.join(tosign)
    logger.debug('signed string %r', tosign)
    tosign = tosign.encode('utf-8')
    signature = hmac.new(key, tosign, algo)
    return tuple(data) + (('PBX_HMAC', signature.hexdigest().upper()),)


def verify(data, signature, key=PAYBOX_KEY):
    '''Verify signature using SHA1withRSA by Paybox'''
    key = RSA.importKey(key)
    h = SHA.new(force_byte(data))
    verifier = PKCS1_v1_5.new(key)
    return verifier.verify(h, signature)


class Payment(PaymentCommon):
    '''Paybox backend for eopayment.

       If you want to handle Instant Payment Notification, you must pass
       provide a automatic_return_url option specifying the URL of the
       callback endpoint.

       Email is mandatory to emit payment requests with paybox.

       IP adresses to authorize:
                                 IN           OUT
           test           195.101.99.73 195.101.99.76
           production     194.2.160.66  194.2.122.158
           backup         195.25.7.146  195.25.7.166
    '''
    callback = None

    description = {
        'caption': _('Paybox'),
        'parameters': [
            {
                'name': 'normal_return_url',
                'caption': _('Normal return URL'),
                'default': '',
                'required': False,
            },
            {
                'name': 'automatic_return_url',
                'caption': _('Automatic return URL'),
                'required': False,
            },
            {
                'name': 'platform',
                'caption': 'Plateforme cible',
                'default': 'test',
                'choices': (
                    ('test', 'Test'),
                    ('backup', 'Backup'),
                    ('prod', 'Production'),
                )
            },
            {
                'name': 'site',
                'caption': 'Numéro de site',
                'required': True,
                'validation': lambda x: isinstance(x, six.string_types)
                and x.isdigit() and len(x) == 7,
            },
            {
                'name': 'cle',
                'caption': 'Clé',
                'help_text': 'Uniquement nécessaire pour l\'annulation / remboursement / encaissement (PayBox Direct)',
                'required': False,
                'validation': lambda x: isinstance(x, six.string_types),
            },
            {
                'name': 'rang',
                'caption': 'Numéro de rang',
                'required': True,
                'validation': lambda x: isinstance(x, six.string_types)
                and x.isdigit() and len(x) == 3,
            },
            {
                'name': 'identifiant',
                'caption': 'Identifiant',
                'required': True,
                'validation': lambda x: isinstance(x, six.string_types)
                and x.isdigit() and (0 < len(x) < 10),
            },
            {
                'name': 'shared_secret',
                'caption': 'Secret partagé (clé HMAC)',
                'validation': lambda x: isinstance(x, str)
                and all(a.lower() in '0123456789abcdef' for a in x),
                'required': True,
            },
            {
                'name': 'devise',
                'caption': 'Devise',
                'default': '978',
                'choices': (
                    ('978', 'Euro'),
                ),
            },
            {
                'name': 'callback',
                'caption': _('Callback URL'),
                'deprecated': True,
            },
            {
                'name': 'capture_day',
                'caption': 'Nombre de jours pour un paiement différé',
                'default': '',
                'required': False,
                'validation': lambda x: isinstance(x, six.string_types)
                and x.isdigit() and (1 <= len(x) <= 2)
            },
            {
                'name': 'capture_mode',
                'caption': _('Capture Mode'),
                'default': 'IMMEDIATE',
                'required': False,
                'choices': list(PAYMENT_MODES)
            },
            {
                'name': 'manual_validation',
                'caption': 'Validation manuelle',
                'type': bool,
                'default': False,
                'scope': 'transaction'
            },
            {
                'name': 'timezone',
                'caption': _('Default Timezone'),
                'default': 'Europe/Paris',
                'required': False,
            }
        ]
    }

    def make_pbx_cmd(self, guid, orderid=None, transaction_id=None):
        if not transaction_id:
            date = datetime.datetime.now(pytz.timezone(self.timezone)).strftime('%Y-%m-%dT%H%M%S')
            transaction_id = '%s_%s' % (date, guid)
        pbx_cmd = transaction_id
        if orderid:
            pbx_cmd += '!' + orderid
        return pbx_cmd

    def request(self, amount, email, name=None, orderid=None, manual_validation=None, **kwargs):
        d = OrderedDict()
        d['PBX_SITE'] = force_text(self.site)
        d['PBX_RANG'] = force_text(self.rang).strip()[-3:]
        d['PBX_IDENTIFIANT'] = force_text(self.identifiant)
        d['PBX_TOTAL'] = self.clean_amount(amount)
        d['PBX_DEVISE'] = force_text(self.devise)
        guid = str(uuid.uuid4().hex)
        transaction_id = d['PBX_CMD'] = self.make_pbx_cmd(guid=guid,
                                                          transaction_id=kwargs.get('transaction_id'),
                                                          orderid=orderid)
        d['PBX_PORTEUR'] = force_text(email)
        d['PBX_RETOUR'] = (
            'montant:M;reference:R;code_autorisation:A;erreur:E;numero_appel:T;'
            'numero_transaction:S;'
            'date_transaction:W;heure_transaction:Q;'
            'signature:K'
        )
        d['PBX_HASH'] = 'SHA512'
        d['PBX_TIME'] = kwargs.get('time') or (
            force_text(datetime.datetime.utcnow().isoformat('T')).split('.')[0]
            + '+00:00')
        d['PBX_ARCHIVAGE'] = orderid or guid
        if self.normal_return_url:
            d['PBX_EFFECTUE'] = self.normal_return_url
            d['PBX_REFUSE'] = self.normal_return_url
            d['PBX_ANNULE'] = self.normal_return_url
            d['PBX_ATTENTE'] = self.normal_return_url
        automatic_return_url = self.automatic_return_url
        if not automatic_return_url and self.callback:
            warnings.warn("callback option is deprecated, "
                          "use automatic_return_url", DeprecationWarning)
            automatic_return_url = self.callback
        capture_day = capture_day = kwargs.get('capture_day', self.capture_day)
        if capture_day:
            d['PBX_DIFF'] = capture_day.zfill(2)
        d['PBX_AUTOSEULE'] = PAYMENT_MODES[self.capture_mode]
        if manual_validation:
            d['PBX_AUTOSEULE'] = PAYMENT_MODES['AUTHOR_CAPTURE']
        if automatic_return_url:
            d['PBX_REPONDRE_A'] = force_text(automatic_return_url)
        d = d.items()

        if six.PY3:
            shared_secret = codecs.decode(bytes(self.shared_secret, 'ascii'), 'hex')
        else:
            shared_secret = codecs.decode(bytes(self.shared_secret), 'hex')
        d = sign(d, shared_secret)
        url = URLS[self.platform]
        fields = []
        for k, v in d:
            fields.append({
                'type': u'hidden',
                'name': force_text(k),
                'value': force_text(v),
            })
        form = Form(url, 'POST', fields, submit_name=None,
                    submit_value=u'Envoyer', encoding='utf-8')
        return transaction_id, FORM, form

    def response(self, query_string, callback=False, **kwargs):
        d = urlparse.parse_qs(query_string, True, False)
        if not set(d) >= set(['erreur', 'reference']):
            raise ResponseError('missing erreur or reference')
        signed = False
        if 'signature' in d:
            sig = d['signature'][0]
            sig = base64.b64decode(sig)
            data = []
            if callback:
                for key in ('montant', 'reference', 'code_autorisation',
                            'erreur', 'numero_appel', 'numero_transaction',
                            'date_transaction', 'heure_transaction'):
                    data.append('%s=%s' % (key, urllib.quote(d[key][0])))
            else:
                for key, value in urlparse.parse_qsl(query_string, True, True):
                    if key == 'signature':
                        break
                    data.append('%s=%s' % (key, urllib.quote(value)))
            data = '&'.join(data)
            signed = verify(data, sig)
        erreur = d['erreur'][0]
        if re.match(r'^001[0-9][0-9]$', erreur):
            cb_error_code = erreur[3:5]
            message, result = cb.translate_cb_error_code(cb_error_code)
        elif erreur in PAYBOX_ERROR_CODES:
            message = PAYBOX_ERROR_CODES[erreur]['message']
            result = PAYBOX_ERROR_CODES[erreur].get('result', ERROR)
        else:
            message = 'Code erreur inconnu %s' % erreur
            result = ERROR
        pbx_cmd = d['reference'][0]
        transaction_date = None
        if 'date_transaction' in d and 'heure_transaction' in d:
            try:
                full_date_string = '%sT%s' % (d['date_transaction'][0], d['heure_transaction'][0])
                transaction_date = datetime.datetime.strptime(full_date_string, '%Y%m%dT%H:%M:%S')
            except ValueError:
                pass
            else:
                # We suppose Europe/Paris is the default timezone for Paybox
                # servers.
                paris_tz = pytz.timezone(self.timezone)
                transaction_date = paris_tz.localize(transaction_date)
        return PaymentResponse(
            order_id=pbx_cmd,
            signed=signed,
            bank_data=d,
            result=result,
            bank_status=message,
            transaction_date=transaction_date)

    def perform(self, amount, bank_data, operation):
        logger = logging.getLogger(__name__)
        url = PAYBOX_DIRECT_URLS[self.platform]
        params = {
            'VERSION': PAYBOX_DIRECT_VERSION_NUMBER,
            'TYPE': operation,
            'SITE': force_text(self.site),
            'RANG': self.rang.strip(),
            'CLE': force_text(self.cle),
            'NUMQUESTION': bank_data['numero_transaction'][0].zfill(10),
            'MONTANT': self.clean_amount(amount),
            'DEVISE': force_text(self.devise),
            'NUMTRANS': bank_data['numero_transaction'][0],  # paybox transaction number
            'NUMAPPEL': bank_data['numero_appel'][0],
            'REFERENCE': bank_data['reference'][0],
            'DATEQ': datetime.datetime.now().strftime('%d%m%Y%H%M%S'),
        }
        response = requests.post(url, params)
        response.raise_for_status()
        logger.debug('received %r', response.text)
        data = dict(urlparse.parse_qsl(response.text, True, True))
        if data.get('CODEREPONSE') != PAYBOX_DIRECT_SUCCESS_RESPONSE_CODE:
            if six.PY2:
                raise ResponseError(data['COMMENTAIRE'].encode('utf-8'))
            raise ResponseError(data['COMMENTAIRE'])
        return data

    def validate(self, amount, bank_data, **kwargs):
        return self.perform(amount, bank_data, PAYBOX_DIRECT_VALIDATE_OPERATION)

    def cancel(self, amount, bank_data, **kwargs):
        return self.perform(amount, bank_data, PAYBOX_DIRECT_CANCEL_OPERATION)
