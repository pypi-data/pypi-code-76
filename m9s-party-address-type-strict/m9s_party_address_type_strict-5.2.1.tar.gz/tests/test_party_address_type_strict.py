# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class PartyAddressTypeStrictTestCase(ModuleTestCase):
    'Test Party Address Type Strict module'
    module = 'party_address_type_strict'
    extras = [
        'account_invoice',
        'stock',
        ]


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PartyAddressTypeStrictTestCase))
    return suite
