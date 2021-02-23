# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool


class PartyVCardDAVTestCase(ModuleTestCase):
    'Test PartyVCardDAV module'
    module = 'party_vcarddav'

    @with_transaction()
    def test_party_vcard_report(self):
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
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PartyVCardDAVTestCase))
    return suite
