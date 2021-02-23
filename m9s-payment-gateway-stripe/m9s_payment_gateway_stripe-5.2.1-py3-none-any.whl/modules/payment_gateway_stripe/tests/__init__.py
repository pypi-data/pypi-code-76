# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.payment_gateway_stripe.tests.test_payment_gateway_stripe import suite
except ImportError:
    from .test_payment_gateway_stripe import suite

__all__ = ['suite']
