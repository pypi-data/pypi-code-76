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


from datetime import datetime, timedelta

import pytest
from six.moves.urllib import parse as urlparse

import eopayment
from eopayment.systempayv2 import Payment, VADS_CUST_FIRST_NAME, \
    VADS_CUST_LAST_NAME, PAID
from eopayment import ResponseError

PARAMS = {
    'secret_test': u'1122334455667788',
    'vads_site_id': u'12345678',
    'vads_ctx_mode': u'TEST',
    'vads_trans_date': u'20090501193530',
    'signature_algo': 'sha1'
}


@pytest.fixture
def backend():
    return eopayment.Payment('systempayv2', PARAMS)


def get_field(form, field_name):
    for field in form.fields:
        if field['name'] == field_name:
            return field


def test_systempayv2(caplog):
    caplog.set_level(0)
    p = Payment(PARAMS)
    data = {
        'amount': 15.24,
        'orderid': '654321',
        'first_name': u'Jean Michél',
        'last_name': u'Mihaï'
    }
    qs = (
        'vads_version=V2&vads_page_action=PAYMENT&vads_action_mode=INTERACTIV'
        'E&vads_payment_config=SINGLE&vads_site_id=12345678&vads_ctx_mode=TES'
        'T&vads_trans_id=654321&vads_trans_date=20090501193530&vads_amount=15'
        '24&vads_currency=978&vads_cust_first_name=Jean+Mich%C3%A9l&vads_cust_last_name=Mihaï'
    )
    qs = urlparse.parse_qs(qs)
    for key in qs.keys():
        qs[key] = qs[key][0]
    assert p.signature(qs) == 'cf1ccac335590a33d6c243345c4f4531a0316b7f'
    transaction_id, f, form = p.request(**data)

    # check that user first and last names are unicode
    for field in form.fields:
        if field['name'] in (VADS_CUST_FIRST_NAME, VADS_CUST_LAST_NAME):
            assert field['value'] in (u'Jean Michél', u'Mihaï')

    response_qs = 'vads_amount=1042&vads_auth_mode=FULL&vads_auth_number=3feadf' \
                  '&vads_auth_result=00&vads_capture_delay=0&vads_card_brand=CB' \
                  '&vads_result=00' \
                  '&vads_card_number=497010XXXXXX0000' \
                  '&vads_payment_certificate=582ba2b725057618706d7a06e9e59acdbf69ff53' \
                  '&vads_ctx_mode=TEST&vads_currency=978&vads_effective_amount=1042' \
                  '&vads_site_id=70168983&vads_trans_date=20161013101355' \
                  '&vads_trans_id=226787&vads_trans_uuid=4b5053b3b1fe4b02a07753e7a' \
                  '&vads_effective_creation_date=20200330162530' \
                  '&signature=c17fab393f94dc027dc029510c85d5fc46c4710f'
    response = p.response(response_qs)
    assert response.result == PAID
    assert response.signed
    assert response.transaction_date
    assert response.transaction_date.isoformat() == '2020-03-30T16:25:30+00:00'

    PARAMS['signature_algo'] = 'hmac_sha256'
    p = Payment(PARAMS)
    assert p.signature(qs) == 'aHrJ7IzSGFa4pcYA8kh99+M/xBzoQ4Odnu3f4BUrpIA='
    response_qs = 'vads_amount=1042&vads_auth_mode=FULL&vads_auth_number=3feadf' \
                  '&vads_result=00' \
                  '&vads_auth_result=00&vads_capture_delay=0&vads_card_brand=CB' \
                  '&vads_card_number=497010XXXXXX0000' \
                  '&vads_payment_certificate=582ba2b725057618706d7a06e9e59acdbf69ff53' \
                  '&vads_ctx_mode=TEST&vads_currency=978&vads_effective_amount=1042' \
                  '&vads_site_id=70168983&vads_trans_date=20161013101355' \
                  '&vads_trans_id=226787&vads_trans_uuid=4b5053b3b1fe4b02a07753e7a' \
                  '&vads_effective_creation_date=20200330162530' \
                  '&signature=Wbz3bP6R6wDvAwb2HnSiH9%2FiUUoRVCxK7mdLtCMz8Xw%3D'
    response = p.response(response_qs)
    assert response.result == PAID
    assert response.signed

    # bad response
    with pytest.raises(ResponseError, match='missing signature, vads_ctx_mode or vads_auth_result'):
        p.response('foo=bar')


def test_systempayv2_deferred_payment():
    default_params = {
        'secret_test': u'1122334455667788',
        'vads_site_id': u'12345678',
        'vads_ctx_mode': u'TEST',
    }
    default_data = {
        'amount': 15.24, 'orderid': '654321', 'first_name': u'John',
        'last_name': u'Doe'
    }

    # default vads_capture_delay used
    params = default_params.copy()
    params['vads_capture_delay'] = 1

    backend = eopayment.Payment('systempayv2', params)
    data = default_data.copy()
    transaction_id, f, form = backend.request(**data)
    assert get_field(form, 'vads_capture_delay')['value'] == '1'

    # vads_capture_delay can used in request and
    # override default vads_capture_delay
    params = default_params.copy()
    params['vads_capture_delay'] = 1
    p = eopayment.Payment('systempayv2', params)
    data = default_data.copy()
    data['vads_capture_delay'] = '3'
    transaction_id, f, form = p.request(**data)
    assert get_field(form, 'vads_capture_delay')['value'] == '3'

    # capture_date can be used for deferred_payment
    params = default_params.copy()
    params['vads_capture_delay'] = 1
    p = eopayment.Payment('systempayv2', params)
    data = default_data.copy()
    data['capture_date'] = (datetime.now().date() + timedelta(days=4))
    transaction_id, f, form = p.request(**data)
    assert get_field(form, 'vads_capture_delay')['value'] == '4'


def test_manual_validation():
    params = {
        'secret_test': u'1122334455667788',
        'vads_site_id': u'12345678',
        'vads_ctx_mode': u'TEST',
    }
    data = {
        'amount': 15.24, 'orderid': '654321', 'first_name': u'John',
        'last_name': u'Doe'
    }

    backend = eopayment.Payment('systempayv2', params)
    transaction_id, f, form = backend.request(**data.copy())
    assert get_field(form, 'vads_validation_mode')['value'] == ''

    data['manual_validation'] = True
    transaction_id, f, form = backend.request(**data.copy())
    assert get_field(form, 'vads_validation_mode')['value'] == '1'

    data['manual_validation'] = False
    transaction_id, f, form = backend.request(**data.copy())
    assert get_field(form, 'vads_validation_mode')['value'] == ''

FIXED_TRANSACTION_ID = '1234'

def test_transaction_id_request(backend):
    transaction_id, kind, form = backend.request(10.0, transaction_id=FIXED_TRANSACTION_ID)
    assert transaction_id == FIXED_TRANSACTION_ID
    found = None
    for field in form.fields:
        if field['name'] == 'vads_ext_info_eopayment_trans_id':
            found = field
            break
    assert found
    assert found['value'] == FIXED_TRANSACTION_ID


def test_transaction_id_response(backend, caplog):
    caplog.set_level(0)
    response = '''vads_amount=1000&vads_auth_mode=FULL&vads_auth_number=3fcdd2&vads_auth_result=00&vads_capture_delay=0&vads_card_brand=CB&vads_card_number=597010XXXXXX0018&vads_payment_certificate=4db13859ab429cb6b9bae7546952846efd190e3a&vads_ctx_mode=TEST&vads_currency=978&vads_effective_amount=1000&vads_effective_currency=978&vads_site_id=51438584&vads_trans_date=20201027212030&vads_trans_id=sDJJeQ&vads_trans_uuid=368ef4d0822448e3a2e7413c4e9f8be8&vads_validation_mode=0&vads_version=V2&vads_warranty_result=&vads_payment_src=EC&vads_cust_country=FR&vads_contrib=eopayment&vads_tid=001&vads_sequence_number=1&vads_contract_used=2334410&vads_trans_status=AUTHORISED&vads_expiry_month=6&vads_expiry_year=2021&vads_bank_label=Banque+de+d%C3%A9mo+et+de+l%27innovation&vads_bank_product=MCW&vads_pays_ip=FR&vads_presentation_date=20201027212031&vads_effective_creation_date=20201027212031&vads_operation_type=DEBIT&vads_result=00&vads_extra_result=&vads_card_country=FR&vads_language=fr&vads_brand_management=%7B%22userChoice%22%3Afalse%2C%22brandList%22%3A%22CB%7CMASTERCARD%22%2C%22brand%22%3A%22CB%22%7D&vads_action_mode=INTERACTIVE&vads_payment_config=SINGLE&vads_page_action=PAYMENT&vads_ext_info_eopayment_trans_id=1234&vads_threeds_enrolled=Y&vads_threeds_auth_type=CHALLENGE&vads_threeds_eci=02&vads_threeds_xid=bVpsTUhLSWpodnJjdXJVdE5rb0g%3D&vads_threeds_cavvAlgorithm=2&vads_threeds_status=Y&vads_threeds_sign_valid=1&vads_threeds_error_code=&vads_threeds_exit_status=10&vads_threeds_cavv=jG26AYSjvclBARFYSf%2FtXRmjGXM%3D&signature=fBGbFQPlUiyrL0yVgQzbhokMt6cqG24hOr%2BYsXKr/b8='''
    result = backend.response(response)
    assert result.signed
    assert result.transaction_id == FIXED_TRANSACTION_ID
