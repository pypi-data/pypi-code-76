# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.tests.test_tryton import suite as test_suite


class PartyVcarddavTestCase(ModuleTestCase):
    'Test Party Vcarddav module'
    module = 'party_vcarddav'

    @with_transaction()
    def test_0010_party_vcard_report(self):
        'Test Party VCARD report'
        pool = Pool()
        Party = pool.get('party.party')
        VCardReport = pool.get('party_vcarddav.party.vcard', type='report')

        party1, = Party.create([{
                    'name': 'Party 1',
                    }])
        oext, content, _, _ = VCardReport.execute([party1.id], {})
        self.assertEqual(oext, 'vcf')
        self.assertIn('FN:Party 1', str(content))


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PartyVcarddavTestCase))
    return suite
