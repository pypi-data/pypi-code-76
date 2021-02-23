# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, MatchMixin, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

TRACKING_URL = 'https://gls-group.eu/track/'


class CredentialGLS(ModelSQL, ModelView, MatchMixin):
    'GLS Credential'
    __name__ = 'carrier.credential.gls'

    company = fields.Many2One('company.company', 'Company')
    user_id = fields.Char('User', required=True)
    password = fields.Char('Password', required=True)
    customer_id = fields.Char('Customer ID', required=True)
    contact_id = fields.Char('Contact ID', required=True)
    server = fields.Selection([
            ('testing', 'Testing'),
            ('production', 'Production'),
            ], 'Server')

    @classmethod
    def default_server(cls):
        return 'testing'


class Carrier(metaclass=PoolMeta):
    __name__ = 'carrier'

    gls_service_type = fields.Selection([
            (None, ''),
            ('businessparcel', 'BusinessParcel'),
            ('eurobusinessparcel', 'EuroBusinessParcel'),
            ('cashondelivery', 'CashService'),
            ('deliveryatworkservice', 'DeliveryatWorkService'),
            ('shopdeliveryservice', 'ShopDeliveryService'),
            ('depositservice', 'DepositService'),
            ('identpinservice', 'IdentPinService'),
            ('intercompanyservice', 'IntercompanyService'),
            ('shopreturnservice', 'ShopReturnService'),
            ('guaranteed24service', 'Guaranteed24Service'),
            ('flexdeliveryservice', 'FlexDeliveryService'),
            ('thinkgreenservice', 'ThinkGreenService'),
            ('documentreturnservice', 'DocumentReturnService'),
            ('proofservice', 'ProofService'),
            ('privatedeliveryservice', 'PrivateDeliveryService'),
            ('exworksservice', 'ExworksService'),
            ('exchangeservice', 'ExchangeService'),
            ('pickup', 'Pick&ShipService'),  # (Schedules a pickup and does not return a label)
            ('pickupreturn', 'Pick&ReturnService'),  # (Schedules a pickup and does not return a label)
            ], 'Service Type', sort=False, translate=False,
        states={
            'required': Eval('shipping_service') == 'gls',
            'invisible': Eval('shipping_service') != 'gls',
            },
        depends=['shipping_service'])
    gls_label_image_format = fields.Selection([
            (None, ''),
            ('PDF', 'PDF'),
            ('PNG', 'PNG'),
            ], 'Label Image Format', sort=False, translate=False,
        states={
            'required': Eval('shipping_service') == 'gls',
            'invisible': Eval('shipping_service') != 'gls',
            },
        depends=['shipping_service'])
    gls_label_size = fields.Selection([
            (None, ''),
            ('A4', 'A4'),
            ('A5', 'A5'),
            ('A6', 'A6'),
            ], 'Label Size', sort=False, translate=False,
        states={
            'required': Eval('shipping_service') == 'gls',
            'invisible': Eval('shipping_service') != 'gls',
            },
        depends=['shipping_service'])

    @classmethod
    def __setup__(cls):
        super(Carrier, cls).__setup__()
        cls.shipping_service.selection.append(('gls', 'GLS'))

    @classmethod
    def view_attributes(cls):
        return super(Carrier, cls).view_attributes() + [
            ("/form/separator[@id='gls']", 'states', {
                    'invisible': Eval('shipping_service') != 'gls',
                    }),
            ]

    @staticmethod
    def default_gls_label_image_format():
        return 'PDF'

    @staticmethod
    def default_gls_label_size():
        return 'A6'
