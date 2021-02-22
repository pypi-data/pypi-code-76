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

from six.moves.urllib.parse import urlparse, parse_qs
import datetime

import eopayment
import pytest


@pytest.fixture
def backend():
    options = {
        'automatic_notification_url': 'http://example.com/direct_notification_url',
        'origin': 'Mairie de Perpette-les-oies'
    }
    return eopayment.Payment('dummy', options)


def test_request(backend, freezer):
    freezer.move_to('2020-01-01 00:00:00+01:00')
    transaction_id, method, raw_url = backend.request(
        '10.10', capture_date=datetime.date(2020, 1, 7), subject='Repas pour 4 personnes')
    assert transaction_id
    assert method == 1
    url = urlparse(raw_url)
    assert url.scheme == 'http'
    assert url.netloc == 'dummy-payment.demo.entrouvert.com'
    assert url.path == '/'
    assert url.fragment == ''
    qs = {k: v[0] for k, v in parse_qs(url.query).items()}
    assert qs['transaction_id'] == transaction_id
    assert qs['amount'] == '10.10'
    assert qs['origin'] == 'Mairie de Perpette-les-oies'
    assert qs['capture_day'] == '6'
    assert qs['subject'] == 'Repas pour 4 personnes'


def test_response(backend):
    retour = (
        'http://example.com/retour?amount=10.0'
        '&direct_notification_url=http%3A%2F%2Fexample.com%2Fdirect_notification_url'
        '&email=toto%40example.com'
        '&transaction_id=6Tfw2e1bPyYnz7CedZqvdHt7T9XX6T'
        '&return_url=http%3A%2F%2Fexample.com%2Fretour'
        '&nok=1'
    )
    r = backend.response(retour.split('?', 1)[1])
    assert not r.signed
    assert r.transaction_id == '6Tfw2e1bPyYnz7CedZqvdHt7T9XX6T'
    assert r.return_content is None
    retour = (
        'http://example.com/retour'
        '?amount=10.0'
        '&direct_notification_url=http%3A%2F%2Fexample.com%2Fdirect_notification_url'
        '&email=toto%40example.com'
        '&transaction_id=6Tfw2e1bPyYnz7CedZqvdHt7T9XX6T'
        '&return_url=http%3A%2F%2Fexample.com%2Fretour'
        '&ok=1&signed=1'
    )
    r = backend.response(retour.split('?', 1)[1])
    assert r.signed
    assert r.transaction_id == '6Tfw2e1bPyYnz7CedZqvdHt7T9XX6T'
    assert r.return_content == 'signature ok'

    with pytest.raises(eopayment.ResponseError, match='missing transaction_id'):
        backend.response('foo=bar')
