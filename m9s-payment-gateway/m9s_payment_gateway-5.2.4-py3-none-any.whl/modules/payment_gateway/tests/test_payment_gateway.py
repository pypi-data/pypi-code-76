# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.tests.test_tryton import suite as test_suite
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.exceptions import UserError

from trytond.modules.company.tests import create_company, set_company
from trytond.modules.account.tests import create_chart, get_fiscalyear
try:
    from trytond.modules.account_invoice.tests import set_invoice_sequences
except:
    set_invoice_sequences = None


def create_payment_gateway(method='manual', provider=None):
    """
    Create and return a payment transaction
    """
    pool = Pool()
    Company = pool.get('company.company')
    FiscalYear = pool.get('account.fiscalyear')
    Journal = pool.get('account.journal')
    Account = pool.get('account.account')
    PaymentGateway = pool.get('payment_gateway.gateway')

    companies = Company.search([])
    if companies:
        company = companies[0]
    else:
        company = create_company()

    with set_company(company):
        fiscalyear_id = FiscalYear.find(company.id, exception=False)
        if fiscalyear_id is None:
            fiscalyear = get_fiscalyear(company)
            # Set the invoice sequences if account_invoice is installed
            if set_invoice_sequences:
                fiscalyear = set_invoice_sequences(fiscalyear)
            fiscalyear.save()
            FiscalYear.create_period([fiscalyear])
            create_chart(company)
        else:
            fiscalyear = FiscalYear(fiscalyear_id)

        journal_revenue, = Journal.search([
                ('code', '=', 'REV'),
                ])
        journal_expense, = Journal.search([
                ('code', '=', 'EXP'),
                ])
        journal_cash, = Journal.search([
                ('code', '=', 'CASH'),
                ])
        revenue, = Account.search([
                ('type.revenue', '=', True),
                ])
        receivable, = Account.search([
                ('type.receivable', '=', True),
                ])
        expense, = Account.search([
                ('type.expense', '=', True),
                ])
        payable, = Account.search([
                ('type.payable', '=', True),
                ])
        cash, = Account.search([
                ('name', '=', 'Main Cash'),
                ])

        context = {
            'company': company.id,
            'use_dummy': True if method == 'dummy' else False,
            }
        with Transaction().set_context(**context):
            gateway, = PaymentGateway.create([{
                    'name': 'Gateway %s' % method,
                    'journal': journal_cash,
                    'account': expense,
                    'provider': provider if provider else method,
                    'method': method,
                    }])
        return gateway


def create_payment_transaction(method='manual', amount=400):
    """
    Create and return a payment transaction
    """
    pool = Pool()
    Party = pool.get('party.party')
    Address = pool.get('party.address')
    Company = pool.get('company.company')
    Account = pool.get('account.account')
    PaymentGatewayTransaction = pool.get('payment_gateway.transaction')

    gateway = create_payment_gateway(method=method)
    company, = Company.search([])
    with set_company(company):
        context = {
            'company': company.id,
            'use_dummy': True if method == 'dummy' else False,
            }
        with Transaction().set_context(**context):
            receivable, = Account.search([
                    ('type.receivable', '=', True),
                    ])
            party = Party(name='Party')
            party.account_receivable = receivable
            party.save()
            address, = Address.create([{
                    'party': party.id,
                    }])
            transaction, = PaymentGatewayTransaction.create([{
                'party': party,
                'credit_account': party.account_receivable,
                'address': party.addresses[0],
                'gateway': gateway,
                'amount': amount,
                }])
        return transaction


def create_payment_profile(party, gateway):
    """
    Create a payment profile for the party
    """
    pool = Pool()
    AddPaymentProfileWizard = pool.get(
        'party.party.payment_profile.add', type='wizard')

    profile_wiz = AddPaymentProfileWizard(
        AddPaymentProfileWizard.create()[0])
    profile_wiz.card_info.party = party.id
    profile_wiz.card_info.address = party.addresses[0].id
    profile_wiz.card_info.provider = gateway.provider
    profile_wiz.card_info.gateway = gateway
    profile_wiz.card_info.owner = party.name
    profile_wiz.card_info.number = '4111111111111111'
    profile_wiz.card_info.expiry_month = '11'
    profile_wiz.card_info.expiry_year = '2025'
    profile_wiz.card_info.csc = '353'

    with Transaction().set_context(return_profile=True):
        return profile_wiz.transition_add()


class PaymentGatewayTestCase(ModuleTestCase):
    'Test Payment Gateway module'
    module = 'payment_gateway'

    @with_transaction()
    def test_0005_payment_transaction_search_rec_name(self):
        """
        Search payment transaction with UUID and Customer Name
        """
        pool = Pool()
        PaymentGatewayTransaction = pool.get('payment_gateway.transaction')

        transaction = create_payment_transaction()

        self.assertTrue(
            PaymentGatewayTransaction.search([
                ('rec_name', 'ilike', '%' + transaction.uuid + '%'),
                ('rec_name', 'ilike', '%' + transaction.party.name + '%')
                ]))

    @with_transaction()
    def test_0010_test_manual_transaction(self):
        """
        Test manual transaction and journal results
        """
        pool = Pool()
        PaymentGatewayTransaction = pool.get('payment_gateway.transaction')
        AccountMove = pool.get('account.move')
        Company = pool.get('company.company')
        Journal = pool.get('account.journal')
        Period = pool.get('account.period')

        transaction = create_payment_transaction()

        # Process transaction
        PaymentGatewayTransaction.process([transaction])
        # Assert that transaction state is completed
        self.assertEqual(transaction.state, 'completed')
        # Assert that there are no account moves
        self.assertEqual(AccountMove.search([], count="True"), 0)

        company, = Company.search([])
        with Transaction().set_context(company=company.id):
            # Post transaction
            PaymentGatewayTransaction.post([transaction])
        # Assert that the transaction is done
        self.assertEqual(transaction.state, 'posted')
        # Assert that an account move is created
        self.assertEqual(AccountMove.search([], count="True"), 1)
        party = transaction.party
        self.assertEqual(party.receivable_today, -400)
        period_id = Period.find(company.id)
        period = Period(period_id)
        context = {
            'start_date': period.start_date,
            'end_date': period.end_date,
            'company': company.id,
            }
        with Transaction().set_context(**context):
            journal_cash, = Journal.search([
                    ('code', '=', 'CASH'),
                    ])
            self.assertEqual(transaction.gateway.account.balance, 400)
            self.assertEqual(journal_cash.debit, 400)
            self.assertEqual(journal_cash.credit, 0)
            self.assertEqual(journal_cash.balance, 400)

    @with_transaction()
    def test_0210_test_dummy_gateway_process(self):
        """
        Test dummy gateway transaction
        """
        pool = Pool()
        PaymentGatewayTransaction = pool.get('payment_gateway.transaction')

        transaction = create_payment_transaction(method='dummy')
        self.assertTrue(transaction)

        # Only manual transactions can be processed
        with self.assertRaises(UserError):
            PaymentGatewayTransaction.process([transaction])

    @with_transaction()
    def test_0220_test_dummy_gateway_settle(self):
        """
        Test dummy gateway transaction
        """
        pool = Pool()
        PaymentGatewayTransaction = pool.get('payment_gateway.transaction')
        AccountMove = pool.get('account.move')
        Company = pool.get('company.company')
        Journal = pool.get('account.journal')
        Period = pool.get('account.period')

        transaction = create_payment_transaction(method='dummy')
        self.assertTrue(transaction)

        company, = Company.search([])
        period_id = Period.find(company.id)
        period = Period(period_id)
        context = {
            'start_date': period.start_date,
            'end_date': period.end_date,
            'company': company.id,
            }
        with Transaction().set_context(**context):
            # Now authorize and capture a transaction with this
            PaymentGatewayTransaction.authorize([transaction])
            self.assertEqual(transaction.state, 'authorized')

            # Now settle this transaction
            PaymentGatewayTransaction.settle([transaction])
            self.assertEqual(transaction.state, 'posted')
            # Assert that an account move is created
            self.assertEqual(AccountMove.search([], count="True"), 1)
            party = transaction.party
            self.assertEqual(party.receivable_today, -400)
            journal_cash, = Journal.search([
                    ('code', '=', 'CASH'),
                    ])
            self.assertEqual(transaction.gateway.account.balance, 400)
            self.assertEqual(journal_cash.debit, 400)
            self.assertEqual(journal_cash.credit, 0)
            self.assertEqual(journal_cash.balance, 400)

    @with_transaction()
    def test_0220_test_dummy_profile_add(self):
        """
        Test dummy gateway profile addition
        """
        pool = Pool()
        Company = pool.get('company.company')
        PaymentGateway = pool.get('payment_gateway.gateway')

        transaction = create_payment_transaction(method='dummy')

        company, = Company.search([])
        with Transaction().set_context(
                company=company.id, use_dummy=True):

            gateway, = PaymentGateway.search([])
            party = transaction.party
            profile = create_payment_profile(party, gateway)
            self.assertTrue(profile)


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PaymentGatewayTestCase))
    return suite
