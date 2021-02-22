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

from datetime import date, datetime, timedelta

import mock
import pytest

import eopayment
from eopayment.common import PaymentCommon


def do_mock_backend(monkeypatch):
    class MockBackend(PaymentCommon):
        request = mock.Mock()

        description = {
            'parameters': [
                {
                    'name': 'capture_day',
                },
                {
                    'name': 'manual_validation',
                    'caption': 'Validation manuelle',
                    'type': bool,
                    'default': False,
                    'scope': 'transaction'
                },
                {
                    'name': 'global_param',
                    'caption': 'Global Param',
                    'type': bool,
                    'default': False,
                    'scope': 'global'
                },

            ]
        }

    def get_backend(*args, **kwargs):
        def backend(*args, **kwargs):
            return MockBackend
        return backend

    monkeypatch.setattr(eopayment, 'get_backend', get_backend)
    return MockBackend, eopayment.Payment('kind', None)


def test_deferred_payment(monkeypatch):
    mock_backend, payment = do_mock_backend(monkeypatch)

    capture_date = (datetime.now().date() + timedelta(days=3))
    payment.request(amount=12.2, capture_date=capture_date)
    mock_backend.request.assert_called_with(12.2, **{'capture_day': u'3'})

    # capture date can't be inferior to the transaction date
    capture_date = (datetime.now().date() - timedelta(days=3))
    with pytest.raises(
            ValueError, match='capture_date needs to be superior to the transaction date.'):
        payment.request(amount=12.2, capture_date=capture_date)

    # capture date should be a date object
    capture_date = 'not a date'
    with pytest.raises(ValueError, match='capture_date should be a datetime.date object.'):
        payment.request(amount=12.2, capture_date=capture_date)

    # using capture date on a backend that does not support it raise an error
    capture_date = (datetime.now().date() + timedelta(days=3))
    mock_backend.description['parameters'] = []
    with pytest.raises(ValueError, match='capture_date is not supported by the backend.'):
        payment.request(amount=12.2, capture_date=capture_date)


def test_paris_timezone(freezer, monkeypatch):
    freezer.move_to('2018-10-02 23:50:00')
    _, payment = do_mock_backend(monkeypatch)
    capture_date = date(year=2018, month=10, day=3)

    with pytest.raises(
            ValueError, match='capture_date needs to be superior to the transaction date'):
        # utcnow will return 2018-10-02 23:50:00,
        # converted to Europe/Paris it is already 2018-10-03
        # so 2018-10-03 for capture_date is invalid
        payment.request(amount=12.2, capture_date=capture_date)


def test_get_parameters(monkeypatch):
    _, payment = do_mock_backend(monkeypatch)

    global_parameters = payment.get_parameters()
    assert len(global_parameters) == 2
    assert global_parameters[0]['name'] == 'capture_day'
    assert global_parameters[1]['name'] == 'global_param'

    transaction_parameters = payment.get_parameters(scope='transaction')
    assert len(transaction_parameters) == 1
    assert transaction_parameters[0]['name'] == 'manual_validation'


def test_payment_status(monkeypatch):
    _, payment = do_mock_backend(monkeypatch)
    assert not payment.has_payment_status
