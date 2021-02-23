# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import carrier
from . import stock
from . import sale

__all__ = ['register']


def register():
    Pool.register(
        carrier.Carrier,
        carrier.CarrierService,
        carrier.BoxType,
        carrier.VolumePriceList,
        stock.ShipmentIn,
        stock.ShipmentOut,
        sale.Sale,
        module='carrier_weight_volume_combined', type_='model')
