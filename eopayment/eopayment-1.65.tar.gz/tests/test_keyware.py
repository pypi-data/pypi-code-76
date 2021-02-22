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

import pytest
import requests
import six
from httmock import response, urlmatch, HTTMock, with_httmock, all_requests, remember_called

import eopayment
from eopayment.keyware import Payment

pytestmark = pytest.mark.skipif(six.PY2, reason='this payment module only supports python3')

WEBHOOK_URL = 'https://callback.example.com'
RETURN_URL = 'https://return.example.com'
API_KEY = 'test'

ORDER_ID = "1c969951-f5f1-4290-ae41-6177961fb3cb"
QUERY_STRING = 'order_id=' + ORDER_ID


POST_ORDER_RESPONSE = {
    "amount": 995,
    "client": {
        "user_agent": "Testing API"
    },
    "created": "2016-07-04T11:41:57.121017+00:00",
    "currency": "EUR",
    "description": "Example description",
    "id": ORDER_ID,
    "merchant_id": "7131b462-1b7d-489f-aba9-de2f0eadc9dc",
    "modified": "2016-07-04T11:41:57.183822+00:00",
    "order_url": "https://api.online.emspay.eu/pay/1c969951-f5f1-4290-ae41-6177961fb3cb/",
    "project_id": "1ef558ed-d77d-470d-b43b-c0f4a131bcef",
    "status": "new"
}

GET_ORDER_RESPONSE = {
    "amount": 995,
    "client": {
        "user_agent": "Testing API"
    },
    "created": "2016-07-04T11:41:55.635115+00:00",
    "currency": "EUR",
    "description": "Example order #1",
    "id": ORDER_ID,
    "last_transaction_added": "2016-07-04T11:41:55.831655+00:00",
    "merchant_id": "7131b462-1b7d-489f-aba9-de2f0eadc9dc",
    "merchant_order_id": "EXAMPLE001",
    "modified": "2016-07-04T11:41:56.215543+00:00",
    "project_id": "1ef558ed-d77d-470d-b43b-c0f4a131bcef",
    "return_url": "http://www.example.com/",
    "status": "completed",
    "transactions": [
        {
            "amount": 995,
            "balance": "internal",
            "created": "2016-07-04T11:41:55.831655+00:00",
            "credit_debit": "credit",
            "currency": "EUR",
            "description": "Example order #1",
            "events": [
                {
                    "event": "new",
                    "id": "0c4bd0cd-f197-446b-b218-39cbeb028290",
                    "noticed": "2016-07-04T11:41:55.987468+00:00",
                    "occurred": "2016-07-04T11:41:55.831655+00:00",
                    "source": "set_status"
                }
            ],
            "expiration_period": "PT60M",
            "id": "6c81499c-14e4-4974-99e5-fe72ce019411",
            "merchant_id": "7131b462-1b7d-489f-aba9-de2f0eadc9dc",
            "modified": "2016-07-04T11:41:56.065147+00:00",
            "order_id": ORDER_ID,
            "payment_method": "ideal",
            "payment_method_details": {
                "issuer_id": "INGBNL2A",
            },
            "payment_url": "https://api.online.emspay.eu/redirect/6c81499c-14e4-4974-99e5-fe72ce019411/to/payment/",
            "project_id": "1ef558ed-d77d-470d-b43b-c0f4a131bcef",
            "status": "completed"
        }
    ]
}


@remember_called
@urlmatch(scheme='https', netloc='api.online.emspay.eu', path='/v1/orders', method='POST')
def add_order(url, request):
    return response(200, POST_ORDER_RESPONSE, request=request)

@remember_called
@urlmatch(scheme='https', netloc='api.online.emspay.eu', path='/v1/orders', method='GET')
def successful_order(url, request):
    return response(200, GET_ORDER_RESPONSE, request=request)

@remember_called
@urlmatch(scheme='https', netloc='api.online.emspay.eu', path=r'/v1/orders', method='DELETE')
def cancelled_order(url, request):
    resp = GET_ORDER_RESPONSE.copy()
    resp['status'] = 'cancelled'
    return response(200, resp, request=request)

@remember_called
@urlmatch(scheme='https', netloc='api.online.emspay.eu', path='/v1/orders')
def error_order(url, request):
    resp = GET_ORDER_RESPONSE.copy()
    resp['status'] = 'error'
    return response(200, resp, request=request)

@remember_called
@urlmatch(scheme='https', netloc='api.online.emspay.eu', path='/v1/orders', method='GET')
def connection_error(url, request):
    raise requests.ConnectionError('test msg')

@remember_called
@urlmatch(scheme='https', netloc='api.online.emspay.eu', path='/v1/orders', method='GET')
def http_error(url, request):
    error_payload = {'error': {'status': 400, 'type': 'Bad request', 'value': 'error'}}
    return response(400, error_payload, request=request)

@remember_called
@urlmatch(scheme='https', netloc='api.online.emspay.eu', path='/v1/orders', method='GET')
def invalid_json(url, request):
    return response(200, '{', request=request)

@pytest.fixture
def keyware():
    return Payment({
        'normal_return_url': RETURN_URL,
        'automatic_return_url': WEBHOOK_URL,
        'api_key': API_KEY,
    })


@with_httmock(add_order)
def test_keyware_request(keyware):
    email = 'test@test.com'
    order_id, kind, url = keyware.request(2.5, email=email)

    assert order_id == ORDER_ID
    assert kind == eopayment.URL
    assert 'api.online.emspay.eu/pay/' in url

    body = json.loads(add_order.call['requests'][0].body.decode())
    assert body['currency'] == 'EUR'
    assert body['customer']['email_address'] == email
    assert isinstance(body['amount'], int)
    assert body['amount'] == 250
    assert body['webhook_url'] == WEBHOOK_URL
    assert body['return_url'] == RETURN_URL


@with_httmock(successful_order)
def test_keyware_response(keyware):
    payment_response = keyware.response(QUERY_STRING)

    assert payment_response.result == eopayment.PAID
    assert payment_response.signed is True
    assert payment_response.bank_data == GET_ORDER_RESPONSE
    assert payment_response.order_id == ORDER_ID
    assert payment_response.transaction_id == ORDER_ID
    assert payment_response.bank_status == 'completed'
    assert payment_response.test is False

    request = successful_order.call['requests'][0]
    assert ORDER_ID in request.url


@with_httmock(error_order)
def test_keyware_response_error(keyware):
    payment_response = keyware.response(QUERY_STRING)
    assert payment_response.result == eopayment.ERROR


@with_httmock(cancelled_order)
def test_keyware_cancel(keyware):
    resp = keyware.cancel(amount=995, bank_data=POST_ORDER_RESPONSE)
    request = cancelled_order.call['requests'][0]
    assert ORDER_ID in request.url


@with_httmock(error_order)
def test_keyware_cancel_error(keyware):
    with pytest.raises(eopayment.ResponseError) as excinfo:
        keyware.cancel(amount=995, bank_data=POST_ORDER_RESPONSE)
        assert 'expected "cancelled" status, got "error" instead' in str(excinfo.value)


@with_httmock(connection_error)
def test_keyware_endpoint_connection_error(keyware):
    with pytest.raises(eopayment.PaymentException) as excinfo:
        keyware.call_endpoint('GET', 'orders')
        assert 'test msg' in str(excinfo.value)


@with_httmock(http_error)
def test_keyware_endpoint_http_error(keyware):
    with pytest.raises(eopayment.PaymentException) as excinfo:
        keyware.call_endpoint('GET', 'orders')
        assert 'Bad request' in str(excinfo.value)


@with_httmock(invalid_json)
def test_keyware_endpoint_json_error(keyware):
    with pytest.raises(eopayment.PaymentException) as excinfo:
        keyware.call_endpoint('GET', 'orders')
        assert 'JSON' in str(excinfo.value)
