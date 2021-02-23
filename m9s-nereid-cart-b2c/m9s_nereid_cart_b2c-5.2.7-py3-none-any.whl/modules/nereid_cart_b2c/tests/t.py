# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import json
import pycountry

from decimal import Decimal

from trytond.tests.test_tryton import suite as test_suite
from trytond.tests.test_tryton import with_transaction, USER
from trytond.pool import Pool
from trytond.exceptions import UserError
from trytond.transaction import Transaction

from nereid.testing import NereidModuleTestCase
from nereid import current_user, current_website

from trytond.modules.company.tests import create_company, set_company
from trytond.modules.nereid.tests.test_common import (create_website_locale,
    create_static_file)
from trytond.modules.payment_gateway.tests import (create_payment_gateway,
    create_payment_profile)
from trytond.modules.sale_channel.tests import (create_sale_channels,
    create_channel_sale)

from trytond.config import config
config.set('database', 'path', '/tmp')


def create_website(name='localhost', locales=[], default_locale=None):
    """
    Creates the website for testing
    """
    pool = Pool()
    Website = pool.get('nereid.website')
    Party = pool.get('party.party')
    User = pool.get('res.user')
    NereidUser = pool.get('nereid.user')
    Company = pool.get('company.company')
    SaleChannel = pool.get('sale.channel')
    Location = pool.get('stock.location')
    PaymentTerm = pool.get('account.invoice.payment_term')

    websites = Website.search([('name', '=', name)])
    if websites:
        return websites[0]

    companies = Company.search([])
    if companies:
        company = companies[0]
    else:
        company = create_company()

    Transaction().context.update(
        User.get_preferences(context_only=True))
    print(Transaction().context)

    with Transaction().set_context(company=company.id), Transaction().set_user(User.id):
        print(Transaction().context)
    print(User)
    with Transaction().set_user(User):
        print(Transaction().context)
    payment_term = PaymentTerm.create([{
            'name': 'Direct',
            'lines': [('create', [{'type': 'remainder'}])]
            }])

    User.write(
        [User(USER)], {
            'main_company': company.id,
            'company': company.id,
            })
    channel_price_list, user_price_list = create_pricelists()

    with Transaction().set_context(company=company.id):
        channel, = SaleChannel.create([{
            'name': 'Default Channel',
            'price_list': channel_price_list,
            'invoice_method': 'order',
            'shipment_method': 'order',
            'source': 'webshop',
            'create_users': [('add', [USER])],
            'warehouse': warehouse,
            'payment_term': payment_term,
            'company': company.id,
        }])

    User.set_preferences({'current_channel': channel})

    warehouse, = Location.search([
            ('type', '=', 'warehouse'),
            ])
    with Transaction().set_context(company=company.id):
        channel1.price_list = channel_price_list
        channel1.invoice_method = 'order'
        channel1.shipment_method = 'order'
        channel1.source = 'webshop'
        channel1.create_users = [USER]
        channel1.warehouse = warehouse
        channel1.save()

    party1, = Party.create([{
        'name': 'Guest User',
    }])
    party2, = Party.create([{
        'name': 'Registered User 1',
        'sale_price_list': user_price_list,
        'addresses': [('create', [{
            'name': 'Address1',
        }])],
    }])
    party3, = Party.create([{
        'name': 'Registered User 2',
    }])

    guest_user, = NereidUser.create([{
        'party': party1.id,
        'name': 'Guest User',
        'email': 'guest@m9s.biz',
        'password': 'password',
        'company': company.id,
    }])
    registered_user, = NereidUser.create([{
        'party': party2.id,
        'name': 'Registered User',
        'email': 'email@example.com',
        'password': 'password',
        'company': company.id,
    }])
    registered_user2, = NereidUser.create([{
        'party': party3.id,
        'name': 'Registered User 2',
        'email': 'email2@example.com',
        'password': 'password2',
        'company': company.id,
    }])

    if not locales:
        locale = create_website_locale()
        locales = [locale.id]
        default_locale = locale
    else:
        locales = [l for l in locales]

    if default_locale is None:
        default_locale = locales[0]

    website = Website()
    website.name = name
    website.company = company
    website.application_user = USER
    website.default_locale = default_locale
    website.locales = locales
    website.guest_user = guest_user
    return website


def create_countries(count=5):
    """
    Create some sample countries and subdivisions
    """
    pool = Pool()
    Subdivision = pool.get('country.subdivision')
    Country = pool.get('country.country')

    for country in list(pycountry.countries)[0:count]:
        countries = Country.create([{
            'name': country.name,
            'code': country.alpha_2,
        }])
        try:
            divisions = pycountry.subdivisions.get(
                country_code=country.alpha_2
            )
        except KeyError:
            pass
        else:
            for subdivision in list(divisions)[0:count]:
                Subdivision.create([{
                    'country': countries[0].id,
                    'name': subdivision.name,
                    'code': subdivision.code,
                    'type': subdivision.type.lower(),
                }])


def create_pricelists(party_pl_margin=None, guest_pl_margin=None):
    """
    Create the pricelists
    """
    pool = Pool()
    PriceList = pool.get('product.price_list')
    Company = pool.get('company.company')

    if party_pl_margin is None:
        party_pl_margin = Decimal('1.10')
    if guest_pl_margin is None:
        guest_pl_margin = Decimal('1.20')
    # Setup the pricelists
    company, = Company.search([])
    user_price_list, = PriceList.create([{
        'name': 'PL 1',
        'company': company.id,
        'lines': [
            ('create', [{
                'formula': 'unit_price * %s' % party_pl_margin
            }])
        ],
    }])
    guest_price_list, = PriceList.create([{
        'name': 'PL 2',
        'company': company.id,
        'lines': [
            ('create', [{
                'formula': 'unit_price * %s' % guest_pl_margin
            }])
        ],
    }])
    return guest_price_list.id, user_price_list.id


def create_product_template(name, vlist, uri, uom='Unit'):
    """
    Create a product template with products and return its ID

    :param name: Name of the product
    :param vlist: List of dictionaries of values to create
    :param uri: uri of product template
    :param uom: Note it is the name of UOM (not symbol or code)
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
        expense, = Account.search([
                ('type.expense', '=', True),
                ])

    with Transaction().set_context(company=company.id):
        category = Category()
        category.name = 'Account category'
        category.account_revenue = revenue
        category.account_expense = expense
        category.accounting = True
        category.save()

    uom, = Uom.search([('name', '=', uom)])
    for values in vlist:
        values['name'] = name
        values['default_uom'] = uom
        values['sale_uom'] = uom
        values['account_category'] = category
        values['products'] = [
            ('create', [{
                'uri': uri,
                'displayed_on_eshop': True,
                'cost_price': Decimal('5'),
            }])
        ]
    return Template.create(vlist)


class NereidCartB2CTestCase(NereidModuleTestCase):
    'Test Nereid Cart B2C module'
    module = 'nereid_cart_b2c'

    def setUp(self):
        self.templates = {
            'home.jinja': '{{get_flashed_messages()}}',
            'login.jinja':
                '{{ login_form.errors }} {{get_flashed_messages()}}',
            'shopping-cart.jinja':
                'Cart:{{ cart.id }},{{get_cart_size()|round|int}},'
                '{{cart.sale.total_amount}}',
            'product.jinja':
                '{{ product.sale_price(product.id) }}',
            }

    @with_transaction()
    def test_0010_test_guest_price(self):
        """
        Test the pricelist lookup algorithm

        We are not logged in, the pricelist of the channel is used.
        """
        pool = Pool()
        Company = pool.get('company.company')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        website = create_website()
        website.save()
        gateway = create_payment_gateway()
        gateway.save()
        company, = Company.search([])

        # Create product templates with products
        template1, = create_product_template(
            'product-1',
            [{
                'type': 'goods',
                'salable': True,
                'list_price': Decimal('10'),
            }],
            uri='product-1',
        )
        template2, = create_product_template(
            'product-2',
            [{
                'type': 'goods',
                'salable': True,
                'list_price': Decimal('15'),
            }],
            uri='product-2',
        )

        party_pl_margin = Decimal('1.10')
        guest_pl_margin = Decimal('1.20')

        app = self.get_app()
        with app.test_client() as c:
            rv = c.get('/en/product/product-1')
            self.assertEqual(
                Decimal(rv.data.decode('utf-8')),
                Decimal('10') * guest_pl_margin)

            rv = c.get('/en/product/product-2')
            self.assertEqual(
                Decimal(rv.data.decode('utf-8')),
                Decimal('15') * guest_pl_margin)


    @with_transaction()
    def test_0020_user_status(self):
        """
        Test that `_user_status()` returns a dictionary
        with correct params.
        """
        pool = Pool()
        Company = pool.get('company.company')
        SaleLine = pool.get('sale.line')
        Channel = pool.get('sale.channel')
        Product = pool.get('product.product')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        website = create_website()
        website.save()
        gateway = create_payment_gateway()
        gateway.save()
        company, = Company.search([])

        # Create product templates with products
        template1, = create_product_template(
            'product-1',
            [{
                'type': 'goods',
                'salable': True,
                'list_price': Decimal('10'),
            }],
            uri='product-1',
        )

        #channel1 = Channel.search([
        #        ('name', '=', 'Channel1'),
        #        ])
        app = self.get_app()
        with app.test_client() as c:
            response = c.post(
                '/en/login',
                data={
                    'email': 'email@example.com',
                    'password': 'password',
                    }
                )
            self.assertEqual(response.status_code, 302)  # Login success

            product, = Product.search([('name', '=', 'product-1')])
            print(Transaction().context)
            rv = c.post(
                '/en/cart/add',
                data={
                    'product': product.id, 'quantity': 7
                }
            )
            self.assertEqual(rv.status_code, 302)

            line, = SaleLine.search([])
            results = c.get('/user_status')

            data = json.loads(results.data)
            lines = data['status']['cart']['lines']

            self.assertEqual(len(lines), 1)
            self.assertEqual(line.serialize('cart'), lines[0])

def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            NereidCartB2CTestCase))
    return suite
