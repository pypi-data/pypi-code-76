# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.account_de.tests.test_account_de import suite
except ImportError:
    from .test_account_de import suite

__all__ = ['suite']
