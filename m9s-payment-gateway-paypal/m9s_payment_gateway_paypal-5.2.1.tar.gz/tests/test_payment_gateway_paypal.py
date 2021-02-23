# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class PaymentGatewayPaypalTestCase(ModuleTestCase):
    'Test Payment Gateway Paypal module'
    module = 'payment_gateway_paypal'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PaymentGatewayPaypalTestCase))
    return suite
