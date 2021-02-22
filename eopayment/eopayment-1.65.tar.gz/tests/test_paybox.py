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


import codecs
from unittest import TestCase
from decimal import Decimal
import base64
import mock
import six
from six.moves.urllib import parse as urllib
from xml.etree import ElementTree as ET

import eopayment.paybox as paybox
import eopayment


BACKEND_PARAMS = {
    'platform': u'test',
    'site': u'12345678',
    'rang': u'001',
    'identifiant': u'12345678',
    'shared_secret': (
        u'0123456789ABCDEF0123456789ABCDEF01234'
        u'56789ABCDEF0123456789ABCDEF0123456789'
        u'ABCDEF0123456789ABCDEF0123456789ABCDE'
        u'F0123456789ABCDEF'
    ),
    'automatic_return_url': u'http://example.com/callback',
}


class PayboxTests(TestCase):
    if six.PY2:
        def assertRaisesRegex(self, *args, **kwargs):
            return self.assertRaisesRegexp(*args, **kwargs)

    def test_sign(self):
        key = (b'0123456789ABCDEF0123456789ABCDEF0123456789'
               b'ABCDEF0123456789ABCDEF0123456789ABCDEF0123'
               b'456789ABCDEF0123456789ABCDEF0123456789ABCD'
               b'EF')
        key = codecs.decode(key, 'hex')
        d = dict(paybox.sign([
            ['PBX_SITE', u'12345678'],
            ['PBX_RANG', u'32'],
            ['PBX_IDENTIFIANT', u'12345678'],
            ['PBX_TOTAL', u'999'],
            ['PBX_DEVISE', u'978'],
            ['PBX_CMD', u'appel à Paybox'],
            ['PBX_PORTEUR', u'test@paybox.com'],
            ['PBX_RETOUR', u'Mt:M;Ref:R;Auto:A;Erreur:E'],
            ['PBX_HASH', u'SHA512'],
            ['PBX_TIME', u'2015-06-08T16:21:16+02:00'],
        ], key))
        result = (
            '7E74D8E9A0DBB65AAE51C5C50C2668FD98FC99AED'
            'F18244BB1935F602B6C2E953B61FD84364F34FDB8'
            '8B049901C0A07F6040AF446BBF5589113F48A733D'
            '551D4'
        )
        self.assertIn('PBX_HMAC', d)
        self.assertEqual(d['PBX_HMAC'], result)

    def test_request(self):
        backend = eopayment.Payment('paybox', BACKEND_PARAMS)
        time = '2015-07-15T18:26:32+02:00'
        email = 'bdauvergne@entrouvert.com'
        order_id = '20160216'
        transaction = '1234'
        amount = '19.99'
        transaction_id, kind, what = backend.request(
            Decimal(amount), email=email, orderid=order_id,
            transaction_id=transaction, time=time, manual_validation=False)
        self.assertEqual(kind, eopayment.FORM)
        self.assertEqual(transaction_id, '%s!%s' % (transaction, order_id))
        root = ET.fromstring(str(what))
        self.assertEqual(root.tag, 'form')
        self.assertEqual(root.attrib['method'], 'POST')
        self.assertEqual(root.attrib['action'], paybox.URLS['test'])
        expected_form_values = {
            'PBX_RANG': '001',
            'PBX_SITE': '12345678',
            'PBX_IDENTIFIANT': '12345678',
            'PBX_RETOUR': (
                'montant:M;reference:R;code_autorisation:A;'
                'erreur:E;numero_appel:T;numero_transaction:S;'
                'date_transaction:W;heure_transaction:Q;signature:K'
            ),
            'PBX_TIME': time,
            'PBX_PORTEUR': email,
            'PBX_CMD': '%s!%s' % (transaction, order_id),
            'PBX_TOTAL': amount.replace('.', ''),
            'PBX_DEVISE': '978',
            'PBX_HASH': 'SHA512',
            'PBX_HMAC': (
                'A9F561A6EA79390F1741A6B72872470BC1A1688E4581'
                'F097EC80B99D2038413AB350F2F5429FFA4F8D426D99'
                'B72E038164642F6F9BA10D46837EE486EEB944A2'
            ),
            'PBX_ARCHIVAGE': '20160216',
            'PBX_REPONDRE_A': 'http://example.com/callback',
            'PBX_AUTOSEULE': 'N'
        }

        form_params = {}
        for node in root:
            self.assertIn(node.attrib['type'], ('hidden', 'submit'))
            if node.attrib['type'] == 'submit':
                self.assertEqual(set(node.attrib.keys()), set(['type', 'value']))
            if node.attrib['type'] == 'hidden':
                self.assertEqual(set(node.attrib.keys()), set(['type', 'name', 'value']))
                name = node.attrib['name']
                form_params[name] = node.attrib['value']
        assert form_params == expected_form_values

    def test_request_with_capture_day(self):
        params = BACKEND_PARAMS.copy()
        time = '2018-08-21T10:26:32+02:00'
        email = 'user@entrouvert.com'
        order_id = '20180821'
        transaction = '1234'
        amount = '42.99'

        for capture_day in ('7', '07'):
            params['capture_day'] = capture_day
            backend = eopayment.Payment('paybox', params)
            transaction_id, kind, what = backend.request(
                Decimal(amount), email=email, orderid=order_id,
                transaction_id=transaction, time=time)
            root = ET.fromstring(str(what))

            form_params = dict(
                ((node.attrib['name'], node.attrib['value']) for node in root if node.attrib['type'] == 'hidden'))
            self.assertIn('PBX_DIFF', form_params)
            self.assertEqual(form_params['PBX_DIFF'], '07')

        # capture_day can be used as a request argument
        params = BACKEND_PARAMS.copy()
        backend = eopayment.Payment('paybox', params)
        transaction_id, kind, what = backend.request(
            Decimal(amount), email=email, orderid=order_id,
            transaction_id=transaction, time=time, capture_day='2')
        root = ET.fromstring(str(what))

        form_params = dict(((
            node.attrib['name'], node.attrib['value']) for node in root
            if node.attrib['type'] == 'hidden'))
        self.assertIn('PBX_DIFF', form_params)
        self.assertEqual(form_params['PBX_DIFF'], '02')

        # capture_day passed as a request argument
        # overrides capture_day from backend params
        params = BACKEND_PARAMS.copy()
        params['capture_day'] = '7'
        backend = eopayment.Payment('paybox', params)
        transaction_id, kind, what = backend.request(
            Decimal(amount), email=email, orderid=order_id,
            transaction_id=transaction, time=time, capture_day='2')
        root = ET.fromstring(str(what))

        form_params = dict(((
            node.attrib['name'], node.attrib['value']) for node in root
            if node.attrib['type'] == 'hidden'))
        self.assertIn('PBX_DIFF', form_params)
        self.assertEqual(form_params['PBX_DIFF'], '02')

    def test_request_with_authorization_only(self):
        params = BACKEND_PARAMS.copy()
        time = '2018-08-21T10:26:32+02:00'
        email = 'user@entrouvert.com'
        order_id = '20180821'
        transaction = '1234'
        amount = '42.99'

        params['capture_mode'] = 'AUTHOR_CAPTURE'
        backend = eopayment.Payment('paybox', params)
        transaction_id, kind, what = backend.request(
            Decimal(amount), email=email, orderid=order_id,
            transaction_id=transaction, time=time)
        root = ET.fromstring(str(what))

        form_params = dict(
            ((node.attrib['name'], node.attrib['value']) for node in root if node.attrib['type'] == 'hidden'))
        self.assertEqual(form_params['PBX_AUTOSEULE'], 'O')

    def test_response(self):
        backend = eopayment.Payment('paybox', BACKEND_PARAMS)
        order_id = '20160216'
        transaction = '1234'
        reference = '%s!%s' % (transaction, order_id)
        data = {
            'montant': '4242',
            'reference': reference,
            'code_autorisation': 'A',
            'erreur': '00000',
            'date_transaction': '20200101',
            'heure_transaction': '01:01:01'}
        response = backend.response(urllib.urlencode(data))
        self.assertEqual(response.order_id, reference)
        assert not response.signed
        assert response.transaction_date.isoformat() == '2020-01-01T01:01:01+01:00'

        with self.assertRaisesRegex(eopayment.ResponseError, 'missing erreur or reference'):
            backend.response('foo=bar')

    def test_perform_operations(self):
        operations = {'validate': '00002', 'cancel': '00055'}
        for operation_name, operation_code in operations.items():
            params = BACKEND_PARAMS.copy()
            params['cle'] = 'cancelling_key'
            backend = eopayment.Payment('paybox', params)
            bank_data = {
                'numero_transaction': ['13957441'],
                'numero_appel': ['30310733'],
                'reference': ['830657461681'],
            }
            backend_raw_response = (
                u'NUMTRANS=0013989865&NUMAPPEL=0030378572&NUMQUESTION=0013989862'
                u'&SITE=1999888&RANG=32&AUTORISATION=XXXXXX&CODEREPONSE=00000'
                u'&COMMENTAIRE=Demande traitée avec succès&REFABONNE=&PORTEUR='
            )
            backend_expected_response = {"CODEREPONSE": "00000",
                                         "RANG": "32",
                                         "AUTORISATION": "XXXXXX",
                                         "NUMTRANS": "0013989865",
                                         "PORTEUR": "",
                                         "COMMENTAIRE": u"Demande traitée avec succès",
                                         "SITE": "1999888",
                                         "NUMAPPEL": "0030378572",
                                         "REFABONNE": "",
                                         "NUMQUESTION": "0013989862"}

            with mock.patch('eopayment.paybox.requests.post') as requests_post:
                response = mock.Mock(status_code=200, text=backend_raw_response)
                requests_post.return_value = response
                backend_response = getattr(backend, operation_name)(Decimal('10'), bank_data)
                self.assertEqual(requests_post.call_args[0][0], 'https://preprod-ppps.paybox.com/PPPS.php')
                params_sent = requests_post.call_args[0][1]
                # make sure the date parameter is present
                assert 'DATEQ' in params_sent
                # don't care about its value
                params_sent.pop('DATEQ')
                expected_params = {
                    'CLE': 'cancelling_key',
                    'VERSION': '00103',
                    'TYPE': operation_code,
                    'MONTANT': '1000',
                    'NUMAPPEL': '30310733',
                    'NUMTRANS': '13957441',
                    'NUMQUESTION': '0013957441',
                    'REFERENCE': '830657461681',
                    'RANG': backend.backend.rang,
                    'SITE': backend.backend.site,
                    'DEVISE': backend.backend.devise
                }
                self.assertEqual(params_sent, expected_params)
                self.assertEqual(backend_response, backend_expected_response)

                params['platform'] = 'prod'
                backend = eopayment.Payment('paybox', params)
                with mock.patch('eopayment.paybox.requests.post') as requests_post:
                    response = mock.Mock(status_code=200, text=backend_raw_response)
                    requests_post.return_value = response
                    getattr(backend, operation_name)(Decimal('10'), bank_data)
                    self.assertEqual(requests_post.call_args[0][0], 'https://ppps.paybox.com/PPPS.php')

                with mock.patch('eopayment.paybox.requests.post') as requests_post:
                    error_response = u"""CODEREPONSE=00015&COMMENTAIRE=PAYBOX : Transaction non trouvée"""
                    response = mock.Mock(status_code=200, text=error_response)
                    requests_post.return_value = response
                    self.assertRaisesRegex(
                        eopayment.ResponseError,
                        'Transaction non trouvée',
                        getattr(backend, operation_name),
                        Decimal('10'),
                        bank_data)

    def test_validate_payment(self):
        params = BACKEND_PARAMS.copy()
        params['cle'] = 'cancelling_key'
        backend = eopayment.Payment('paybox', params)
        bank_data = {
            'numero_transaction': ['13957441'],
            'numero_appel': ['30310733'],
            'reference': ['830657461681']
        }
        backend_raw_response = (
            u'NUMTRANS=0013989865&NUMAPPEL=0030378572&NUMQUESTION=0013989862'
            u'&SITE=1999888&RANG=32&AUTORISATION=XXXXXX&CODEREPONSE=00000'
            u'&COMMENTAIRE=Demande traitée avec succès&REFABONNE=&PORTEUR='
        )

        with mock.patch('eopayment.paybox.requests.post') as requests_post:
            response = mock.Mock(status_code=200, text=backend_raw_response)
            requests_post.return_value = response
            backend.validate(Decimal(12), bank_data)

    def test_rsa_signature_validation(self):
        pkey = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUgYufHuheMztK1LhQSG6xsOzb
UX4D2A/QcMvkEcRVXFx5tQqcE9/JnMqE41TF/ebn7jC/MBxxtPFkUN7+EZoeMN7x
OWzAMDm/xsCWRvvel4GGixgm3aQRUPyTrlm4Ksy32Ya0rNnEDMAvB3dxOn7cp8GR
ZdzrudBlevZXpr6iYwIDAQAB
-----END PUBLIC KEY-----'''
        data = 'coin\n'
        sig64 = '''VCt3sgT0ecacmDEWWNVXJ+jGmIPBMApK42tBJV0FlDjpllOGPy8MsAmLW4/QjTtx
z0Dkz0NjxvU+5WzQZh9Uuxr/egRCwV4NMRWqu0zaVVioeBvl4/5CWm4f4/1L9+0m
FBFKOZhgBJnkC+l6+XhT4aYWKaQ4ocmOMV92yjeXTE4='''
        self.assertTrue(paybox.verify(data, base64.b64decode(sig64), key=pkey))

    def test_request_manual_validation(self):
        params = BACKEND_PARAMS.copy()
        time = '2018-08-21T10:26:32+02:00'
        email = 'user@entrouvert.com'
        order_id = '20180821'
        transaction = '1234'
        amount = '42.99'

        backend = eopayment.Payment('paybox', params)

        transaction_id, kind, what = backend.request(
            Decimal(amount),
            email=email,
            orderid=order_id,
            transaction_id=transaction,
            time=time)
        root = ET.fromstring(str(what))
        form_params = dict((
            (node.attrib['name'], node.attrib['value']) for node in root
            if node.attrib['type'] == 'hidden'))
        self.assertIn('PBX_AUTOSEULE', form_params)
        self.assertEqual(form_params['PBX_AUTOSEULE'], 'N')

        transaction_id, kind, what = backend.request(
            Decimal(amount),
            email=email,
            orderid=order_id,
            transaction_id=transaction,
            time=time,
            manual_validation=True)
        root = ET.fromstring(str(what))
        form_params = dict((
            (node.attrib['name'], node.attrib['value']) for node in root
            if node.attrib['type'] == 'hidden'))
        self.assertIn('PBX_AUTOSEULE', form_params)
        self.assertEqual(form_params['PBX_AUTOSEULE'], 'O')
