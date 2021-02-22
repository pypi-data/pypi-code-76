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

from __future__ import unicode_literals, print_function

import functools

from six.moves.urllib.parse import urljoin, parse_qs

import lxml.etree as ET
import zeep
import zeep.exceptions

from .common import (PaymentException, PaymentCommon, ResponseError, URL, PAID,
                     DENIED, CANCELLED, ERROR, PaymentResponse)

_zeep_transport = None


class SagaError(PaymentException):
    pass


class Saga(object):
    def __init__(self, wsdl_url, service_url=None, zeep_client_kwargs=None):
        self.wsdl_url = wsdl_url
        kwargs = (zeep_client_kwargs or {}).copy()
        if _zeep_transport and 'transport' not in kwargs:
            kwargs['transport'] = _zeep_transport
        self.client = zeep.Client(wsdl_url, **kwargs)
        # distribued WSDL is wrong :/
        if service_url:
            self.client.service._binding_options['address'] = service_url

    def soap_call(self, operation, content_tag, **kwargs):
        content = getattr(self.client.service, operation)(**kwargs)
        if 'ISO-8859-1' in content:
            encoded_content = content.encode('latin1')
        else:
            encoded_content = content.encode('utf-8')
        try:
            tree = ET.fromstring(encoded_content)
        except Exception:
            raise SagaError('Invalid SAGA response "%s"' % content[:1024])
        if tree.tag == 'erreur':
            raise SagaError(tree.text)
        if tree.tag != content_tag:
            raise SagaError('Invalid SAGA response "%s"' % content[:1024])
        return tree

    def transaction(self, num_service, id_tiers, compte, lib_ecriture, montant,
                    urlretour_asynchrone, email, urlretour_synchrone):
        tree = self.soap_call(
            'Transaction',
            'url',
            num_service=num_service,
            id_tiers=id_tiers,
            compte=compte,
            lib_ecriture=lib_ecriture,
            montant=montant,
            urlretour_asynchrone=urlretour_asynchrone,
            email=email,
            urlretour_synchrone=urlretour_synchrone)
        # tree == <url>...</url>
        return tree.text

    def page_retour(self, operation, idop):
        tree = self.soap_call(
            operation,
            'ok',
            idop=idop)
        # tree == <ok id_tiers="A1"
        # etat="paye" email="albert,dupond@monsite.com" num_service="222222"
        # montant="100.00" compte="708"
        # lib_ecriture="Paiement pour M. Albert Dupondréservationsejourxxxx" />
        return tree.attrib

    def page_retour_synchrone(self, idop):
        return self.page_retour('PageRetourSynchrone', idop)

    def page_retour_asynchrone(self, idop):
        return self.page_retour('PageRetourAsynchrone', idop)


class Payment(PaymentCommon):
    description = {
        'caption': 'Système de paiement Saga de Futur System',
        'parameters': [
            {
                'name': 'base_url',
                'caption': 'URL de base du WSDL',
                'help_text': 'Sans la partie /paiement_internet_ws_ministere?wsdl',
                'required': True,
            },
            {
                'name': 'num_service',
                'caption': 'Numéro du service',
                'required': True,
            },
            {
                'name': 'compte',
                'caption': 'Compte de recettes',
                'required': True,
            },
            {
                'name': 'normal_return_url',
                'caption': 'URL de retour',
                'default': '',
                'required': True,
            },
            {
                'name': 'automatic_return_url',
                'caption': 'URL de notification',
                'required': False,
            },
        ]
    }

    @property
    def saga(self):
        return Saga(
            wsdl_url=urljoin(self.base_url, 'paiement_internet_ws_ministere?wsdl'))

    def request(self, amount, email, subject, orderid=None, **kwargs):
        num_service = self.num_service
        id_tiers = '-1'
        compte = self.compte
        lib_ecriture = subject
        montant = self.clean_amount(amount, max_amount=100000, cents=False)
        urlretour_synchrone = self.normal_return_url
        urlretour_asynchrone = self.automatic_return_url

        url = self.saga.transaction(
            num_service=num_service,
            id_tiers=id_tiers,
            compte=compte,
            lib_ecriture=lib_ecriture,
            montant=montant,
            urlretour_asynchrone=urlretour_asynchrone,
            email=email,
            urlretour_synchrone=urlretour_synchrone)

        try:
            idop = parse_qs(url.split('?', 1)[-1])['idop'][0]
        except Exception:
            raise SagaError('Invalid payment URL, no idop: %s' % url)

        return str(idop), URL, url

    def response(self, query_string, **kwargs):
        fields = parse_qs(query_string, True)
        idop = (fields.get('idop') or [None])[0]

        if not idop:
            raise ResponseError('missing idop parameter in query')

        redirect = kwargs.get('redirect', False)

        if redirect:
            response = self.saga.page_retour_synchrone(idop=idop)
        else:
            response = self.saga.page_retour_asynchrone(idop=idop)

        etat = response['etat']
        if etat == 'paye':
            result = PAID
            bank_status = 'paid'
        elif etat == 'refus':
            result = DENIED
            bank_status = 'refused'
        elif etat == 'abandon':
            result = CANCELLED
            bank_status = 'cancelled'
        else:
            result = ERROR
            bank_status = 'unknown result code: etat=%r' % etat

        return PaymentResponse(
            result=result,
            bank_status=bank_status,
            signed=True,
            bank_data=dict(response),
            order_id=idop,
            transaction_id=idop,
            test=False)


if __name__ == '__main__':
    import click

    def show_payfip_error(func):
        @functools.wraps(func)
        def f(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except SagaError as e:
                click.echo(click.style('SAGA ERROR : %s' % e, fg='red'))
        return f

    @click.group()
    @click.option('--wsdl-url')
    @click.option('--service-url', default=None)
    @click.pass_context
    def main(ctx, wsdl_url, service_url):
        import logging
        logging.basicConfig(level=logging.INFO)
        # hide warning from zeep
        logging.getLogger('zeep.wsdl.bindings.soap').level = logging.ERROR

        ctx.obj = Saga(wsdl_url=wsdl_url, service_url=service_url)

    @main.command()
    @click.option('--num-service', type=str, required=True)
    @click.option('--id-tiers', type=str, required=True)
    @click.option('--compte', type=str, required=True)
    @click.option('--lib-ecriture', type=str, required=True)
    @click.option('--montant', type=str, required=True)
    @click.option('--urlretour-asynchrone', type=str, required=True)
    @click.option('--email', type=str, required=True)
    @click.option('--urlretour-synchrone', type=str, required=True)
    @click.pass_obj
    @show_payfip_error
    def transaction(saga, num_service, id_tiers, compte, lib_ecriture, montant,
                    urlretour_asynchrone, email, urlretour_synchrone):
        url = saga.transaction(
            num_service=num_service,
            id_tiers=id_tiers,
            compte=compte,
            lib_ecriture=lib_ecriture,
            montant=montant,
            urlretour_asynchrone=urlretour_asynchrone,
            email=email,
            urlretour_synchrone=urlretour_synchrone)
        print('url:', url)

    main()
