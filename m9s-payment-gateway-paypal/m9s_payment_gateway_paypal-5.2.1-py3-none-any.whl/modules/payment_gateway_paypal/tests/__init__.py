# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.payment_gateway_paypal.tests.test_payment_gateway_paypal import suite
except ImportError:
    from .test_payment_gateway_paypal import suite

__all__ = ['suite']
