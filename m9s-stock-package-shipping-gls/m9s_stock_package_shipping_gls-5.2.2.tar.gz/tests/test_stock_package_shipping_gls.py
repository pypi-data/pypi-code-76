# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class StockPackageShippingGlsTestCase(ModuleTestCase):
    'Test Stock Package Shipping Gls module'
    module = 'stock_package_shipping_gls'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            StockPackageShippingGlsTestCase))
    return suite
