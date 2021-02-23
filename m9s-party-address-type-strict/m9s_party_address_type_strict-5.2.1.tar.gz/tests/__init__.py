# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.party_address_type_strict.tests.test_party_address_type_strict import suite
except ImportError:
    from .test_party_address_type_strict import suite

__all__ = ['suite']
