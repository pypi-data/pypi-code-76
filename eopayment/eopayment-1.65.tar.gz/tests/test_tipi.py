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
from decimal import Decimal
from six.moves.urllib.parse import urlparse, parse_qs

import pytz

import eopayment
import eopayment.tipi
import pytest


def test_tipi():
    p = eopayment.Payment('tipi', {'numcli': '12345'})
    payment_id, kind, url = p.request(
        amount=Decimal('123.12'),
        exer='9999',
        refdet='999900000000999999',
        objet='tout a fait',
        email='info@entrouvert.com',
        urlcl='http://example.com/tipi/test',
        saisie='T')
    assert eopayment.tipi.Payment.REFDET_RE.match(payment_id) is not None
    parsed_qs = parse_qs(urlparse(url).query)
    assert parsed_qs['objet'][0].startswith('tout a fait')
    assert parsed_qs['montant'] == ['12312']
    assert parsed_qs['saisie'] == ['T']
    assert parsed_qs['mel'] == ['info@entrouvert.com']
    assert parsed_qs['numcli'] == ['12345']
    assert parsed_qs['exer'] == ['9999']
    assert parsed_qs['refdet'] == ['999900000000999999']

    response = p.response(
        'objet=tout+a+fait&montant=12312&saisie=T&mel=info%40entrouvert.com'
        '&numcli=12345&exer=9999&refdet=999900000000999999&resultrans=P')
    assert response.signed  # ...
    assert response.order_id == '999900000000999999'
    assert response.transaction_id == '999900000000999999'
    assert response.result == eopayment.PAID

    with pytest.raises(eopayment.ResponseError, match='missing refdet or resultrans'):
        p.response('foo=bar')


def test_tipi_no_orderid_no_refdet():
    p = eopayment.Payment('tipi', {'numcli': '12345'})
    payment_id, kind, url = p.request(
        amount=Decimal('123.12'),
        exer=9999,
        email='info@entrouvert.com',
        saisie='T')
    assert eopayment.tipi.Payment.REFDET_RE.match(payment_id) is not None
    parsed_qs = parse_qs(urlparse(url).query)
    assert 'objet' not in parsed_qs
    assert parsed_qs['montant'] == ['12312']
    assert parsed_qs['saisie'] == ['T']
    assert parsed_qs['mel'] == ['info@entrouvert.com']
    assert parsed_qs['numcli'] == ['12345']
    assert parsed_qs['exer'] == ['9999']
    assert parsed_qs['refdet'][0].startswith(datetime.datetime.now(pytz.timezone('Europe/Paris')).strftime('%Y%m%d'))


def test_tipi_orderid_refdef_compatible():
    p = eopayment.Payment('tipi', {'numcli': '12345', 'saisie': 'A'})
    payment_id, kind, url = p.request(
        amount=Decimal('123.12'),
        email='info@entrouvert.com',
        orderid='F121212')
    assert eopayment.tipi.Payment.REFDET_RE.match(payment_id)
    expected_url = urlparse(eopayment.tipi.TIPI_URL)
    parsed_url = urlparse(url)
    assert parsed_url[:3] == expected_url[:3]
    parsed_qs = parse_qs(parsed_url.query)
    assert 'objet' not in parsed_qs
    assert 'exer' not in parsed_qs
    assert parsed_qs['montant'] == ['12312']
    assert parsed_qs['saisie'] == ['A']
    assert parsed_qs['mel'] == ['info@entrouvert.com']
    assert parsed_qs['numcli'] == ['12345']
    assert parsed_qs['refdet'] == ['F121212']


def test_tipi_orderid_not_refdef_compatible():
    p = eopayment.Payment('tipi', {'numcli': '12345', 'saisie': 'A'})
    payment_id, kind, url = p.request(
        amount=Decimal('123.12'),
        email='info@entrouvert.com',
        objet='coucou',
        orderid='F12-12-12')
    assert eopayment.tipi.Payment.REFDET_RE.match(payment_id) is not None
    expected_url = urlparse(eopayment.tipi.TIPI_URL)
    parsed_url = urlparse(url)
    assert parsed_url[:3] == expected_url[:3]
    parsed_qs = parse_qs(parsed_url.query)
    assert 'exer' not in parsed_qs
    assert parsed_qs['montant'] == ['12312']
    assert parsed_qs['saisie'] == ['A']
    assert parsed_qs['mel'] == ['info@entrouvert.com']
    assert parsed_qs['numcli'] == ['12345']
    assert parsed_qs['refdet'][0].startswith(datetime.datetime.now().strftime('%Y%m%d'))
    assert 'coucou' in parsed_qs['objet'][0]
    assert 'F12-12-12' in parsed_qs['objet'][0]
