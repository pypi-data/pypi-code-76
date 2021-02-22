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

import json

import requests
import six

import eopayment
import pytest
from eopayment.mollie import Payment
from httmock import remember_called, response, urlmatch, with_httmock

pytestmark = pytest.mark.skipif(six.PY2, reason='this payment module only supports python3')

WEBHOOK_URL = 'https://callback.example.com'
RETURN_URL = 'https://return.example.com'
API_KEY = 'test'

PAYMENT_ID = "tr_7UhSN1zuXS"
QUERY_STRING = 'id=' + PAYMENT_ID


POST_PAYMENTS_RESPONSE = {
    "resource": "payment",
    "id": PAYMENT_ID,
    "mode": "test",
    "createdAt": "2018-03-20T09:13:37+00:00",
    "amount": {
        "value": "3.50",
        "currency": "EUR"
    },
    "description": "Payment #12345",
    "method": "null",
    "status": "open",
    "isCancelable": True,
    "expiresAt": "2018-03-20T09:28:37+00:00",
    "sequenceType": "oneoff",
    "redirectUrl": "https://webshop.example.org/payment/12345/",
    "webhookUrl": "https://webshop.example.org/payments/webhook/",
    "_links": {
        "checkout": {
            "href": "https://www.mollie.com/payscreen/select-method/7UhSN1zuXS",
            "type": "text/html"
        },
    }
}


GET_PAYMENTS_RESPONSE = {
    "amount": {
        "currency": "EUR",
        "value": "3.50"
    },
    "amountRefunded": {
        "currency": "EUR",
        "value": "0.00"
    },
    "amountRemaining": {
        "currency": "EUR",
        "value": "3.50"
    },
    "countryCode": "FR",
    "createdAt": "2020-05-06T13:04:26+00:00",
    "description": "Publik",
    "details": {
        "cardAudience": "consumer",
        "cardCountryCode": "NL",
        "cardHolder": "T. TEST",
        "cardLabel": "Mastercard",
        "cardNumber": "6787",
        "cardSecurity": "normal",
        "feeRegion": "other"
    },
    "id": PAYMENT_ID,
    "metadata": {
        "email": "test@entrouvert.com",
        "first_name": "test",
        "last_name": "test"
    },
    "isCancelable": True,
    "method": "creditcard",
    "mode": "test",
    "paidAt": "2020-05-06T14:01:04+00:00",
    "profileId": "pfl_WNPCPTGepu",
    "redirectUrl": "https://localhost/lingo/return-payment-backend/3/MTAw.1jWJis.6TbbjwSEurag6v4Z2VCheISBFjw/",
    "resource": "payment",
    "sequenceType": "oneoff",
    "settlementAmount": {
        "currency": "EUR",
        "value": "3.50"
    },
    "status": "paid",
    "webhookUrl": "https://localhost/lingo/callback-payment-backend/3/"
}


@remember_called
@urlmatch(scheme='https', netloc='api.mollie.com', path='/v2/payments', method='POST')
def add_payment(url, request):
    return response(200, POST_PAYMENTS_RESPONSE, request=request)


@remember_called
@urlmatch(scheme='https', netloc='api.mollie.com', path='/v2/payments', method='GET')
def successful_payment(url, request):
    return response(200, GET_PAYMENTS_RESPONSE, request=request)


@remember_called
@urlmatch(scheme='https', netloc='api.mollie.com', path=r'/v2/payments', method='DELETE')
def canceled_payment(url, request):
    resp = GET_PAYMENTS_RESPONSE.copy()
    resp['status'] = 'canceled'
    return response(200, resp, request=request)


@remember_called
@urlmatch(scheme='https', netloc='api.mollie.com', path='/v2/payments')
def failed_payment(url, request):
    resp = GET_PAYMENTS_RESPONSE.copy()
    resp['status'] = 'failed'
    return response(200, resp, request=request)


@remember_called
@urlmatch(scheme='https', netloc='api.mollie.com', path='/v2/payments')
def expired_payment(url, request):
    resp = GET_PAYMENTS_RESPONSE.copy()
    resp['status'] = 'expired'
    return response(200, resp, request=request)


@remember_called
@urlmatch(scheme='https', netloc='api.mollie.com', path=r'/v2/payments', method='GET')
def canceled_payment_get(url, request):
    resp = GET_PAYMENTS_RESPONSE.copy()
    resp['status'] = 'canceled'
    return response(200, resp, request=request)


@remember_called
@urlmatch(scheme='https', netloc='api.mollie.com', path='/v2/payments', method='GET')
def connection_error(url, request):
    raise requests.ConnectionError('test msg')


@remember_called
@urlmatch(scheme='https', netloc='api.mollie.com', path='/v2/payments', method='GET')
def http_error(url, request):
    error_payload = {
        'status': 404,
        'title': 'Not Found',
        'detail': 'No payment exists with token hop.',
    }
    return response(400, error_payload, request=request)


@remember_called
@urlmatch(scheme='https', netloc='api.mollie.com', path='/v2/payments', method='GET')
def invalid_json(url, request):
    return response(200, '{', request=request)


@pytest.fixture
def mollie():
    return Payment({
        'normal_return_url': RETURN_URL,
        'automatic_return_url': WEBHOOK_URL,
        'api_key': API_KEY,
    })


@with_httmock(add_payment)
def test_mollie_request(mollie):
    email = 'test@test.com'
    payment_id, kind, url = mollie.request(2.5, email=email)

    assert payment_id == PAYMENT_ID
    assert kind == eopayment.URL
    assert 'mollie.com/payscreen/' in url

    body = json.loads(add_payment.call['requests'][0].body.decode())
    assert body['amount']['value'] == '2.5'
    assert body['amount']['currency'] == 'EUR'
    assert body['metadata']['email'] == email
    assert body['webhookUrl'] == WEBHOOK_URL
    assert body['redirectUrl'] == RETURN_URL


@with_httmock(successful_payment)
def test_mollie_response(mollie):
    payment_response = mollie.response(QUERY_STRING)

    assert payment_response.result == eopayment.PAID
    assert payment_response.signed is True
    assert payment_response.bank_data == GET_PAYMENTS_RESPONSE
    assert payment_response.order_id == PAYMENT_ID
    assert payment_response.transaction_id == PAYMENT_ID
    assert payment_response.bank_status == 'paid'
    assert payment_response.test is True

    request = successful_payment.call['requests'][0]
    assert PAYMENT_ID in request.url


@with_httmock(successful_payment)
def test_mollie_response_on_redirect(mollie):
    payment_response = mollie.response(query_string=None, redirect=True, order_id_hint=PAYMENT_ID,
                                       order_status_hint=0)
    assert payment_response.result == eopayment.PAID

    request = successful_payment.call['requests'][0]
    assert PAYMENT_ID in request.url


def test_mollie_response_on_redirect_final_status(mollie):
    payment_response = mollie.response(query_string=None, redirect=True, order_id_hint=PAYMENT_ID,
                                       order_status_hint=eopayment.PAID)
    assert payment_response.result == eopayment.PAID
    assert payment_response.order_id == PAYMENT_ID


@with_httmock(failed_payment)
def test_mollie_response_failed(mollie):
    payment_response = mollie.response(QUERY_STRING)
    assert payment_response.result == eopayment.ERROR


@with_httmock(canceled_payment_get)
def test_mollie_response_canceled(mollie):
    payment_response = mollie.response(QUERY_STRING)
    assert payment_response.result == eopayment.CANCELED


@with_httmock(expired_payment)
def test_mollie_response_expired(mollie):
    payment_response = mollie.response(QUERY_STRING)
    assert payment_response.result == eopayment.CANCELED


@with_httmock(connection_error)
def test_mollie_endpoint_connection_error(mollie):
    with pytest.raises(eopayment.PaymentException) as excinfo:
        mollie.call_endpoint('GET', 'payments')
        assert 'test msg' in str(excinfo.value)


@with_httmock(http_error)
def test_mollie_endpoint_http_error(mollie):
    with pytest.raises(eopayment.PaymentException) as excinfo:
        mollie.call_endpoint('GET', 'payments')
        assert 'Not Found' in str(excinfo.value)
        assert 'token' in str(excinfo.value)


@with_httmock(invalid_json)
def test_mollie_endpoint_json_error(mollie):
    with pytest.raises(eopayment.PaymentException) as excinfo:
        mollie.call_endpoint('GET', 'payments')
        assert 'JSON' in str(excinfo.value)
