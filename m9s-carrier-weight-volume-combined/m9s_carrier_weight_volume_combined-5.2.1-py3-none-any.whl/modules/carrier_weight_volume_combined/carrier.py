# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal

from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Eval, Bool, Id
from trytond.pool import PoolMeta
from trytond.transaction import Transaction


class Carrier(metaclass=PoolMeta):
    __name__ = 'carrier'
    volume_uom = fields.Many2One('product.uom', 'Volume Uom',
        domain=[('category', '=', Id('product', 'uom_cat_volume'))],
        states={
            'invisible': Eval('carrier_cost_method') != 'weight_volume',
            'required': Eval('carrier_cost_method') == 'weight_volume',
            'readonly': Bool(Eval('weight_price_list', [])),
            },
        depends=['carrier_cost_method', 'weight_price_list'])
    volume_uom_digits = fields.Function(fields.Integer('Volume Uom Digits'),
        'on_change_with_volume_uom_digits')
    volume_price_list = fields.One2Many('carrier.volume_price_list', 'carrier',
        'Volume Price List',
        states={
            'invisible': Eval('carrier_cost_method') != 'weight_volume',
            'readonly': ~(Eval('volume_uom', 0) & Eval('weight_currency', 0)),
            },
        depends=['carrier_cost_method', 'volume_uom', 'weight_currency'])

    @classmethod
    def __setup__(cls):
        super(Carrier, cls).__setup__()
        selection = ('weight_volume', 'Weight Volume Combined')
        if selection not in cls.carrier_cost_method.selection:
            cls.carrier_cost_method.selection.append(selection)
        invisible = Eval('carrier_cost_method') != 'weight_volume'
        required = Eval('carrier_cost_method') == 'weight_volume'
        for fname in ('weight_uom', 'weight_currency', 'weight_price_list'):
            field = getattr(cls, fname)
            field.states['invisible'] = field.states.get('invisible') & invisible
            if field.states.get('required'):
                field.states['required'] = field.states.get('required') | required
        cls.weight_price_list.string = 'Weight Price List'

    @staticmethod
    def default_volume_uom_digits():
        return 2

    @fields.depends('volume_uom')
    def on_change_with_volume_uom_digits(self, name=None):
        if self.volume_uom:
            return self.volume_uom.digits
        return 2

    def compute_volume_price(self, volume):
        "Compute price based on volume"
        for line in reversed(self.volume_price_list):
            if line.volume < volume:
                return line.price
        return Decimal(0)

    def get_sale_price(self):
        price, currency_id = super(Carrier, self).get_sale_price()
        if self.carrier_cost_method == 'weight_volume':
            # The highest match for either weight or volume determines the
            # necessary price
            weight_price = Decimal(0)
            for weight in Transaction().context.get('weights', []):
                weight_price += self.compute_weight_price(weight)
            volume_price = Decimal(0)
            for volume in Transaction().context.get('volumes', []):
                volume_price += self.compute_volume_price(volume)
            return max(weight_price, volume_price), self.weight_currency.id
        return price, currency_id

    def get_purchase_price(self):
        price, currency_id = super(Carrier, self).get_purchase_price()
        if self.carrier_cost_method == 'weight_volume':
            weight_price = Decimal(0)
            for weight in Transaction().context.get('weights', []):
                weight_price += self.compute_weight_price(weight)
            volume_price = Decimal(0)
            for volume in Transaction().context.get('volumes', []):
                volume_price += self.compute_volume_price(volume)
            return max(weight_price, volume_price), self.weight_currency.id
        return price, currency_id


class VolumePriceList(ModelSQL, ModelView):
    'Carrier Volume Price List'
    __name__ = 'carrier.volume_price_list'
    carrier = fields.Many2One('carrier', 'Carrier', required=True, select=True)
    volume = fields.Float('Volume',
        digits=(16, Eval('_parent_carrier', {}).get('volume_uom_digits', 2)))
    price = fields.Numeric('Price',
        digits=(
            16, Eval('_parent_carrier', {}).get('weight_currency_digits', 2)))

    @classmethod
    def __setup__(cls):
        super(VolumePriceList, cls).__setup__()
        cls._order.insert(0, ('volume', 'ASC'))


class CarrierService(metaclass=PoolMeta):
    __name__ = 'carrier.service'

    @classmethod
    def __setup__(cls):
        super(CarrierService, cls).__setup__()

        selection = ('weight_volume', 'Weight/Volume')
        if selection not in cls.carrier_cost_method.selection:
            cls.carrier_cost_method.selection.append(selection)


class BoxType(metaclass=PoolMeta):
    __name__ = "carrier.box_type"

    @classmethod
    def __setup__(cls):
        super(BoxType, cls).__setup__()

        selection = ('weight_volume', 'Weight/Volume')
        if selection not in cls.carrier_cost_method.selection:
            cls.carrier_cost_method.selection.append(selection)
