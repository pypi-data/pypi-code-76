# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.stock_package_shipping_gls.tests.test_stock_package_shipping_gls import suite
except ImportError:
    from .test_stock_package_shipping_gls import suite

__all__ = ['suite']
