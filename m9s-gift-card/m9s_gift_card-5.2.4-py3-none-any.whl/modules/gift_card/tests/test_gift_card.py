# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest

from decimal import Decimal
from unittest.mock import patch

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.tests.test_tryton import suite as test_suite
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.config import config
from trytond.exceptions import UserError

from trytond.modules.company.tests import set_company
from trytond.modules.currency.tests import (create_currency,
    add_currency_rate)
from trytond.modules.payment_gateway.tests import (create_payment_gateway,
    create_payment_profile)
from trytond.modules.invoice_payment_gateway.tests import (create_payment_term,
    create_write_off)
from trytond.modules.sale_payment_gateway.tests import create_sale

from trytond.modules.gift_card import gift_card as gift_card_module


def create_gift_card(set_configuration_account=True):
    """
    Create gift card
    """
    pool = Pool()
    Company = pool.get('company.company')
    GiftCard = pool.get('gift_card.gift_card')
    Configuration = pool.get('gift_card.configuration')
    Sequence = pool.get('ir.sequence')
    Currency = pool.get('currency.currency')
    Account = pool.get('account.account')

    # Setup defaults
    # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
    # etc.)
    gateway = create_payment_gateway()
    gateway.save()
    company, = Company.search([])
    with set_company(company):
        revenue, = Account.search([
                ('type.revenue', '=', True),
                ])
    gift_card_sequence, = Sequence.search([
            ('code', '=', 'gift_card.gift_card'),
            ])
    with Transaction().set_context(company=company.id):
        configuration = Configuration(1)
        configuration.number_sequence = gift_card_sequence
        if set_configuration_account:
            configuration.liability_account = revenue
        configuration.save()

    currencies = Currency.search([
            ('code', '=', 'USD'),
            ])
    if currencies:
        usd = currencies[0]
    else:
        usd = create_currency('USD')
        try:
            add_currency_rate(usd, Decimal('1'))
        except:
            pass

    gift_card, = GiftCard.create([{
        'currency': usd,
        'amount': Decimal('20'),
    }])
    return gift_card


def create_product(type='service', mode='physical', is_gift_card=False,
    allow_open_amount=False):
    """
    Create default product
    """
    pool = Pool()
    Template = pool.get('product.template')
    Category = pool.get('product.category')
    Uom = pool.get('product.uom')
    Account = pool.get('account.account')
    Company = pool.get('company.company')

    company, = Company.search([])
    with set_company(company):
        revenue, = Account.search([
                ('type.revenue', '=', True),
                ])

    with Transaction().set_context(company=company.id):
        category = Category()
        category.name = 'Account category'
        category.account_revenue = revenue
        category.accounting = True
        category.save()
        uom, = Uom.search([('name', '=', 'Unit')])
        values = {
            'name': 'product',
            'type': type,
            'list_price': Decimal('20'),
            'default_uom': uom,
            'salable': True,
            'sale_uom': uom,
            'account_category': category,
            }
        product_values = {
            'code': 'Test Product',
            'cost_price': Decimal('5'),
            }

        if is_gift_card:
            product_values.update({
                    'is_gift_card': True,
                    'gift_card_delivery_mode': mode
                    })
            if not allow_open_amount:
                product_values.update({
                        'gift_card_prices': [
                            ('create', [{
                                        'price': 500,
                                        }, {
                                        'price': 600,
                                        }])
                            ]
                        })
            else:
                product_values.update({
                    'allow_open_amount': True,
                    'gc_min': 100,
                    'gc_max': 400
                })
        values.update({
                'products': [
                    ('create', [product_values])
                    ]
                })
    return Template.create([values])[0].products[0]


FROM = 'no-reply@localhost'


class GiftCardTestCase(ModuleTestCase):
    'Test Gift Card module'
    module = 'gift_card'

    def setUp(self):
        self.smtplib_patcher = patch('smtplib.SMTP')
        self.PatchedSMTP = self.smtplib_patcher.start()
        reset_from = config.get('email', 'from')
        config.set('email', 'from', FROM)
        self.addCleanup(lambda: config.set('email', 'from', reset_from))

    @with_transaction()
    def test0010_create_gift_card(self):
        """
        Create gift card
        """
        gift_card = create_gift_card()
        self.assertEqual(gift_card.state, 'draft')

    @with_transaction()
    def test0015_on_change_currency(self):
        """
        Check if currency digits are changed because of currency of gift
        card
        """
        pool = Pool()
        GiftCard = pool.get('gift_card.gift_card')
        Currency = pool.get('currency.currency')

        usd = Currency(
            name='US Dollar', symbol='$', code='USD', digits=3)
        usd.save()

        gift_card = GiftCard(currency=usd.id)

        self.assertEqual(gift_card.on_change_with_currency_digits(), 3)

        gift_card = GiftCard(currency=None)

        self.assertEqual(gift_card.on_change_with_currency_digits(), 2)

    @with_transaction()
    def test0017_check_on_change_amount(self):
        """
        Check if amount is changed with quantity and unit price
        """
        pool = Pool()
        SaleLine = pool.get('sale.line')
        SaleLine = pool.get('sale.line')
        Company = pool.get('company.company')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            # Sale line as gift card
            sale_line = SaleLine(
                unit_price=Decimal('22.56789'),
                type='line', sale=None)

            sale_line.on_change_is_gift_card()
            self.assertEqual(sale_line.description, None)
            self.assertEqual(sale_line.product, None)

            sale_line.is_gift_card = True
            sale_line.on_change_is_gift_card()

            self.assertEqual(sale_line.product, None)
            self.assertEqual(sale_line.description, 'Gift Card')
            self.assertNotEqual(sale_line.unit, None)

    @with_transaction()
    def test0018_gift_card_transition(self):
        """
        Check gift card transitions
        """
        pool = Pool()
        GiftCard = pool.get('gift_card.gift_card')

        gift_card = create_gift_card()

        self.assertEqual(gift_card.state, 'draft')

        # Gift card can become active in draft state
        GiftCard.activate([gift_card])

        self.assertEqual(gift_card.state, 'active')

        # Gift card can be calcelled from active state
        GiftCard.cancel([gift_card])

        self.assertEqual(gift_card.state, 'canceled')

        # Gift card can be set back to draft state once canceled
        GiftCard.draft([gift_card])

        self.assertEqual(gift_card.state, 'draft')

        # Gift card can be canceled from draft state also
        GiftCard.cancel([gift_card])

        self.assertEqual(gift_card.state, 'canceled')

    @with_transaction()
    def test0020_physical_gift_card_on_processing_sale_order(self):
        """
        Check if physical gift card is being created on processing sale when
        invoice method is order.
        """
        pool = Pool()
        Sale = pool.get('sale.sale')
        GiftCard = pool.get('gift_card.gift_card')
        Invoice = pool.get('account.invoice')
        InvoiceLine = pool.get('account.invoice.line')
        Configuration = pool.get('gift_card.configuration')
        SaleConfiguration = pool.get('sale.configuration')
        AccountConfiguration = pool.get('account.configuration')
        SaleLine = pool.get('sale.line')
        Company = pool.get('company.company')
        Uom = pool.get('product.uom')
        SalePayment = pool.get('sale.payment')
        Account = pool.get('account.account')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        gift_card_product = create_product(type='service',
            is_gift_card=True)

        company, = Company.search([])
        with Transaction().set_context(company=company.id, language='en'):
            revenue, = Account.search([
                    ('type.revenue', '=', True),
                    ])
            account_config = AccountConfiguration(1)
            account_config.default_category_account_revenue = revenue
            account_config.save()

            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()

            sale = create_sale(amount=400)
            sale.invoice_method = 'order'
            sale.save()

            gc_price, _, = gift_card_product.gift_card_prices
            uom, = Uom.search([('name', '=', 'Unit')])
            gift_card_line = SaleLine()
            gift_card_line.sale = sale
            gift_card_line.quantity = 1
            gift_card_line.unit_price = 500
            gift_card_line.unit = uom
            gift_card_line.description = 'Gift Card'
            gift_card_line.product = gift_card_product
            gift_card_line.gc_price = gc_price
            gift_card_line.save()
            comment_line = SaleLine()
            comment_line.sale = sale
            comment_line.type = 'comment'
            comment_line.description = 'Test comment'
            comment_line.save()

            sale_line1, = SaleLine.search([
                    ('sale', '=', sale.id),
                    ('product', '=', gift_card_product.id),
                    ])
            self.assertTrue(sale_line1.is_gift_card)

            sale_line2, = SaleLine.search([
                    ('sale', '=', sale.id),
                    ('type', '=', 'line'),
                    ('id', '!=', sale_line1.id),
                    ])
            self.assertFalse(sale_line2.is_gift_card)

            sale_line3, = SaleLine.search([
                    ('sale', '=', sale.id),
                    ('type', '=', 'comment'),
                    ])
            self.assertFalse(sale_line3.is_gift_card)

            self.assertEqual(sale_line1.gift_card_delivery_mode, 'physical')

            # Gift card line amount is included in untaxed amount
            self.assertEqual(sale.untaxed_amount, 900)

            # Gift card line amount is included in total amount
            self.assertEqual(sale.total_amount, 900)

            Sale.quote([sale])

            self.assertEqual(sale.untaxed_amount, 900)
            self.assertEqual(sale.total_amount, 900)

            Sale.confirm([sale])

            self.assertEqual(sale.untaxed_amount, 900)
            self.assertEqual(sale.total_amount, 900)

            self.assertFalse(
                GiftCard.search([('sale_line', '=', sale_line1.id)])
            )

            self.assertFalse(Invoice.search([]))

            SalePayment.create([{
                'sale': sale,
                'amount': Decimal('1000'),
                'gateway': create_payment_gateway('manual'),
                'credit_account': sale.party.account_receivable,
            }])

            Sale.process([sale])

            self.assertEqual(sale.untaxed_amount, 900)
            self.assertEqual(sale.total_amount, 900)

            self.assertTrue(
                GiftCard.search([('sale_line', '=', sale_line1.id)]))

            self.assertEqual(
                GiftCard.search(
                    [('sale_line', '=', sale_line1.id)], count=True), 1)

            self.assertEqual(Invoice.search([], count=True), 1)

            gift_card, = GiftCard.search([
                ('sale_line', '=', sale_line1.id)
            ])

            invoice, = Invoice.search([])
            line, = InvoiceLine.search([
                ('invoice', '=', invoice.id),
                ('description', '=', 'Gift Card'),
            ])
            self.assertEqual(
                line.account,
                Configuration(1).liability_account
            )

            self.assertEqual(gift_card.amount, 500)
            self.assertEqual(gift_card.state, 'active')
            self.assertEqual(gift_card.sale, sale)

            self.assertEqual(invoice.untaxed_amount, 900)
            self.assertEqual(invoice.total_amount, 900)

    @with_transaction()
    def test0030_physical_gift_card_on_processing_sale_shipment(self):
        """
        Check if physical gift card is being created on processing sale when
        invoice method is shipping.
        """
        pool = Pool()
        Sale = pool.get('sale.sale')
        GiftCard = pool.get('gift_card.gift_card')
        Invoice = pool.get('account.invoice')
        InvoiceLine = pool.get('account.invoice.line')
        Configuration = pool.get('gift_card.configuration')
        SaleConfiguration = pool.get('sale.configuration')
        AccountConfiguration = pool.get('account.configuration')
        SaleLine = pool.get('sale.line')
        Company = pool.get('company.company')
        Uom = pool.get('product.uom')
        SalePayment = pool.get('sale.payment')
        Account = pool.get('account.account')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        gift_card_product = create_product(type='service',
            is_gift_card=True)

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            revenue, = Account.search([
                    ('type.revenue', '=', True),
                    ])
            account_config = AccountConfiguration(1)
            account_config.default_category_account_revenue = revenue
            account_config.save()

            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()

            sale = create_sale(amount=400)
            sale.invoice_method = 'shipment'
            sale.shipment_method = 'order'
            sale.save()

            gc_price, _, = gift_card_product.gift_card_prices
            uom, = Uom.search([('name', '=', 'Unit')])
            gift_card_line = SaleLine()
            gift_card_line.sale = sale
            gift_card_line.quantity = 1
            gift_card_line.unit_price = 500
            gift_card_line.unit = uom
            gift_card_line.description = 'Gift Card'
            gift_card_line.product = gift_card_product
            gift_card_line.gc_price = gc_price
            gift_card_line.save()
            comment_line = SaleLine()
            comment_line.sale = sale
            comment_line.type = 'comment'
            comment_line.description = 'Test comment'
            comment_line.save()

            sale_line1, = SaleLine.search([
                    ('sale', '=', sale.id),
                    ('product', '=', gift_card_product.id),
                    ])
            self.assertTrue(sale_line1.is_gift_card)

            sale_line2, = SaleLine.search([
                    ('sale', '=', sale.id),
                    ('type', '=', 'line'),
                    ('id', '!=', sale_line1.id),
                    ])
            self.assertFalse(sale_line2.is_gift_card)

            sale_line3, = SaleLine.search([
                    ('sale', '=', sale.id),
                    ('type', '=', 'comment'),
                    ])
            self.assertFalse(sale_line3.is_gift_card)

            self.assertEqual(sale_line1.gift_card_delivery_mode, 'physical')

            # Gift card line amount is included in untaxed amount
            self.assertEqual(sale.untaxed_amount, 900)

            # Gift card line amount is included in total amount
            self.assertEqual(sale.total_amount, 900)

            Sale.quote([sale])

            self.assertEqual(sale.untaxed_amount, 900)
            self.assertEqual(sale.total_amount, 900)

            Sale.confirm([sale])

            self.assertEqual(sale.untaxed_amount, 900)
            self.assertEqual(sale.total_amount, 900)

            self.assertFalse(
                GiftCard.search([('sale_line', '=', sale_line1.id)])
            )

            self.assertFalse(Invoice.search([]))

            SalePayment.create([{
                'sale': sale,
                'amount': Decimal('1000'),
                'gateway': create_payment_gateway('manual'),
                'credit_account': sale.party.account_receivable,
            }])

            Sale.process([sale])

            self.assertEqual(sale.untaxed_amount, 900)
            self.assertEqual(sale.total_amount, 900)

            self.assertTrue(
                GiftCard.search([('sale_line', '=', sale_line1.id)]))

            self.assertEqual(
                GiftCard.search(
                    [('sale_line', '=', sale_line1.id)], count=True), 1)

            self.assertEqual(Invoice.search([], count=True), 1)

            gift_card, = GiftCard.search([
                ('sale_line', '=', sale_line1.id)
            ])

            invoice, = Invoice.search([])
            line, = InvoiceLine.search([
                ('invoice', '=', invoice.id),
                ('description', '=', 'Gift Card'),
            ])
            self.assertEqual(
                line.account,
                Configuration(1).liability_account
            )

            self.assertEqual(gift_card.amount, 500)
            self.assertEqual(gift_card.state, 'active')
            self.assertEqual(gift_card.sale, sale)

            self.assertEqual(invoice.untaxed_amount, 900)
            self.assertEqual(invoice.total_amount, 900)

    @with_transaction()
    def test0040_virtual_gift_card_on_processing_sale_shipment(self):
        """
        Check if virtual gift card is being created on processing sale when
        invoice method is shipping.
        """
        pool = Pool()
        Sale = pool.get('sale.sale')
        GiftCard = pool.get('gift_card.gift_card')
        Invoice = pool.get('account.invoice')
        InvoiceLine = pool.get('account.invoice.line')
        Configuration = pool.get('gift_card.configuration')
        SaleConfiguration = pool.get('sale.configuration')
        AccountConfiguration = pool.get('account.configuration')
        SaleLine = pool.get('sale.line')
        Company = pool.get('company.company')
        Uom = pool.get('product.uom')
        SalePayment = pool.get('sale.payment')
        Account = pool.get('account.account')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        gift_card_product = create_product(type='service',
            mode='virtual', is_gift_card=True)

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            revenue, = Account.search([
                    ('type.revenue', '=', True),
                    ])
            account_config = AccountConfiguration(1)
            account_config.default_category_account_revenue = revenue
            account_config.save()

            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()

            sale = create_sale(amount=400)
            sale.invoice_method = 'shipment'
            sale.shipment_method = 'order'
            sale.save()

            gc_price, _, = gift_card_product.gift_card_prices
            uom, = Uom.search([('name', '=', 'Unit')])
            gift_card_line = SaleLine()
            gift_card_line.sale = sale
            gift_card_line.quantity = 1
            gift_card_line.unit_price = 500
            gift_card_line.unit = uom
            gift_card_line.description = 'Gift Card'
            gift_card_line.product = gift_card_product
            gift_card_line.gc_price = gc_price
            gift_card_line.recipient_email = 'test@example.com'
            gift_card_line.save()
            comment_line = SaleLine()
            comment_line.sale = sale
            comment_line.type = 'comment'
            comment_line.description = 'Test comment'
            comment_line.save()

            sale_line1, = SaleLine.search([
                    ('sale', '=', sale.id),
                    ('product', '=', gift_card_product.id),
                    ])
            self.assertTrue(sale_line1.is_gift_card)

            sale_line2, = SaleLine.search([
                    ('sale', '=', sale.id),
                    ('type', '=', 'line'),
                    ('id', '!=', sale_line1.id),
                    ])
            self.assertFalse(sale_line2.is_gift_card)

            sale_line3, = SaleLine.search([
                    ('sale', '=', sale.id),
                    ('type', '=', 'comment'),
                    ])
            self.assertFalse(sale_line3.is_gift_card)

            self.assertEqual(sale_line1.gift_card_delivery_mode, 'virtual')

            # Gift card line amount is included in untaxed amount
            self.assertEqual(sale.untaxed_amount, 900)

            # Gift card line amount is included in total amount
            self.assertEqual(sale.total_amount, 900)

            Sale.quote([sale])

            self.assertEqual(sale.untaxed_amount, 900)
            self.assertEqual(sale.total_amount, 900)

            Sale.confirm([sale])

            self.assertEqual(sale.untaxed_amount, 900)
            self.assertEqual(sale.total_amount, 900)

            self.assertFalse(
                GiftCard.search([('sale_line', '=', sale_line1.id)]))

            self.assertFalse(Invoice.search([]))

            SalePayment.create([{
                'sale': sale,
                'amount': Decimal('1000'),
                'gateway': create_payment_gateway('manual'),
                'credit_account': sale.party.account_receivable,
                }])

            Sale.process([sale])

            self.assertEqual(sale.untaxed_amount, 900)
            self.assertEqual(sale.total_amount, 900)

            self.assertTrue(
                GiftCard.search([('sale_line', '=', sale_line1.id)]))

            self.assertEqual(
                GiftCard.search(
                    [('sale_line', '=', sale_line1.id)], count=True), 1)

            self.assertEqual(Invoice.search([], count=True), 1)

            gift_card, = GiftCard.search([
                ('sale_line', '=', sale_line1.id)
                ])

            invoice, = Invoice.search([])
            line, = InvoiceLine.search([
                ('invoice', '=', invoice.id),
                ('description', '=', 'Gift Card'),
                ])
            self.assertEqual(line.account,
                Configuration(1).liability_account)

            self.assertEqual(gift_card.amount, 500)
            self.assertEqual(gift_card.state, 'active')
            self.assertEqual(gift_card.sale, sale)

            self.assertEqual(invoice.untaxed_amount, 900)
            self.assertEqual(invoice.total_amount, 900)

    @with_transaction()
    def test0050_create_gift_card_for_line(self):
        """
        Check that gift card is not created for sale lines of type line
        """
        pool = Pool()
        GiftCard = pool.get('gift_card.gift_card')
        SaleConfiguration = pool.get('sale.configuration')
        AccountConfiguration = pool.get('account.configuration')
        SaleLine = pool.get('sale.line')
        Company = pool.get('company.company')
        Account = pool.get('account.account')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            revenue, = Account.search([
                    ('type.revenue', '=', True),
                    ])
            account_config = AccountConfiguration(1)
            account_config.default_category_account_revenue = revenue
            account_config.save()

            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()

            sale = create_sale(amount=200)
            sale.invoice_method = 'shipment'
            sale.shipment_method = 'order'
            sale.save()

            self.assertTrue(len(sale.lines), 1)
            sale_line = sale.lines[0]

            self.assertFalse(
                GiftCard.search([('sale_line', '=', sale_line.id)]))

            sale_line.create_gift_cards()

            # No gift card is created
            self.assertFalse(
                GiftCard.search([('sale_line', '=', sale_line.id)]))

            sale_line2, = SaleLine.copy([sale_line])
            self.assertFalse(sale_line2.gift_cards)

    @with_transaction()
    def test0060_gift_card_on_processing_sale_without_liability_account(self):
        """
        Check if gift card is being created on processing sale when liability
        account is missing from gift card configuration
        """
        pool = Pool()
        Sale = pool.get('sale.sale')
        GiftCard = pool.get('gift_card.gift_card')
        Invoice = pool.get('account.invoice')
        SaleConfiguration = pool.get('sale.configuration')
        AccountConfiguration = pool.get('account.configuration')
        SaleLine = pool.get('sale.line')
        Company = pool.get('company.company')
        Uom = pool.get('product.uom')
        Account = pool.get('account.account')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card(set_configuration_account=False)

        gift_card_product = create_product(type='service',
            is_gift_card=True)

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            revenue, = Account.search([
                    ('type.revenue', '=', True),
                    ])
            account_config = AccountConfiguration(1)
            account_config.default_category_account_revenue = revenue
            account_config.save()

            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()

            sale = create_sale(amount=400)
            sale.invoice_method = 'shipment'
            sale.shipment_method = 'order'
            sale.save()

            gc_price, _, = gift_card_product.gift_card_prices
            uom, = Uom.search([('name', '=', 'Unit')])
            gift_card_line = SaleLine()
            gift_card_line.sale = sale
            gift_card_line.quantity = 1
            gift_card_line.unit_price = 500
            gift_card_line.unit = uom
            gift_card_line.description = 'Gift Card'
            gift_card_line.product = gift_card_product
            gift_card_line.gc_price = gc_price
            gift_card_line.save()
            comment_line = SaleLine()
            comment_line.sale = sale
            comment_line.type = 'comment'
            comment_line.description = 'Test comment'
            comment_line.save()

            sale_line1, = SaleLine.search([
                    ('sale', '=', sale.id),
                    ('product', '=', gift_card_product.id),
                    ])
            self.assertTrue(sale_line1.is_gift_card)

            sale_line2, = SaleLine.search([
                    ('sale', '=', sale.id),
                    ('type', '=', 'line'),
                    ('id', '!=', sale_line1.id),
                    ])
            self.assertFalse(sale_line2.is_gift_card)

            sale_line3, = SaleLine.search([
                    ('sale', '=', sale.id),
                    ('type', '=', 'comment'),
                    ])
            self.assertFalse(sale_line3.is_gift_card)

            self.assertEqual(sale_line1.gift_card_delivery_mode, 'physical')

            # Gift card line amount is included in untaxed amount
            self.assertEqual(sale.untaxed_amount, 900)

            # Gift card line amount is included in total amount
            self.assertEqual(sale.total_amount, 900)

            Sale.quote([sale])

            self.assertEqual(sale.untaxed_amount, 900)
            self.assertEqual(sale.total_amount, 900)

            Sale.confirm([sale])

            self.assertEqual(sale.untaxed_amount, 900)
            self.assertEqual(sale.total_amount, 900)
            self.assertFalse(
                GiftCard.search([('sale_line', '=', sale_line1.id)]))
            self.assertFalse(Invoice.search([]))
            with self.assertRaises(UserError):
                Sale.process([sale])

    @with_transaction()
    def test0100_authorize_gift_card_payment_gateway_valid_card(self):
        """
        Test gift card authorization
        """
        pool = Pool()
        GiftCard = pool.get('gift_card.gift_card')
        SaleConfiguration = pool.get('sale.configuration')
        Company = pool.get('company.company')
        PaymentTransaction = pool.get('payment_gateway.transaction')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            active_gift_card, = GiftCard.create([{
                'amount': Decimal('150'),
                'number': '45671338',
                'state': 'active',
                }])

            gateway = create_payment_gateway(method='gift_card',
                provider='manual')
            # Create a random sale to setup defaults
            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()
            sale = create_sale()

            party = sale.party
            # Case 1:
            # Gift card available amount (150) > amount to be paid (50)
            payment_transaction = PaymentTransaction(
                description="Pay invoice using gift card",
                party=party,
                address=party.addresses[0],
                amount=Decimal('50'),
                currency=company.currency,
                gateway=gateway,
                gift_card=active_gift_card,
                credit_account=party.account_receivable,
                )
            payment_transaction.save()

            PaymentTransaction.authorize([payment_transaction])

            self.assertEqual(payment_transaction.state, 'authorized')

            self.assertEqual(
                active_gift_card.amount_authorized, Decimal('50'))

            self.assertEqual(
                active_gift_card.amount_available, Decimal('100'))

            # Case 2: Gift card amount (100) < amount to be paid (300)
            payment_transaction = PaymentTransaction(
                description="Pay invoice using gift card",
                party=party,
                address=party.addresses[0],
                amount=Decimal('300'),
                currency=company.currency,
                gateway=gateway,
                gift_card=active_gift_card,
                credit_account=party.account_receivable,
                )
            payment_transaction.save()

            with self.assertRaises(UserError):
                PaymentTransaction.authorize([payment_transaction])

    @with_transaction()
    def test0110_capture_gift_card(self):
        """
        Test capturing of gift card
        """
        pool = Pool()
        GiftCard = pool.get('gift_card.gift_card')
        SaleConfiguration = pool.get('sale.configuration')
        Company = pool.get('company.company')
        PaymentTransaction = pool.get('payment_gateway.transaction')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            active_gift_card, = GiftCard.create([{
                'amount': Decimal('200'),
                'number': '45671338',
                'state': 'active',
                }])
            self.assertEqual(
                active_gift_card.amount_captured, Decimal('0'))

            self.assertEqual(
                active_gift_card.amount_authorized, Decimal('0'))

            self.assertEqual(
                active_gift_card.amount_available, Decimal('200'))

            gateway = create_payment_gateway(method='gift_card',
                provider='manual')
            # Create a random sale to setup defaults
            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()
            sale = create_sale()

            party = sale.party
            # Capture
            # Case 1
            # Gift card available amount(200) > amount to be paid (180)
            payment_transaction = PaymentTransaction(
                description="Pay invoice using gift card",
                party=party,
                address=party.addresses[0],
                amount=Decimal('100'),
                currency=company.currency,
                gateway=gateway,
                gift_card=active_gift_card,
                credit_account=party.account_receivable,
                )
            payment_transaction.save()

            PaymentTransaction.capture([payment_transaction])

            self.assertEqual(payment_transaction.state, 'posted')

            self.assertEqual(
                active_gift_card.amount_captured, Decimal('100')
            )
            self.assertEqual(
                active_gift_card.amount_authorized, Decimal('0')
            )

            # 200 - 100 = 100
            self.assertEqual(
                active_gift_card.amount_available, Decimal('100')
            )

            # Case 2
            # Gift card available amount (100) = amount to be paid (100)
            payment_transaction = PaymentTransaction(
                description="Pay invoice using gift card",
                party=party,
                address=party.addresses[0],
                amount=Decimal('100'),
                currency=company.currency,
                gateway=gateway,
                gift_card=active_gift_card,
                credit_account=party.account_receivable,
                )
            payment_transaction.save()

            PaymentTransaction.capture([payment_transaction])

            self.assertEqual(payment_transaction.state, 'posted')
            self.assertEqual(
                active_gift_card.amount_captured, Decimal('200')
            )
            self.assertEqual(
                active_gift_card.amount_authorized, Decimal('0')
            )

            # 200 - 200 = 0
            self.assertEqual(
                active_gift_card.amount_available, Decimal('0')
            )
            self.assertEqual(active_gift_card.state, 'used')

            # Case 3: Gift card amount (10) < amount to be paid (100)
            active_gift_card, = GiftCard.create([{
                'amount': Decimal('10'),
                'number': '45671339',
                'state': 'active',
            }])

            payment_transaction = PaymentTransaction(
                description="Pay invoice using gift card",
                party=party,
                address=party.addresses[0],
                amount=Decimal('100'),
                currency=company.currency,
                gateway=gateway,
                gift_card=active_gift_card,
                credit_account=party.account_receivable,
                )
            payment_transaction.save()

            with self.assertRaises(UserError):
                PaymentTransaction.capture([payment_transaction])

    @with_transaction()
    def test0120_settle_gift_card(self):
        """
        Test settlement of gift card
        """
        pool = Pool()
        GiftCard = pool.get('gift_card.gift_card')
        SaleConfiguration = pool.get('sale.configuration')
        Company = pool.get('company.company')
        PaymentTransaction = pool.get('payment_gateway.transaction')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            active_gift_card, = GiftCard.create([{
                'amount': Decimal('200'),
                'number': '45671338',
                'state': 'active',
                }])
            self.assertEqual(
                active_gift_card.amount_captured, Decimal('0'))

            self.assertEqual(
                active_gift_card.amount_authorized, Decimal('0'))

            self.assertEqual(
                active_gift_card.amount_available, Decimal('200'))

            gateway = create_payment_gateway(method='gift_card',
                provider='manual')
            # Create a random sale to setup defaults
            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()
            sale = create_sale()

            party = sale.party
            # Capture
            # Case 1
            # Gift card available amount(200) > amount to be paid (180)
            payment_transaction = PaymentTransaction(
                description="Pay using gift card",
                party=party,
                address=party.addresses[0],
                amount=Decimal('100'),
                currency=company.currency,
                gateway=gateway,
                gift_card=active_gift_card,
                credit_account=party.account_receivable,
                )
            payment_transaction.save()

            PaymentTransaction.authorize([payment_transaction])

            self.assertEqual(
                active_gift_card.amount_captured, Decimal('0'))

            self.assertEqual(
                active_gift_card.amount_authorized, Decimal('100'))

            # 200 - 100 = 100
            self.assertEqual(
                active_gift_card.amount_available, Decimal('100'))

            # Settlement
            # Case 1: Gift card amount (100) > amount to be settled (50)
            payment_transaction = PaymentTransaction(
                description="Pay using gift card",
                party=party,
                address=party.addresses[0],
                amount=Decimal('50'),
                currency=company.currency,
                gateway=gateway,
                gift_card=active_gift_card,
                credit_account=party.account_receivable,
                )
            payment_transaction.save()

            PaymentTransaction.authorize([payment_transaction])

            self.assertEqual(
                active_gift_card.amount_captured, Decimal('0'))
            self.assertEqual(
                active_gift_card.amount_authorized, Decimal('150'))
            # 100 - 50 = 50
            self.assertEqual(
                active_gift_card.amount_available, Decimal('50'))

            PaymentTransaction.settle([payment_transaction])

            self.assertEqual(payment_transaction.state, 'posted')
            self.assertEqual(
                active_gift_card.amount_captured, Decimal('50'))
            self.assertEqual(
                active_gift_card.amount_authorized, Decimal('100'))
            # 200 - 100 - 50 = 50
            self.assertEqual(
                active_gift_card.amount_available, Decimal('50'))

    @with_transaction()
    def test0150_payment_gateway_methods_and_providers(self):
        """
        Tests gateway methods
        """
        pool = Pool()
        Company = pool.get('company.company')
        PaymentGateway = pool.get('payment_gateway.gateway')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            gateway = create_payment_gateway(method='gift_card',
                provider='manual')
        self.assertTrue(gateway.get_methods())
        self.assertTrue(('gift_card', 'Gift Card') in gateway.get_methods())

        gateway = PaymentGateway(provider='authorize.net')
        self.assertFalse(gateway.get_methods())

    @with_transaction()
    def test0160_gift_card_amount(self):
        """
        Check authorized, captured and available amount for a gift card
        """
        pool = Pool()
        GiftCard = pool.get('gift_card.gift_card')
        SaleConfiguration = pool.get('sale.configuration')
        Company = pool.get('company.company')
        PaymentTransaction = pool.get('payment_gateway.transaction')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            active_gift_card, = GiftCard.create([{
                'amount': Decimal('200'),
                'number': '45671338',
                'state': 'active',
                }])
            self.assertEqual(
                active_gift_card.amount_captured, Decimal('0'))

            self.assertEqual(
                active_gift_card.amount_authorized, Decimal('0'))

            self.assertEqual(
                active_gift_card.amount_available, Decimal('200'))

            gateway = create_payment_gateway(method='gift_card',
                provider='manual')
            # Create a random sale to setup defaults
            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()
            sale = create_sale()

            party = sale.party
            # Payment transactions in authorized state
            payment_transaction1 = PaymentTransaction(
                description="Payment 1",
                party=party,
                address=party.addresses[0],
                amount=Decimal('70'),
                currency=company.currency,
                gateway=gateway,
                gift_card=active_gift_card,
                credit_account=party.account_receivable,
                )
            payment_transaction1.save()
            PaymentTransaction.authorize([payment_transaction1])

            payment_transaction2 = PaymentTransaction(
                description="Payment 2",
                party=party,
                address=party.addresses[0],
                amount=Decimal('20'),
                currency=company.currency,
                gateway=gateway,
                gift_card=active_gift_card,
                credit_account=party.account_receivable,
                )
            payment_transaction2.save()
            PaymentTransaction.authorize([payment_transaction2])

            # Payment transactions being captured
            payment_transaction3 = PaymentTransaction(
                description="Payment 3",
                party=party,
                address=party.addresses[0],
                amount=Decimal('10'),
                currency=company.currency,
                gateway=gateway,
                gift_card=active_gift_card,
                credit_account=party.account_receivable,
                )
            payment_transaction3.save()
            PaymentTransaction.capture([payment_transaction3])

            payment_transaction4 = PaymentTransaction(
                description="Payment 4",
                party=party,
                address=party.addresses[0],
                amount=Decimal('20'),
                currency=company.currency,
                gateway=gateway,
                gift_card=active_gift_card,
                credit_account=party.account_receivable,
                )
            payment_transaction4.save()
            PaymentTransaction.capture([payment_transaction4])

        self.assertEqual(active_gift_card.amount_authorized, 90)
        self.assertEqual(active_gift_card.amount_captured, 30)
        self.assertEqual(active_gift_card.amount_available, 80)

    @with_transaction()
    def test0200_test_gift_card_report(self):
        """
        Test Gift Card report
        """
        pool = Pool()
        Company = pool.get('company.company')
        GiftCard = pool.get('gift_card.gift_card')
        GiftCardReport = pool.get('gift_card.gift_card', type='report')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            active_gift_card, = GiftCard.create([{
                'amount': Decimal('200'),
                'number': '45671338',
                'state': 'active',
                }])

            val = GiftCardReport.execute([gift_card.id], {})

            self.assertTrue(val)
            # Assert report name
            self.assertEqual(val[3], 'Gift Card')

    @with_transaction()
    def test0210_test_gift_card_deletion(self):
        """
        Test that Gift Card can not be deleted in active state
        """
        pool = Pool()
        Company = pool.get('company.company')
        GiftCard = pool.get('gift_card.gift_card')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            active_gift_card, = GiftCard.create([{
                'amount': Decimal('200'),
                'number': '45671338',
                'state': 'active',
                }])

            with self.assertRaises(UserError):
                GiftCard.delete([active_gift_card])

            # Try to delete gift card in state draft and it will
            # be deleted
            gift_card, = GiftCard.create([{
                'amount': Decimal('200'),
                'number': '45671339',
                'state': 'draft',
            }])

            GiftCard.delete([gift_card])

    @with_transaction()
    def test0300_send_virtual_gift_card(self):
        """
        Check if virtual gift cards are sent through email
        """
        pool = Pool()
        Sale = pool.get('sale.sale')
        GiftCard = pool.get('gift_card.gift_card')
        Invoice = pool.get('account.invoice')
        SaleConfiguration = pool.get('sale.configuration')
        AccountConfiguration = pool.get('account.configuration')
        SaleLine = pool.get('sale.line')
        Company = pool.get('company.company')
        Uom = pool.get('product.uom')
        SalePayment = pool.get('sale.payment')
        Account = pool.get('account.account')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        gift_card_product = create_product(type='service',
            mode='virtual', is_gift_card=True)

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            revenue, = Account.search([
                    ('type.revenue', '=', True),
                    ])
            account_config = AccountConfiguration(1)
            account_config.default_category_account_revenue = revenue
            account_config.save()

            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()

            sale = create_sale(amount=400)
            sale.invoice_method = 'order'
            sale.save()

            gc_price, _, = gift_card_product.gift_card_prices
            uom, = Uom.search([('name', '=', 'Unit')])
            gift_card_line = SaleLine()
            gift_card_line.sale = sale
            gift_card_line.quantity = 1
            gift_card_line.unit_price = 500
            gift_card_line.unit = uom
            gift_card_line.description = 'Gift Card'
            gift_card_line.product = gift_card_product
            gift_card_line.gc_price = gc_price
            gift_card_line.recipient_email = 'test@gift_card.com'
            gift_card_line.recipient_name = 'John Doe'
            gift_card_line.save()
            comment_line = SaleLine()
            comment_line.sale = sale
            comment_line.type = 'comment'
            comment_line.description = 'Test comment'
            comment_line.save()

            gift_card_line, = SaleLine.search([
                ('sale', '=', sale.id),
                ('product', '=', gift_card_product.id),
            ])

            self.assertEqual(
                gift_card_line.gift_card_delivery_mode, 'virtual'
            )

            Sale.quote([sale])

            with patch.object(
                gift_card_module, 'sendmail_transactional') as sendmail, \
                    patch.object(gift_card_module, 'SMTPDataManager') as dm:

                Sale.confirm([sale])

                # No gift card yet
                self.assertFalse(
                    GiftCard.search([('sale_line', '=', gift_card_line.id)])
                )
                # No Email is being sent yet
                sendmail.assert_not_called()

                SalePayment.create([{
                    'sale': sale,
                    'amount': Decimal('1000'),
                    'gateway': create_payment_gateway(),
                    'credit_account': sale.party.account_receivable,
                    }])

                Sale.process([sale])

                # Gift card is created
                self.assertTrue(
                    GiftCard.search([('sale_line', '=', gift_card_line.id)]))
                self.assertEqual(
                    GiftCard.search(
                        [('sale_line', '=', gift_card_line.id)], count=True
                    ), 1)
                self.assertEqual(Invoice.search([], count=True), 1)

                gift_card, = GiftCard.search([
                    ('sale_line', '=', gift_card_line.id)
                    ])
                self.assertEqual(
                    gift_card.recipient_email, gift_card_line.recipient_email)

                self.assertEqual(
                    gift_card.recipient_name, gift_card_line.recipient_name)

                # Email was sent
                sendmail.assert_called_once()

    @with_transaction()
    def test0310_test_send_email_only_once(self):
        """
        Test that email is not sent more than once for gift card
        """
        pool = Pool()
        GiftCard = pool.get('gift_card.gift_card')
        SaleConfiguration = pool.get('sale.configuration')
        AccountConfiguration = pool.get('account.configuration')
        SaleLine = pool.get('sale.line')
        Company = pool.get('company.company')
        Uom = pool.get('product.uom')
        Account = pool.get('account.account')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        gift_card_product = create_product(type='service',
            mode='virtual', is_gift_card=True)

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):
            revenue, = Account.search([
                    ('type.revenue', '=', True),
                    ])
            account_config = AccountConfiguration(1)
            account_config.default_category_account_revenue = revenue
            account_config.save()

            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()

            sale = create_sale(amount=400)
            sale.invoice_method = 'order'
            sale.save()

            gc_price, _, = gift_card_product.gift_card_prices
            uom, = Uom.search([('name', '=', 'Unit')])
            gift_card_line = SaleLine()
            gift_card_line.sale = sale
            gift_card_line.quantity = 1
            gift_card_line.unit_price = 500
            gift_card_line.unit = uom
            gift_card_line.description = 'Gift Card'
            gift_card_line.product = gift_card_product
            gift_card_line.gc_price = gc_price
            gift_card_line.recipient_email = 'test@gift_card.com'
            gift_card_line.recipient_name = 'John Doe'
            gift_card_line.save()
            comment_line = SaleLine()
            comment_line.sale = sale
            comment_line.type = 'comment'
            comment_line.description = 'Test comment'
            comment_line.save()

            gift_card_line, = SaleLine.search([
                ('sale', '=', sale.id),
                ('product', '=', gift_card_product.id),
            ])

            with patch.object(
                gift_card_module, 'sendmail_transactional') as sendmail, \
                    patch.object(gift_card_module, 'SMTPDataManager') as dm:

                gift_card, = GiftCard.create([{
                    'sale_line': gift_card_line,
                    'amount': Decimal('200'),
                    'number': '45671338',
                    'recipient_email': 'test@gift_card.com',
                    'recipient_name': 'Jhon Doe',
                    }])


                self.assertFalse(gift_card.is_email_sent)

                # No Email is being sent yet
                sendmail.assert_not_called()

                # Send email by activating gift card
                GiftCard.activate([gift_card])

                # Email is being sent
                sendmail.assert_called_once()
                self.assertTrue(gift_card.is_email_sent)

                # Try sending email again
                GiftCard.activate([gift_card])

                # Email was only sent once
                sendmail.assert_called_once()

                # Set to Draft and activate again
                GiftCard.draft([gift_card])
                GiftCard.activate([gift_card])

                # Email was only sent once
                sendmail.assert_called_once()

    @with_transaction()
    def test0400_validate_product_type(self):
        """
        Check if gift card product is service product
        """
        pool = Pool()
        Company = pool.get('company.company')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):

            # Create gift card product of goods type in virtual mode
            with self.assertRaises(UserError):
                create_product(
                    type='goods', mode='virtual', is_gift_card=True
                )

            # Product can be created with service type only
            service_product = create_product(
                type='service', mode='virtual', is_gift_card=True
            )

            self.assertTrue(service_product)

    @with_transaction()
    def test410_test_gc_min_max(self):
        """
        Test gift card minimum and maximum amounts on product template
        """
        pool = Pool()
        Company = pool.get('company.company')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        gift_card_product = create_product(
            type='service', mode='virtual', is_gift_card=True
        )

        gift_card_product.allow_open_amount = True

        company, = Company.search([])
        with Transaction().set_context({'company': company.id}):

            # gc_min > gc_max
            gift_card_product.gc_min = Decimal('70')
            gift_card_product.gc_max = Decimal('60')

            with self.assertRaises(UserError):
                gift_card_product.save()

            # gc_min as negative
            gift_card_product.gc_min = Decimal('-10')
            gift_card_product.gc_max = Decimal('60')

            with self.assertRaises(UserError):
                gift_card_product.save()

            # gc_max as negative
            gift_card_product.gc_min = Decimal('10')
            gift_card_product.gc_max = Decimal('-80')

            with self.assertRaises(UserError):
                gift_card_product.save()

            # gc_min < gc_max
            gift_card_product.gc_min = Decimal('70')
            gift_card_product.gc_max = Decimal('100')

            gift_card_product.save()

    @with_transaction()
    def test0420_validate_gc_amount_on_sale_line(self):
        """
        Tests if gift card line amount lies between gc_min and gc_max defined
        on the template
        """
        pool = Pool()
        Sale = pool.get('sale.sale')
        SaleConfiguration = pool.get('sale.configuration')
        AccountConfiguration = pool.get('account.configuration')
        SaleLine = pool.get('sale.line')
        Company = pool.get('company.company')
        Uom = pool.get('product.uom')
        SalePayment = pool.get('sale.payment')
        Account = pool.get('account.account')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        gift_card_product = create_product(type='service',
            mode='physical', is_gift_card=True)

        gift_card_product.allow_open_amount = True
        gift_card_product.gc_min = Decimal('100')
        gift_card_product.gc_max = Decimal('500')
        gift_card_product.save()

        company, = Company.search([])
        with Transaction().set_context(company=company.id, language='en'):
            revenue, = Account.search([
                    ('type.revenue', '=', True),
                    ])
            account_config = AccountConfiguration(1)
            account_config.default_category_account_revenue = revenue
            account_config.save()

            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()

            uom, = Uom.search([('name', '=', 'Unit')])
            # gift card line amount < gc_min
            sale = create_sale(amount=400)
            sale.invoice_method = 'order'
            sale.save()

            gift_card_line = SaleLine()
            gift_card_line.sale = sale
            gift_card_line.quantity = 1
            gift_card_line.unit_price = 50
            gift_card_line.unit = uom
            gift_card_line.description = 'Gift Card'
            gift_card_line.product = gift_card_product
            gift_card_line.save()
            comment_line = SaleLine()
            comment_line.sale = sale
            comment_line.type = 'comment'
            comment_line.description = 'Test comment'
            comment_line.save()

            Sale.quote([sale])
            Sale.confirm([sale])

            with self.assertRaises(UserError):
                Sale.process([sale])

            # gift card line amount > gc_max
            sale = create_sale(amount=400)
            sale.invoice_method = 'order'
            sale.save()

            gift_card_line = SaleLine()
            gift_card_line.sale = sale
            gift_card_line.quantity = 10
            gift_card_line.unit_price = 700
            gift_card_line.unit = uom
            gift_card_line.description = 'Gift Card'
            gift_card_line.product = gift_card_product
            gift_card_line.save()
            comment_line = SaleLine()
            comment_line.sale = sale
            comment_line.type = 'comment'
            comment_line.description = 'Test comment'
            comment_line.save()

            Sale.quote([sale])
            Sale.confirm([sale])

            with self.assertRaises(UserError):
                Sale.process([sale])

            # gc_min <= gift card line amount <= gc_max
            sale = create_sale(amount=400)
            sale.invoice_method = 'order'
            sale.save()

            gift_card_line = SaleLine()
            gift_card_line.sale = sale
            gift_card_line.quantity = 3
            gift_card_line.unit_price = 500
            gift_card_line.unit = uom
            gift_card_line.description = 'Gift Card'
            gift_card_line.product = gift_card_product
            gift_card_line.save()
            comment_line = SaleLine()
            comment_line.sale = sale
            comment_line.type = 'comment'
            comment_line.description = 'Test comment'
            comment_line.save()

            Sale.quote([sale])
            Sale.confirm([sale])

            gift_card_line, = SaleLine.search([
                ('sale', '=', sale.id),
                ('product', '=', gift_card_product.id),
                ])

            Sale.quote([sale])
            Sale.confirm([sale])

            self.assertEqual(len(gift_card_line.gift_cards), 0)

            SalePayment.create([{
                'sale': sale,
                'amount': sale.total_amount,
                'gateway': create_payment_gateway(),
                'credit_account': sale.party.account_receivable.id,
                }])

            Sale.process([sale])

            self.assertEqual(sale.state, 'processing')
            self.assertEqual(len(gift_card_line.gift_cards), 3)

    @with_transaction()
    def test0430_test_gift_card_prices(self):
        """
        Test gift card price
        """
        pool = Pool()
        GiftCardPrice = pool.get('product.product.gift_card.price')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        gift_card_product = create_product(type='service',
            mode='virtual', is_gift_card=True)

        with self.assertRaises(UserError):
            GiftCardPrice.create([{
                'product': gift_card_product,
                'price': -90
            }])

        price, = GiftCardPrice.create([{
            'product': gift_card_product,
            'price': 90
        }])

        self.assertTrue(price)

    @with_transaction()
    def test0440_test_on_change_gc_price(self):
        """
        Tests if unit price is changed with gift card price
        """
        pool = Pool()
        SaleLine = pool.get('sale.line')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        gift_card_product = create_product(type='service',
            mode='virtual', is_gift_card=True)

        gc_price, _, = gift_card_product.gift_card_prices

        sale_line = SaleLine(gc_price=gc_price)

        sale_line_ = sale_line.on_change_gc_price()

        self.assertEqual(sale_line_.unit_price, gc_price.price)

    @with_transaction()
    def test0500_pay_with_manual_gateway(self):
        """
        Check authorized, captured and available amount for manual method
        """
        pool = Pool()
        GiftCard = pool.get('gift_card.gift_card')
        SaleConfiguration = pool.get('sale.configuration')
        Company = pool.get('company.company')
        PaymentTransaction = pool.get('payment_gateway.transaction')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()
        gift_card.amount = 200
        gift_card.save()
        GiftCard.activate([gift_card])

        company, = Company.search([])
        with Transaction().set_context(company=company.id, language='en'):
            gateway = create_payment_gateway(method='gift_card',
                provider='manual')
            # Create a random sale to setup defaults
            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()
            sale = create_sale()

            party = sale.party
            # Authorise Payment transaction
            payment_transaction = PaymentTransaction(
                description="Payment 1",
                party=party,
                address=party.addresses[0],
                amount=Decimal('70'),
                currency=company.currency,
                gateway=gateway,
                gift_card=gift_card,
                credit_account=party.account_receivable,
                )
            payment_transaction.save()
            PaymentTransaction.authorize([payment_transaction])
            self.assertEqual(payment_transaction.state, 'authorized')

            # Settle Payment transactions
            PaymentTransaction.settle([payment_transaction])
            self.assertEqual(payment_transaction.state, 'posted')

            # Capture Payment transactions
            payment_transaction = PaymentTransaction(
                description="Payment 1",
                party=party,
                address=party.addresses[0],
                amount=Decimal('70'),
                currency=company.currency,
                gateway=gateway,
                gift_card=gift_card,
                credit_account=party.account_receivable,
                )
            payment_transaction.save()
            PaymentTransaction.capture([payment_transaction])
            self.assertEqual(payment_transaction.state, 'posted')

    @with_transaction()
    def test0510_giftcard_redeem_wizard(self):
        """
        Tests the gift card redeem wizard.
        """
        pool = Pool()
        GiftCard = pool.get('gift_card.gift_card')
        SaleConfiguration = pool.get('sale.configuration')
        Company = pool.get('company.company')
        GCRedeemWizard = pool.get('gift_card.redeem.wizard', type='wizard')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()
        gift_card.amount = 150
        gift_card.save()

        company, = Company.search([])
        with Transaction().set_context(company=company.id, language='en'):
            gateway = create_payment_gateway(method='gift_card',
                provider='manual')
            # Create a random sale to setup defaults
            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()
            sale = create_sale()

            party = sale.party
            with Transaction().set_context(active_ids=[gift_card.id]):
                session_id, start_state, end_state = GCRedeemWizard.create()
                data = {
                    start_state: {
                        'name': 'start',
                        'gateway': gateway,
                        'description': 'This is a description.',
                        'party': party,
                        'address': party.addresses[0],
                        'amount': Decimal('100'),
                        'gift_card': gift_card,
                        'currency': sale.currency,
                        },
                    }

                # Trying to redeem GC in draft state, error is thrown.
                # Note that a domain error is thrown instead of
                # check_giftcard_state() being called.
                with self.assertRaises(UserError):
                    GCRedeemWizard.execute(session_id, data, 'redeem')

                # Test check_giftcard_state(). Draft state error is thrown.
                with self.assertRaises(UserError):
                    GCRedeemWizard(session_id).check_giftcard_state(
                        gift_card)

                GiftCard.activate([gift_card])

                # Test the default_start() method.
                values = GCRedeemWizard(session_id).default_start({})
                self.assertEqual(values['gift_card'], gift_card.id)
                self.assertEqual(values['gateway'], gateway.id)

                # Now execute the wizard properly.
                GCRedeemWizard.execute(session_id, data, 'redeem')
                self.assertEqual(gift_card.state, 'active')
                self.assertEqual(
                    gift_card.amount_captured,
                    data[start_state]['amount']
                    )

                data[start_state]['amount'] = Decimal('70')

                # Error thrown because amount available is just 50.
                with self.assertRaises(UserError):
                    GCRedeemWizard.execute(session_id, data, 'redeem')

                data[start_state]['amount'] = Decimal('-70')

                # Error thrown because amount is negative.
                with self.assertRaises(UserError):
                    GCRedeemWizard.execute(session_id, data, 'redeem')

                data[start_state]['amount'] = Decimal('50')
                GCRedeemWizard.execute(session_id, data, 'redeem')
                self.assertEqual(gift_card.state, 'used')
                self.assertEqual(
                    gift_card.amount_available, Decimal('0'))

                # Now the gift card has already been used, cannot run
                # wizard on it once again.
                with self.assertRaises(UserError):
                    GCRedeemWizard(session_id).check_giftcard_state(
                        gift_card)

    @with_transaction()
    def test0520_test_sale_payment_wizard_for_gift_card(self):
        """
        Test the wizard to create sale payment for gift card
        """
        pool = Pool()
        GiftCard = pool.get('gift_card.gift_card')
        SaleConfiguration = pool.get('sale.configuration')
        SaleLine = pool.get('sale.line')
        Company = pool.get('company.company')
        Uom = pool.get('product.uom')
        PaymentWizard = pool.get('sale.payment.add', type="wizard")

        # Active gift card
        gift_card = create_gift_card()
        gift_card.amount = 100
        gift_card.save()
        GiftCard.activate([gift_card])

        company, = Company.search([])
        # Inactive gift card
        inactive_gift_card, = GiftCard.create([{
            'number': 'A1567',
            'amount': Decimal('50'),
            'currency': company.currency,
            'state': 'used'
            }])

        gift_card_product = create_product(type='service',
            mode='physical', is_gift_card=True)

        with Transaction().set_context(company=company.id, language='en'):
            gateway = create_payment_gateway(method='gift_card',
                provider='manual')
            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()
            sale = create_sale(amount=500)
            sale.invoice_method = 'order'
            sale.save()

            uom, = Uom.search([('name', '=', 'Unit')])
            gc_price, _, = gift_card_product.gift_card_prices
            gift_card_line = SaleLine()
            gift_card_line.sale = sale
            gift_card_line.quantity = 3
            gift_card_line.unit_price = 500
            gift_card_line.unit = uom
            gift_card_line.description = 'Gift Card'
            gift_card_line.product = gift_card_product
            gift_card_line.gc_price = gc_price
            gift_card_line.save()

            payment_wizard = PaymentWizard(PaymentWizard.create()[0])
            payment_wizard.payment_info.gateway = gateway
            payment_wizard.payment_info.method = gateway.method
            payment_wizard.payment_info.amount = 200
            payment_wizard.payment_info.payment_profile = None
            payment_wizard.payment_info.party = sale.party
            payment_wizard.payment_info.sale = sale
            payment_wizard.payment_info.reference = 'ref1'
            payment_wizard.payment_info.credit_account = \
                sale.party.account_receivable

            payment_wizard.payment_info.gift_card = gift_card
            payment_wizard.payment_info.amount = 50
            self.assertEqual(gift_card.amount_available, Decimal('100'))
            with Transaction().set_context(active_id=sale.id):
                payment_wizard.transition_add()

            self.assertTrue(len(sale.payments), 1)

            payment, = sale.payments
            self.assertEqual(payment.amount, Decimal('50'))
            self.assertEqual(payment.method, gateway.method)
            self.assertEqual(payment.provider, gateway.provider)
            self.assertEqual(payment.gift_card, gift_card)

    @with_transaction()
    def test0530_partial_payment_using_gift_card(self):
        """
        Check partial payment using cash, credit card and gift card
        """
        pool = Pool()
        Sale = pool.get('sale.sale')
        GiftCard = pool.get('gift_card.gift_card')
        SaleConfiguration = pool.get('sale.configuration')
        Company = pool.get('company.company')
        SalePayment = pool.get('sale.payment')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()
        gift_card.amount = 200
        gift_card.save()
        GiftCard.activate([gift_card])

        company, = Company.search([])
        with Transaction().set_context(company=company.id, language='en'):
            gateway = create_payment_gateway(method='gift_card',
                provider='manual')
            # Create a random sale to setup defaults
            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'sale_confirm'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()
            sale = create_sale(amount=100)
            #sale.invoice_method = 'order'
            sale.invoice_method = 'manual'
            sale.shipment_method = 'manual'
            sale.save()

            party = sale.party
            with Transaction().set_context(use_dummy=True, language='en'):
                # Create gateways
                dummy_gateway = create_payment_gateway(
                    method='dummy', provider='dummy')
                cash_gateway = create_payment_gateway(
                    method='manual', provider='manual')
                gift_card_gateway = create_payment_gateway(
                    method='gift_card', provider='manual')

                # Create a payment profile
                payment_profile = create_payment_profile(
                    party, dummy_gateway)

                # Create sale payment for $30 in cash and $50 in card and $20
                # in gift card
                payment_gift_card, payment_cash, payment_credit_card = \
                    SalePayment.create([{
                        'sale': sale,
                        'amount': Decimal('20'),
                        'gateway': gift_card_gateway,
                        'gift_card': gift_card,
                        'credit_account': party.account_receivable,
                    }, {
                        'sale': sale,
                        'amount': Decimal('30'),
                        'gateway': cash_gateway,
                        'credit_account': party.account_receivable,
                    }, {
                        'sale': sale,
                        'amount': Decimal('50'),
                        'payment_profile': payment_profile,
                        'gateway': dummy_gateway,
                        'credit_account': party.account_receivable,
                    }])

        self.assertTrue(
            payment_credit_card.description.startswith("Paid by Card"))
        self.assertTrue(
            payment_cash.description.startswith("Paid by Cash"))
        self.assertTrue(
            payment_gift_card.description.startswith("Paid by Gift"))

        self.assertEqual(sale.total_amount, Decimal('100'))
        self.assertEqual(sale.payment_total, Decimal('100'))
        self.assertEqual(sale.payment_available, Decimal('100'))
        self.assertEqual(sale.payment_collected, Decimal('0'))
        self.assertEqual(sale.payment_captured, Decimal('0'))
        self.assertEqual(sale.payment_authorized, Decimal('0'))

        with Transaction().set_context(company=company.id):
            Sale.quote([sale])
            Sale.confirm([sale])
            sale.capture_payments(sale.total_amount)
            Sale.process([sale])
            sale.process_pending_payments()

        self.assertEqual(sale.state, 'done')
        self.assertEqual(len(sale.gateway_transactions), 3)

        self.assertEqual(sale.total_amount, Decimal('100'))
        self.assertEqual(sale.payment_total, Decimal('100'))
        self.assertEqual(sale.payment_available, Decimal('0'))
        self.assertEqual(sale.payment_collected, Decimal('100'))
        self.assertEqual(sale.payment_captured, Decimal('100'))
        self.assertEqual(sale.payment_authorized, Decimal('0'))

    @with_transaction()
    def test0600_gift_card_method(self):
        """
        Check if gift card is being created according to gift card method
        """
        pool = Pool()
        Sale = pool.get('sale.sale')
        GiftCard = pool.get('gift_card.gift_card')
        Invoice = pool.get('account.invoice')
        SaleConfiguration = pool.get('sale.configuration')
        AccountConfiguration = pool.get('account.configuration')
        SaleLine = pool.get('sale.line')
        Company = pool.get('company.company')
        Uom = pool.get('product.uom')
        SalePayment = pool.get('sale.payment')
        Account = pool.get('account.account')
        Journal = pool.get('account.journal')
        PaymentMethod = pool.get('account.invoice.payment.method')

        # Create a random gift card to setup defaults
        gift_card = create_gift_card()

        gift_card_product1 = create_product(is_gift_card=True)
        gift_card_product2 = create_product(is_gift_card=True)

        company, = Company.search([])
        with Transaction().set_context(company=company.id, language='en'):
            gateway = create_payment_gateway(method='manual',
                provider='manual')
            revenue, = Account.search([
                    ('type.revenue', '=', True),
                    ])
            account_config = AccountConfiguration(1)
            account_config.default_category_account_revenue = revenue
            account_config.save()

            sale_config = SaleConfiguration(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()

            sale = create_sale(amount=400)
            sale.invoice_method = 'order'
            sale.save()

            gc_price1, _, = gift_card_product1.gift_card_prices
            gc_price2, _, = gift_card_product2.gift_card_prices
            uom, = Uom.search([('name', '=', 'Unit')])
            gift_card_line = SaleLine()
            gift_card_line.sale = sale
            gift_card_line.quantity = 1
            gift_card_line.unit_price = 500
            gift_card_line.unit = uom
            gift_card_line.description = 'Gift Card 1'
            gift_card_line.product = gift_card_product1
            gift_card_line.gc_price = gc_price1
            gift_card_line.save()
            gift_card_line2 = SaleLine()
            gift_card_line2.sale = sale
            gift_card_line2.quantity = 1
            gift_card_line2.unit_price = 500
            gift_card_line2.unit = uom
            gift_card_line2.description = 'Gift Card 2'
            gift_card_line2.product = gift_card_product2
            gift_card_line2.gc_price = gc_price2
            gift_card_line2.save()
            comment_line = SaleLine()
            comment_line.sale = sale
            comment_line.type = 'comment'
            comment_line.description = 'Test comment'
            comment_line.save()

            gc_price1, _, = gift_card_product1.gift_card_prices
            gc_price2, _, = gift_card_product2.gift_card_prices

            Sale.quote([sale])
            Sale.confirm([sale])

            party = sale.party
            SalePayment.create([{
                'sale': sale,
                'amount': Decimal('1000'),
                'gateway': gateway,
                'credit_account': party.account_receivable,
                }])

            Sale.process([sale])

            # Two giftcards should have been created and activated
            self.assertEqual(
                GiftCard.search([('state', '=', 'active')], count=True),
                2)

            # Trigger sale process again
            Sale.process([sale])

            # No new giftcards should have been created
            self.assertEqual(
                GiftCard.search([('state', '=', 'active')], count=True),
                2)

            # Now re-do sale with invoice payment
            config = SaleConfiguration(1)
            config.gift_card_method = 'invoice'
            config.save()

            sale = create_sale(amount=400)
            sale.invoice_method = 'order'
            sale.save()

            gift_card_line = SaleLine()
            gift_card_line.sale = sale
            gift_card_line.quantity = 1
            gift_card_line.unit_price = 500
            gift_card_line.unit = uom
            gift_card_line.description = 'Gift Card 1'
            gift_card_line.product = gift_card_product1
            gift_card_line.gc_price = gc_price1
            gift_card_line.save()
            gift_card_line2 = SaleLine()
            gift_card_line2.sale = sale
            gift_card_line2.quantity = 1
            gift_card_line2.unit_price = 500
            gift_card_line2.unit = uom
            gift_card_line2.description = 'Gift Card 2'
            gift_card_line2.product = gift_card_product2
            gift_card_line2.gc_price = gc_price2
            gift_card_line2.save()
            comment_line = SaleLine()
            comment_line.sale = sale
            comment_line.type = 'comment'
            comment_line.description = 'Test comment'
            comment_line.save()

            Sale.quote([sale])
            Sale.confirm([sale])

            payment, = SalePayment.create([{
                'sale': sale,
                'amount': Decimal('1000'),
                'gateway': gateway,
                'credit_account': party.account_receivable,
                }])

            Sale.process([sale])

            # No new giftcards
            self.assertEqual(
                GiftCard.search([('state', '=', 'active')], count=True), 2)

            # Post and pay the invoice
            invoice, = sale.invoices
            Invoice.post([invoice])

            with set_company(company):
                account_cash, = Account.search([
                        ('name', '=', 'Main Cash'),
                        ])
                journal_cash, = Journal.search([
                        ('type', '=', 'cash'),
                        ])
            payment_method = PaymentMethod()
            payment_method.name = 'Cash'
            payment_method.journal = journal_cash
            payment_method.credit_account = account_cash
            payment_method.debit_account = account_cash
            payment_method.save()

            invoice.pay_invoice(
                invoice.total_amount,
                payment_method,
                invoice.invoice_date,
                'Payment to make invoice paid - obviously!'
            )
            Invoice.paid([invoice])
            Sale.process([sale])

            # New gift cards
            self.assertEqual(
                GiftCard.search([('state', '=', 'active')], count=True), 4)


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            GiftCardTestCase))
    return suite
