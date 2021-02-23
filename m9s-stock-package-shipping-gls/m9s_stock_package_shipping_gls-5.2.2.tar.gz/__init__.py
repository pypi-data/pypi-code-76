# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import carrier
from . import stock

__all__ = ['register']


def register():
    Pool.register(
        stock.ShipmentOut,
        carrier.CredentialGLS,
        carrier.Carrier,
        module='stock_package_shipping_gls', type_='model')
    Pool.register(
        stock.CreateShipping,
        stock.CreateShippingGLS,
        module='stock_package_shipping_gls', type_='wizard')
