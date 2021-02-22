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

import datetime
import json
import lxml.etree as ET
import mock

import pytz

import httmock
import pytest

from zeep.plugins import HistoryPlugin

import eopayment
from eopayment.payfip_ws import PayFiP, PayFiPError, normalize_objet


NUMCLI = '090909'
NOTIF_URL = 'https://notif.payfip.example.com/'
REDIRECT_URL = 'https://redirect.payfip.example.com/'
MEL = 'john.doe@example.com'
EXER = '2019'
REFDET = '201912261758460053903194'
REFDET_GEN = '201912261758460053903195'


def xmlindent(content):
    if hasattr(content, 'encode') or hasattr(content, 'decode'):
        content = ET.fromstring(content)
    return ET.tostring(content, pretty_print=True).decode('utf-8', 'ignore')


# freeze time to fix EXER field to 2019
@pytest.fixture(autouse=True)
def freezer(freezer):
    freezer.move_to('2019-12-12')
    return freezer


class PayFiPHTTMock(object):
    def __init__(self, history_name):
        history_path = 'tests/data/payfip-%s.json' % history_name
        with open(history_path) as fd:
            self.history = json.load(fd)
        self.counter = 0

    @httmock.urlmatch(scheme='https')
    def mock(self, url, request):
        request_content, response_content = self.history[self.counter]
        self.counter += 1
        assert xmlindent(request.body) == request_content
        return response_content


@pytest.fixture
def history_name(request):
    return getattr(request.function, 'history_name', request.function.__name__)


@pytest.fixture
def history(history_name, request):
    if 'update_data' not in request.keywords:
        history_mock = PayFiPHTTMock(history_name)
        with httmock.HTTMock(history_mock.mock):
            yield history_mock
    else:
        yield None


@pytest.fixture
def get_idop():
    with mock.patch('eopayment.payfip_ws.PayFiP.get_idop') as get_idop:
        get_idop.return_value = 'idop-1234'
        yield get_idop


@pytest.fixture
def backend(request):
    with mock.patch('eopayment.payfip_ws.Payment._generate_refdet') as _generate_refdet:
        _generate_refdet.return_value = REFDET_GEN
        yield eopayment.Payment('payfip_ws', {
            'numcli': '090909',
            'automatic_return_url': NOTIF_URL,
            'normal_return_url': REDIRECT_URL,
        })


@pytest.fixture
def payfip(history, history_name, request):
    history = HistoryPlugin()

    @httmock.urlmatch()
    def raise_on_request(url, request):
        # ensure we do not access network
        from requests.exceptions import RequestException
        raise RequestException('huhu')

    with httmock.HTTMock(raise_on_request):
        payfip = PayFiP(wsdl_url='./eopayment/resource/PaiementSecuriseService.wsdl',
                        zeep_client_kwargs={'plugins': [history]})
    yield payfip

    # add @pytest.mark.update_data to test to update fixtures data
    if 'update_data' in request.keywords:
        history_path = 'tests/data/payfip-%s.json' % history_name
        d = [
            (xmlindent(exchange['sent']['envelope']),
             xmlindent(exchange['received']['envelope']))
            for exchange in history._buffer
        ]
        content = json.dumps(d)
        with open(history_path, 'wb') as fd:
            fd.write(content)


def set_history_name(name):
    # decorator to add history_name to test
    def decorator(func):
        func.history_name = name
        return func
    return decorator

# pytestmark = pytest.mark.update_data


def test_get_client_info(payfip):
    result = payfip.get_info_client(NUMCLI)
    assert result.numcli == NUMCLI
    assert result.libelleN2 == 'POUETPOUET'


def test_get_idop_ok(payfip):
    result = payfip.get_idop(
        numcli=NUMCLI,
        exer='2019',
        refdet='ABCDEFGH',
        montant='1000',
        mel=MEL,
        objet='coucou',
        url_notification=NOTIF_URL,
        url_redirect=REDIRECT_URL,
        saisie='T')
    assert result == 'cc0cb210-1cd4-11ea-8cca-0213ad91a103'


def test_get_idop_refdet_error(payfip):
    with pytest.raises(PayFiPError, match='.*R3.*Le format.*REFDET.*conforme'):
        payfip.get_idop(
            numcli=NUMCLI,
            exer='2019',
            refdet='ABCD',
            montant='1000',
            mel=MEL,
            objet='coucou',
            url_notification='https://notif.payfip.example.com/',
            url_redirect='https://redirect.payfip.example.com/',
            saisie='T')


def test_get_idop_adresse_mel_incorrect(payfip):
    with pytest.raises(PayFiPError, match='.*A2.*Adresse.*incorrecte'):
        payfip.get_idop(
            numcli=NUMCLI,
            exer='2019',
            refdet='ABCDEF',
            montant='9990000001',
            mel='john.doeexample.com',
            objet='coucou',
            url_notification='https://notif.payfip.example.com/',
            url_redirect='https://redirect.payfip.example.com/',
            saisie='T')


def test_get_info_paiement_ok(payfip):
    result = payfip.get_info_paiement('cc0cb210-1cd4-11ea-8cca-0213ad91a103')
    assert {k: result[k] for k in result} == {
        'dattrans': '12122019',
        'exer': '20',
        'heurtrans': '1311',
        'idOp': 'cc0cb210-1cd4-11ea-8cca-0213ad91a103',
        'mel': MEL,
        'montant': '1000',
        'numauto': '112233445566-tip',
        'numcli': NUMCLI,
        'objet': 'coucou',
        'refdet': 'EFEFAEFG',
        'resultrans': 'V',
        'saisie': 'T'
    }


def test_get_info_paiement_P1(payfip, freezer):
    # idop par pas encore reçu par la plate-forme ou déjà nettoyé (la nuit)
    with pytest.raises(PayFiPError, match='.*P1.*IdOp incorrect.*'):
        payfip.get_info_paiement('cc0cb210-1cd4-11ea-8cca-0213ad91a103')


@set_history_name('test_get_info_paiement_P1')
def test_P1_and_payment_status(history, backend):
    assert backend.has_payment_status
    response = backend.payment_status(transaction_id='cc0cb210-1cd4-11ea-8cca-0213ad91a103')
    assert response.result == eopayment.EXPIRED


@set_history_name('test_get_info_paiement_P1')
def test_P1_and_payment_status_utc_aware_now(history, backend):
    utc_now = datetime.datetime.now(pytz.utc)
    response = backend.payment_status(transaction_id='cc0cb210-1cd4-11ea-8cca-0213ad91a103', transaction_date=utc_now)
    assert response.result == eopayment.EXPIRED


@set_history_name('test_get_info_paiement_P1')
def test_P1_and_payment_status_utc_naive_now(history, backend):
    now = datetime.datetime.now()
    response = backend.payment_status(transaction_id='cc0cb210-1cd4-11ea-8cca-0213ad91a103', transaction_date=now)
    assert response.result == eopayment.EXPIRED


@set_history_name('test_get_info_paiement_P1')
def test_P1_and_payment_status_utc_aware_now_later(history, backend, freezer):
    utc_now = datetime.datetime.now(pytz.utc)
    freezer.move_to(datetime.timedelta(minutes=25))
    response = backend.payment_status(transaction_id='cc0cb210-1cd4-11ea-8cca-0213ad91a103', transaction_date=utc_now)
    assert response.result == eopayment.EXPIRED


@set_history_name('test_get_info_paiement_P1')
def test_P1_and_payment_status_utc_naive_now_later(payfip, backend, freezer):
    now = datetime.datetime.now()
    freezer.move_to(datetime.timedelta(minutes=25))
    response = backend.payment_status(transaction_id='cc0cb210-1cd4-11ea-8cca-0213ad91a103', transaction_date=now)
    assert response.result == eopayment.EXPIRED


def test_get_info_paiement_P5(payfip):
    # idop reçu par la plate-forme mais transaction en cours
    with pytest.raises(PayFiPError, match='.*P5.*sultat de la transaction non connu.*'):
        payfip.get_info_paiement('cc0cb210-1cd4-11ea-8cca-0213ad91a103')


@set_history_name('test_get_info_paiement_P5')
def test_P5_and_payment_status(payfip, backend, freezer):
    response = backend.payment_status(transaction_id='cc0cb210-1cd4-11ea-8cca-0213ad91a103')
    assert response.result == eopayment.WAITING


@set_history_name('test_get_info_paiement_P5')
def test_P5_and_payment_status_utc_aware_now(payfip, backend, freezer):
    utc_now = datetime.datetime.now(pytz.utc)
    response = backend.payment_status(transaction_id='cc0cb210-1cd4-11ea-8cca-0213ad91a103', transaction_date=utc_now)
    assert response.result == eopayment.WAITING


@set_history_name('test_get_info_paiement_P5')
def test_P5_and_payment_status_utc_naive_now(payfip, backend, freezer):
    now = datetime.datetime.now()
    response = backend.payment_status(transaction_id='cc0cb210-1cd4-11ea-8cca-0213ad91a103', transaction_date=now)
    assert response.result == eopayment.WAITING


@set_history_name('test_get_info_paiement_P5')
def test_P5_and_payment_status_utc_aware_now_later(payfip, backend, freezer):
    utc_now = datetime.datetime.now(pytz.utc)
    freezer.move_to(datetime.timedelta(minutes=25))
    response = backend.payment_status(transaction_id='cc0cb210-1cd4-11ea-8cca-0213ad91a103', transaction_date=utc_now)
    assert response.result == eopayment.EXPIRED


@set_history_name('test_get_info_paiement_P5')
def test_P5_and_payment_status_utc_naive_now_later(payfip, backend, freezer):
    now = datetime.datetime.now()
    freezer.move_to(datetime.timedelta(minutes=25))
    response = backend.payment_status(transaction_id='cc0cb210-1cd4-11ea-8cca-0213ad91a103', transaction_date=now)
    assert response.result == eopayment.EXPIRED


def test_payment_ok(payfip, backend):
    payment_id, kind, url = backend.request(
        amount='10.00',
        email=MEL,
        # make test deterministic
        refdet='201912261758460053903194')

    assert payment_id == 'cc0cb210-1cd4-11ea-8cca-0213ad91a103'
    assert kind == eopayment.URL
    assert url == 'https://www.tipi.budget.gouv.fr/tpa/paiementws.web?idop=cc0cb210-1cd4-11ea-8cca-0213ad91a103'

    response = backend.response('idop=%s' % payment_id)
    assert response.result == eopayment.PAID
    assert response.bank_status == 'paid CB'
    assert response.order_id == payment_id
    assert response.transaction_id == (
        '201912261758460053903194 cc0cb210-1cd4-11ea-8cca-0213ad91a103 112233445566-tip')


@set_history_name('test_payment_ok')
def test_payment_status_ok(history, backend, freezer):
    history.counter = 1  # only the response
    now = datetime.datetime.now()
    response = backend.payment_status(transaction_id='cc0cb210-1cd4-11ea-8cca-0213ad91a103', transaction_date=now)
    assert response.result == eopayment.PAID


def test_payment_denied(history, backend):
    payment_id, kind, url = backend.request(
        amount='10.00',
        email=MEL,
        # make test deterministic
        refdet='201912261758460053903194')

    assert payment_id == 'cc0cb210-1cd4-11ea-8cca-0213ad91a103'
    assert kind == eopayment.URL
    assert url == 'https://www.tipi.budget.gouv.fr/tpa/paiementws.web?idop=cc0cb210-1cd4-11ea-8cca-0213ad91a103'

    response = backend.response('idop=%s' % payment_id)
    assert response.result == eopayment.DENIED
    assert response.bank_status == 'refused CB'
    assert response.order_id == payment_id
    assert response.transaction_id == '201912261758460053903194 cc0cb210-1cd4-11ea-8cca-0213ad91a103'


@set_history_name('test_payment_denied')
def test_payment_status_denied(history, backend, freezer):
    history.counter = 1  # only the response
    now = datetime.datetime.now()
    response = backend.payment_status(transaction_id='cc0cb210-1cd4-11ea-8cca-0213ad91a103', transaction_date=now)
    assert response.result == eopayment.DENIED


def test_payment_cancelled(history, backend):
    payment_id, kind, url = backend.request(
        amount='10.00',
        email=MEL,
        # make test deterministic
        refdet='201912261758460053903194')

    assert payment_id == 'cc0cb210-1cd4-11ea-8cca-0213ad91a103'
    assert kind == eopayment.URL
    assert url == 'https://www.tipi.budget.gouv.fr/tpa/paiementws.web?idop=cc0cb210-1cd4-11ea-8cca-0213ad91a103'

    response = backend.response('idop=%s' % payment_id)
    assert response.result == eopayment.CANCELLED
    assert response.bank_status == 'cancelled CB'
    assert response.order_id == payment_id
    assert response.transaction_id == '201912261758460053903194 cc0cb210-1cd4-11ea-8cca-0213ad91a103'


@set_history_name('test_payment_cancelled')
def test_payment_status_cancelled(history, backend, freezer):
    history.counter = 1  # only the response
    now = datetime.datetime.now()
    response = backend.payment_status(transaction_id='cc0cb210-1cd4-11ea-8cca-0213ad91a103', transaction_date=now)
    assert response.result == eopayment.CANCELLED


def test_normalize_objet():
    assert normalize_objet(None) is None
    assert (
        normalize_objet('18/09/2020  Établissement attestation hors-sol n#1234')
        == '18092020 Etablissement attestation hors sol n1234'
    )


def test_refdet_exer(get_idop, backend):
    payment_id, kind, url = backend.request(
        amount='10.00',
        email=MEL,
        # make test deterministic
        exer=EXER,
        refdet=REFDET)

    assert payment_id == 'idop-1234'
    kwargs = get_idop.call_args[1]

    assert kwargs == {
        'exer': EXER,
        'refdet': REFDET,
        'montant': '1000',
        'objet': None,
        'mel': MEL,
        'numcli': NUMCLI,
        'saisie': 'T',
        'url_notification': NOTIF_URL,
        'url_redirect': REDIRECT_URL,
    }


def test_transaction_id_orderid_subject(get_idop, backend):
    payment_id, kind, url = backend.request(
        amount='10.00',
        email=MEL,
        # make test deterministic
        exer=EXER,
        transaction_id='TR12345',
        orderid='F20190003',
        subject='Précompte famille #1234')

    assert payment_id == 'idop-1234'
    kwargs = get_idop.call_args[1]

    assert kwargs == {
        'exer': EXER,
        'refdet': 'TR12345',
        'montant': '1000',
        'objet': 'O F20190003 S Precompte famille 1234',
        'mel': MEL,
        'numcli': NUMCLI,
        'saisie': 'T',
        'url_notification': NOTIF_URL,
        'url_redirect': REDIRECT_URL,
    }


def test_invalid_transaction_id_valid_orderid(get_idop, backend):
    payment_id, kind, url = backend.request(
        amount='10.00',
        email=MEL,
        # make test deterministic
        exer=EXER,
        transaction_id='TR-12345',
        orderid='F20190003',
        subject='Précompte famille #1234')

    assert payment_id == 'idop-1234'
    kwargs = get_idop.call_args[1]

    assert kwargs == {
        'exer': EXER,
        'refdet': 'F20190003',
        'montant': '1000',
        'objet': 'Precompte famille 1234 T TR 12345',
        'mel': MEL,
        'numcli': NUMCLI,
        'saisie': 'T',
        'url_notification': NOTIF_URL,
        'url_redirect': REDIRECT_URL,
    }


def test_invalid_transaction_id_invalid_orderid(get_idop, backend):
    payment_id, kind, url = backend.request(
        amount='10.00',
        email=MEL,
        # make test deterministic
        exer=EXER,
        transaction_id='TR-12345',
        orderid='F/20190003',
        subject='Précompte famille #1234')

    assert payment_id == 'idop-1234'
    kwargs = get_idop.call_args[1]

    assert kwargs == {
        'exer': EXER,
        'refdet': REFDET_GEN,
        'montant': '1000',
        'objet': 'O F20190003 S Precompte famille 1234 T TR 12345',
        'mel': MEL,
        'numcli': NUMCLI,
        'saisie': 'T',
        'url_notification': NOTIF_URL,
        'url_redirect': REDIRECT_URL,
    }
