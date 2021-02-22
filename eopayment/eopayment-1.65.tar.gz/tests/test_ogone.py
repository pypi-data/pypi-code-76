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

from unittest import TestCase
from xml.etree import ElementTree as ET

import six
from six.moves.urllib import parse as urllib

import eopayment
import eopayment.ogone as ogone
from eopayment import ResponseError

PSPID = u'2352566ö'

BACKEND_PARAMS = {
    'environment': ogone.ENVIRONMENT_TEST,
    'pspid': PSPID,
    'sha_in': u'sécret',
    'sha_out': u'sécret',
    'automatic_return_url': u'http://example.com/autömatic_réturn_url'
}


class OgoneTests(TestCase):
    if six.PY2:
        def assertRaisesRegex(self, *args, **kwargs):
            return self.assertRaisesRegexp(*args, **kwargs)

    def test_request(self):
        ogone_backend = eopayment.Payment('ogone', BACKEND_PARAMS)
        amount = '42.42'
        order_id = u'my ordér'
        reference, kind, what = ogone_backend.request(
            amount=amount,
            orderid=order_id,
            email='foo@example.com')
        self.assertEqual(len(reference), 30)
        assert reference.startswith(order_id)
        root = ET.fromstring(str(what))
        self.assertEqual(root.tag, 'form')
        self.assertEqual(root.attrib['method'], 'POST')
        self.assertEqual(root.attrib['action'], ogone.ENVIRONMENT_TEST_URL)
        values = {
            'CURRENCY': u'EUR',
            'ORDERID': reference,
            'PSPID': PSPID,
            'EMAIL': 'foo@example.com',
            'AMOUNT': amount.replace('.', ''),
            'LANGUAGE': 'fr_FR',
        }
        values.update({'SHASIGN': ogone_backend.backend.sha_sign_in(values)})
        for node in root:
            self.assertIn(node.attrib['type'], ('hidden', 'submit'))
            self.assertEqual(set(node.attrib.keys()), set(['type', 'name', 'value']))
            name = node.attrib['name']
            if node.attrib['type'] == 'hidden':
                self.assertIn(name, values)
                self.assertEqual(node.attrib['value'], values[name])

    def test_unicode_response(self):
        ogone_backend = eopayment.Payment('ogone', BACKEND_PARAMS)
        order_id = 'myorder'
        data = {'orderid': u'myorder', 'status': u'9', 'payid': u'3011229363',
                'cn': u'Usér', 'ncerror': u'0',
                'trxdate': u'10/24/16', 'acceptance': u'test123',
                'currency': u'eur', 'amount': u'7.5',
                'shasign': u'CA4B3C2767B5EFAB33B9122A5D4CF6F27747303D'}
        # uniformize to utf-8 first
        for k in data:
            data[k] = eopayment.common.force_byte(data[k])
        response = ogone_backend.response(urllib.urlencode(data))
        assert response.signed
        self.assertEqual(response.order_id, order_id)

    def test_iso_8859_1_response(self):
        ogone_backend = eopayment.Payment('ogone', BACKEND_PARAMS)
        order_id = 'lRXK4Rl1N2yIR3R5z7Kc'
        backend_response = (
            'orderID=lRXK4Rl1N2yIR3R5z7Kc&currency=EUR&amount=7%2E5'
            '&PM=CreditCard&ACCEPTANCE=test123&STATUS=9'
            '&CARDNO=XXXXXXXXXXXX9999&ED=0118'
            '&CN=Miha%EF+Serghe%EF&TRXDATE=10%2F24%2F16'
            '&PAYID=3011228911&NCERROR=0&BRAND=MasterCard'
            '&IP=80%2E12%2E92%2E47&SHASIGN=C429BE892FACFBFCE5E2CC809B102D866DD3D48C'
        )
        response = ogone_backend.response(backend_response)
        assert response.signed
        self.assertEqual(response.order_id, order_id)

    def test_bad_response(self):
        ogone_backend = eopayment.Payment('ogone', BACKEND_PARAMS)
        data = {'payid': '32100123', 'status': 9, 'ncerror': 0}
        with self.assertRaisesRegex(ResponseError, 'missing ORDERID, PAYID, STATUS or NCERROR'):
            ogone_backend.response(urllib.urlencode(data))

    def test_bank_transfer_response(self):
        ogone_backend = eopayment.Payment('ogone', BACKEND_PARAMS)
        data = {
            'orderid': u'myorder',
            'status': u'41',
            'payid': u'3011229363',
            'cn': u'User',
            'ncerror': u'0',
            'trxdate': u'10/24/16',
            'brand': 'Bank transfer',
            'pm': 'bank transfer',
            'currency': u'eur',
            'amount': u'7.5',
            'shasign': u'944CBD1E010BA4945415AE4B16CC40FD533F6CE2',
        }
        # uniformize to utf-8 first
        for k in data:
            data[k] = eopayment.common.force_byte(data[k])
        response = ogone_backend.response(urllib.urlencode(data))
        assert response.signed
        assert response.result == eopayment.WAITING

        # check utf-8 based signature is also ok
        data['shasign'] = b'0E35F687ACBEAA6CA769E0ADDBD0863EB6C1678A'
        response = ogone_backend.response(urllib.urlencode(data))
        assert response.signed
        assert response.result == eopayment.WAITING

        # check invalid signature is not marked ok
        data['shasign'] = b'0000000000000000000000000000000000000000'
        response = ogone_backend.response(urllib.urlencode(data))
        assert not response.signed
