# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.payment_gateway.tests.test_payment_gateway import (
        suite, create_payment_gateway, create_payment_transaction,
        create_payment_profile)
except ImportError:
    from .test_payment_gateway import (
        suite, create_payment_gateway, create_payment_transaction,
        create_payment_profile)

__all__ = ['suite', 'create_payment_gateway', 'create_payment_transaction',
    'create_payment_profile']
