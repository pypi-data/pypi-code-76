# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import json
import re
import base64
import requests
import ssl

from trytond.config import config
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateTransition, StateAction
from trytond.exceptions import UserError
from trytond.i18n import gettext

SERVER_URLS = {
    'testing': 'https://api-qs.gls-group.eu/public/v1/shipments',
    'production': 'https://api.gls-group.eu/public/v1/shipments',
    }


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    def validate_packing_gls(self):
        warehouse_address = self.warehouse.address
        if not warehouse_address:
            raise UserError(gettext(
                    'stock_package_shipping_gls.warehouse_address_required',
                    warehouse=self.warehouse.rec_name))
        #if warehouse_address.country != self.delivery_address.country:
        #    for party in {self.customer, self.company.party}:
        #        for mechanism in party.contact_mechanisms:
        #            if mechanism.type in ('phone', 'mobile'):
        #                break
        #        else:
        #            raise UserError(gettext('stock_package_shipping_gls.phone_required', {
        #                    'party': party.rec_name,
        #                    })
        #    if not self.shipping_description:
        #        if (any(p.type.gls_code != '01' for p in self.root_packages)
        #                and self.carrier.gls_service_type != '11'):
        #            # TODO Should also test if a country is not in the EU
        #            raise UserError(gettext('stock_package_shipping_gls.shipping_description_required', {
        #                    'shipment': self.rec_name,
        #                    })


class CreateShipping(metaclass=PoolMeta):
    __name__ = 'stock.shipment.create_shipping'

    gls = StateAction(
        'stock_package_shipping_gls.act_create_shipping_gls_wizard')

    def transition_start(self):
        pool = Pool()
        ShipmentOut = pool.get('stock.shipment.out')

        shipment = ShipmentOut(Transaction().context['active_id'])
        next_state = super(CreateShipping, self).transition_start()
        if shipment.carrier.shipping_service == 'gls':
            next_state = 'gls'
        return next_state

    def do_gls(self, action):
        ctx = Transaction().context
        return action, {
            'model': ctx['active_model'],
            'id': ctx['active_id'],
            'ids': [ctx['active_id']],
            }


class CreateShippingGLS(Wizard):
    'Create GLS Shipping'
    __name__ = 'stock.shipment.create_shipping.gls'

    start = StateTransition()

    def transition_start(self):
        pool = Pool()
        ShipmentOut = pool.get('stock.shipment.out')
        Package = pool.get('stock.package')

        shipment = ShipmentOut(Transaction().context['active_id'])
        if shipment.reference:
            raise UserError(gettext(
                    'stock_package_shipping_gls.has_reference_number',
                    shipment=shipment.rec_name))

        credential = self.get_credential(shipment)
        api_url = config.get('stock_package_shipping_gls', credential.server,
            default=SERVER_URLS[credential.server])
        headers = self.get_request_header()
        auth = self.get_authorization(credential)
        packages = [p for p in shipment.root_packages
            if not p.shipping_reference]
        shipment_request = self.get_request(shipment, packages, credential)
        data = json.dumps(shipment_request, ensure_ascii=True,
            encoding="utf-8")

        nb_tries, response = 0, None
        error_message = ''
        try:
            while nb_tries < 5 and response is None:
                try:
                    req = requests.post(api_url, headers=headers, data=data,
                        auth=auth)
                except ssl.SSLError as e:
                    error_message = e.message
                    nb_tries += 1
                    continue
                req.raise_for_status()
                response = req.json()
        except requests.HTTPError as e:
            msg = req.json()
            description = msg['errors'][0]['description']
            exit_msg = msg['errors'][0]['exitMessage']
            exit_code = msg['errors'][0]['exitCode']
            error_message = '\n'.join([e.message, description, exit_msg])

        if error_message:
            raise UserError(gettext(
                    'stock_package_shipping_gls.gls_webservice_error',
                    message=error_message))

        shipment.reference = response['consignmentId']
        gls_packages = response['parcels']

        # Only one pdf containing all labels
        label = fields.Binary.cast(base64.b64decode(
                    response['labels'][0]))

        for tryton_pkg, gls_pkg in zip(packages, gls_packages):
            tryton_pkg.shipping_reference = gls_pkg['trackId']
            tryton_pkg.shipping_label = label
            if hasattr(tryton_pkg, 'label_file_name'):
                tryton_pkg.label_file_name = gls_pkg['trackId'] + '.pdf'
        Package.save(packages)
        shipment.save()

        return 'end'

    def get_credential_pattern(self, shipment):
        return {
            'company': shipment.company.id,
            }

    def get_credential(self, shipment):
        pool = Pool()
        GLSCredential = pool.get('carrier.credential.gls')

        credential_pattern = self.get_credential_pattern(shipment)
        for credential in GLSCredential.search([]):
            if credential.match(credential_pattern):
                return credential
        raise UserError(gettext(
                'stock_package_shipping_gls.missing_configuration',
                company=shipment.company.rec_name))

    def get_authorization(self, credential):
        return (credential.user_id, credential.password)

    def get_request_header(self):
        return {
            'Accept-Language': 'de',
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }

    def get_request_address(self, party, address):
        assert party == address.party

        def format_field(field, length):
            res = ''
            # address.subdivison returns for some unknown reason the record
            # instead of rec_name
            if field:
                if not isinstance(field, unicode):
                    res = field.rec_name[0:length]
                else:
                    res = field[0:length]
            return res

        delivery_address = {
            'name1': format_field(address.party_full_name, 40),
            #'name2': format_field(address.party_name, 40),
            'street1': format_field(address.street, 40),
            'street2': format_field(address.name, 40),
            'country': address.country.code if address.country else 'DE',
            'zipCode': format_field(address.zip, 10),
            'city': format_field(address.city, 40),
            'province': format_field(address.subdivision, 40),
            }
        phone = ''
        mobile = ''
        email = ''
        for mechanism in party.contact_mechanisms:
            if mechanism.type == 'phone':
                phone = mechanism.value
            elif mechanism.type == 'mobile':
                mobile = mechanism.value
            elif mechanism.type == 'email':
                email = mechanism.value
        if phone:
            phone = re.sub('[/() .-]', '', phone)
            if len(phone) <= 40:
                delivery_address['phone'] = phone
        if mobile:
            mobile = re.sub('[/() .-]', '', mobile)
            if len(mobile) <= 40:
                delivery_address['mobile'] = mobile
        if email and len(email) <= 100:
                delivery_address['email'] = email
        return delivery_address

    def get_package(self, package, shipment):
        pool = Pool()
        Sale = pool.get('sale.sale')

        res = {
            'weight': package.weight,
            'references': [
                'Package %s' % package.code,
                'Shipment %s' % shipment.number
                ],
            'comment': package.shipment.shipping_description,
            }
        if shipment.carrier.gls_service_type not in ['businessparcel',
                'eurobusinessparcel']:
            services = {'name': shipment.carrier.gls_service_type}
            if shipment.carrier.gls_service_type == 'cashondelivery':
                sales = Sale.search([
                        ('number', '=', shipment.origins),
                        ])
                if sales:
                    sale = sales[0]
                    services['infos'] = [
                        {'name': 'amount', 'value': str(sale.total_amount)},
                        {'name': 'reference', 'value': sale.number}
                        ]
            if shipment.carrier.gls_service_type == 'shopdeliveryservice':
                services['infos'] = [
                    {'name': 'directshop', 'value': 'Y'},
                    ]
            res['services'] = [services]
        return res

    def get_request(self, shipment, packages, credential):
        shipper_address = self.get_request_address(shipment.company.party,
            shipment.warehouse.address)
        delivery_address = self.get_request_address(shipment.customer,
            shipment.delivery_address)

        if shipment.carrier.gls_service_type in [
                'flexdeliveryservice', 'shopdeliveryservice']:
            if (not delivery_address.get('email')
                    and not delivery_address.get('mobile')):
                        raise UserError(gettext(
                                'stock_package_shipping_gls.email_or_mobile_required',
                                shipment=shipment.rec_name))
        if shipment.carrier.gls_service_type == 'shopdeliveryservice':
            delivery_address['contact'] = shipment.customer.rec_name

        packages = [self.get_package(p, shipment) for p in packages]

        return {
            'shipperId': ' '.join([credential.customer_id,
                    credential.contact_id]),
            'addresses': {
                'delivery': delivery_address,
                'alternativeShipper': shipper_address,
                # XXX TODO:
                # 'return': {}
                # 'pickup': {}
                },
            # XXX TODO
            # returns
            'parcels': packages,
            'labelFormat': shipment.carrier.gls_label_image_format,
            'labelSize': shipment.carrier.gls_label_size,
            }
