# coding: utf-8
#
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

from __future__ import print_function, unicode_literals

import json

import pytest

import zeep.transports

import eopayment


@pytest.fixture
def saga(record_http_session):
    if record_http_session:
        from eopayment import saga

        saga._zeep_transport = zeep.transports.Transport(session=record_http_session)
        try:
            yield None
        finally:
            saga._zeep_transport = None
    else:
        yield


@pytest.fixture
def backend_factory(saga, target_url):
    def factory(**kwargs):
        return eopayment.Payment('saga', dict({
            'base_url': target_url,
            'num_service': '868',
            'compte': '70688',
            'automatic_return_url': 'https://automatic.notif.url/automatic/',
            'normal_return_url': 'https://normal.notif.url/normal/',
        }, **kwargs))
    return factory


def test_error_parametrage(backend_factory):
    payment = backend_factory(num_service='1', compte='1')
    with pytest.raises(eopayment.PaymentException, match='Impossible de déterminer le paramétrage'):
        transaction_id, kind, url = payment.request(
            amount='10.00',
            email='john.doe@example.com',
            subject='Réservation concert XYZ numéro 1234')


def test_request(backend_factory):
    transaction_id, kind, url = backend_factory().request(
        amount='10.00',
        email='john.doe@example.com',
        subject='Réservation concert XYZ numéro 1234')
    assert transaction_id == '347b2060-1a37-11eb-af92-0213ad91a103'
    assert kind == eopayment.URL
    assert url == 'https://www.tipi.budget.gouv.fr/tpa/paiementws.web?idop=347b2060-1a37-11eb-af92-0213ad91a103'


def test_response(backend_factory):
    response = backend_factory().response('idop=28b52f40-1ace-11eb-8ce3-0213ad91a104', redirect=False)
    assert response.__dict__ == {
        'bank_data': {
            'email': 'john.doe@entrouvert.com',
            'etat': 'paye',
            'id_tiers': '-1',
            'montant': '10.00',
            'num_service': '868',
            'numcp': '70688',
            'numcpt_lib_ecriture': 'COUCOU'
        },
        'bank_status': 'paid',
        'order_id': '28b52f40-1ace-11eb-8ce3-0213ad91a104',
        'result': 3,
        'return_content': None,
        'signed': True,
        'test': False,
        'transaction_date': None,
        'transaction_id': '28b52f40-1ace-11eb-8ce3-0213ad91a104',
    }
    # Check bank_data is JSON serializable
    json.dumps(response.bank_data)

