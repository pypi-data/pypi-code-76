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


import eopayment
import pytest


def test_build_request():
    backend = eopayment.Payment('sips2', {})
    transaction, f, form = backend.request(amount=u'12', last_name=u'Foo',
                                           first_name=u'Félix000000')
    data = [f for f in form.fields if f['name'] == 'Data']
    assert u'lix000000' not in data[0]['value']

    transaction, f, form = backend.request(amount=u'12')
    data = [f for f in form.fields if f['name'] == 'Data']
    assert 'statementReference=%s' % transaction in data[0]['value']

    transaction, f, form = backend.request(amount=u'12', info1='foobar')
    data = [f for f in form.fields if f['name'] == 'Data']
    assert 'statementReference=foobar' in data[0]['value']

    transaction, f, form = backend.request(amount=u'12', info1='foobar', capture_day=u'1')
    data = [f for f in form.fields if f['name'] == 'Data']
    assert 'captureDay=1' in data[0]['value']


def test_options():
    payment = eopayment.Payment('sips2', {'capture_mode': u'VALIDATION'})
    assert payment.backend.get_data()['captureMode'] == 'VALIDATION'

    payment = eopayment.Payment('sips2', {})
    assert 'captureDay' not in payment.backend.get_data()

    payment = eopayment.Payment('sips2', {'capture_day': '10'})
    assert 'captureDay' in payment.backend.get_data()


def test_parse_response():
    qs = '''Data=captureDay%3D0%7CcaptureMode%3DAUTHOR_CAPTURE%7CcurrencyCode%3D978%7CmerchantId%3D002001000000001%7CorderChannel%3DINTERNET%7CresponseCode%3D00%7CtransactionDateTime%3D2016-02-01T17%3A44%3A20%2B01%3A00%7CtransactionReference%3D668930%7CkeyVersion%3D1%7CacquirerResponseCode%3D00%7Camount%3D1200%7CauthorisationId%3D12345%7CcardCSCResultCode%3D4E%7CpanExpiryDate%3D201605%7CpaymentMeanBrand%3DMASTERCARD%7CpaymentMeanType%3DCARD%7CcustomerIpAddress%3D82.244.203.243%7CmaskedPan%3D5100%23%23%23%23%23%23%23%23%23%23%23%2300%7CorderId%3Dd4903de7027f4d56ac01634fd7ab9526%7CholderAuthentRelegation%3DN%7CholderAuthentStatus%3D3D_ERROR%7CtransactionOrigin%3DINTERNET%7CpaymentPattern%3DONE_SHOT&Seal=6ca3247765a19b45d25ad54ef4076483e7d55583166bd5ac9c64357aac097602&InterfaceVersion=HP_2.0&Encode='''  # noqa: E501
    backend = eopayment.Payment('sips2', {})
    response = backend.response(qs)
    assert response.signed
    assert response.transaction_date is None

    qs = '''Data=captureDay%3D0%7CcaptureMode%3DAUTHOR_CAPTURE%7CcurrencyCode%3D978%7CmerchantId%3D002001000000001%7CorderChannel%3DINTERNET%7CresponseCode%3D00%7CtransactionDateTime%3D2016-02-01T17%3A44%3A20%2B01%3A00%7CtransactionReference%3D668930%7CkeyVersion%3D1%7CacquirerResponseCode%3D00%7Camount%3D1200%7CauthorisationId%3D12345%7CcardCSCResultCode%3D4E%7CpanExpiryDate%3D201605%7CpaymentMeanBrand%3DMASTERCARD%7CpaymentMeanType%3DCARD%7CcustomerIpAddress%3D82.244.203.243%7CmaskedPan%3D5100%23%23%23%23%23%23%23%23%23%23%23%2300%7CorderId%3Dd4903de7027f4d56ac01634fd7ab9526%7CholderAuthentRelegation%3DN%7CholderAuthentStatus%3D3D_ERROR%7CtransactionOrigin%3DINTERNET%7CpaymentPattern%3DONE_SHOT%7CtransactionDateTime%3D2020-01-01%2001:01:01&Seal=6ca3247765a19b45d25ad54ef4076483e7d55583166bd5ac9c64357aac097602&InterfaceVersion=HP_2.0&Encode='''  # noqa: E501
    response = backend.response(qs)
    assert not response.signed
    assert response.transaction_date.isoformat() == '2020-01-01T01:01:01+01:00'

    with pytest.raises(eopayment.ResponseError, match='missing Data, Seal or InterfaceVersion'):
        backend.response('foo=bar')
