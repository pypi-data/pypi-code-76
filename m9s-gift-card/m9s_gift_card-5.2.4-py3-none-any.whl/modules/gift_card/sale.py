# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal
from trytond import backend
from trytond.model import (ModelView, ModelSQL, ValueMixin,
    fields)
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval, Bool, Get
from trytond.wizard import Wizard
from trytond.tools.multivalue import migrate_property
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)

from trytond.i18n import gettext
from trytond.exceptions import UserError


gift_card_method = fields.Selection([
                ('order', 'On Order Processed'),
                ('invoice', 'On Invoice Paid'),
                ], 'Gift Card Creation Method',
            required=True)


class SaleConfiguration(metaclass=PoolMeta):
    __name__ = 'sale.configuration'

    gift_card_method = fields.MultiValue(gift_card_method)


class _ConfigurationValue(ModelSQL):

    _configuration_value_field = None

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        exist = TableHandler.table_exist(cls._table)

        super(_ConfigurationValue, cls).__register__(module_name)

        if not exist:
            cls._migrate_property([], [], [])

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.append(cls._configuration_value_field)
        value_names.append(cls._configuration_value_field)
        migrate_property(
            'sale.configuration', field_names, cls, value_names,
            fields=fields)


class SaleGiftCardMethod(_ConfigurationValue, ModelSQL, ValueMixin):
    'Sale Gift Card Method'
    __name__ = 'sale.configuration.gift_card_method'
    gift_card_method = gift_card_method
    _configuration_value_field = 'gift_card_method'


class SaleLine(metaclass=PoolMeta):
    "SaleLine"
    __name__ = 'sale.line'

    gift_card_delivery_mode = fields.Function(
        fields.Selection([
            ('virtual', 'Virtual'),
            ('physical', 'Physical'),
            ('combined', 'Combined'),
        ], 'Gift Card Delivery Mode', states={
            'invisible': ~Bool(Eval('is_gift_card')),
        }, depends=['is_gift_card']), 'get_gift_card_delivery_mode'
    )

    is_gift_card = fields.Function(
        fields.Boolean('Gift Card'),
        'get_is_gift_card'
    )
    gift_cards = fields.One2Many(
        'gift_card.gift_card', "sale_line", "Gift Cards", readonly=True
    )
    message = fields.Text(
        "Message", states={'invisible': ~Bool(Eval('is_gift_card'))}
    )

    recipient_email = fields.Char(
        "Recipient Email", states={
            'invisible': ~(
                Bool(Eval('is_gift_card')) &
                (Eval('gift_card_delivery_mode').in_(['virtual', 'combined']))
            ),
            'required': (
                Bool(Eval('is_gift_card')) &
                (Eval('gift_card_delivery_mode').in_(['virtual', 'combined']))
            ),
        }, depends=['gift_card_delivery_mode', 'is_gift_card']
    )

    recipient_name = fields.Char(
        "Recipient Name", states={
            'invisible': ~Bool(Eval('is_gift_card')),
        }, depends=['is_gift_card']
    )
    allow_open_amount = fields.Function(
        fields.Boolean("Allow Open Amount?", states={
            'invisible': ~Bool(Eval('is_gift_card'))
        }, depends=['is_gift_card']), 'get_allow_open_amount'
    )

    gc_price = fields.Many2One(
        'product.product.gift_card.price', "Gift Card Price", states={
            'required': (
                ~Bool(Eval('allow_open_amount')) & Bool(Eval('is_gift_card'))
            ),
            'invisible': ~(
                ~Bool(Eval('allow_open_amount')) & Bool(Eval('is_gift_card'))
            )
        }, depends=['allow_open_amount', 'is_gift_card', 'product'], domain=[
            ('product', '=', Eval('product'))
        ]
    )

    @classmethod
    def view_attributes(cls):
        return super(SaleLine, cls).view_attributes() + [
            ('//page[@id="gift_cards"]', 'states', {
                'invisible': ~Bool(Eval('is_gift_card'))
            }), ('//separator[@id="recipient_details"]', 'states', {
                'invisible': ~Bool(Eval('is_gift_card'))
            }), (
                '//field[@name="message"]', 'spell',
                Get(Eval('_parent_sale', {}), 'party_lang')
            )]

    @fields.depends('product')
    def on_change_with_allow_open_amount(self, name=None):
        SaleLine = Pool().get('sale.line')

        return SaleLine.get_allow_open_amount(
            [self], name='allow_open_amount'
        )[self.id]

    @classmethod
    def get_allow_open_amount(cls, lines, name):
        return {
            line.id: (
                line.product.allow_open_amount if line.product else None
            )
            for line in lines
        }

    @fields.depends('gc_price', 'unit_price')
    def on_change_gc_price(self):
        if self.gc_price:
            self.unit_price = self.gc_price.price

    @classmethod
    def __setup__(cls):
        super(SaleLine, cls).__setup__()

        cls.unit_price.states['readonly'] = (
            ~Bool(Eval('allow_open_amount')) & Bool(Eval('is_gift_card'))
        )

    @classmethod
    def get_gift_card_delivery_mode(cls, lines, name):
        res = {}
        for line in lines:
            if not (line.product and line.is_gift_card):
                mode = None
            else:
                mode = line.product.gift_card_delivery_mode
            res[line.id] = mode
        return res

    @fields.depends('product', 'is_gift_card')
    def on_change_with_gift_card_delivery_mode(self, name=None):
        """
        Returns delivery mode of the gift card product
        """
        SaleLine = Pool().get('sale.line')

        return SaleLine.get_gift_card_delivery_mode(
            [self], name='gift_card_delivery_mode'
        )[self.id]

    @classmethod
    def copy(cls, lines, default=None):
        if default is None:
            default = {}
        default['gift_cards'] = None
        return super(SaleLine, cls).copy(lines, default=default)

    @fields.depends('product')
    def on_change_with_is_gift_card(self, name=None):
        """
        Returns boolean value to tell if product is gift card or not
        """
        SaleLine = Pool().get('sale.line')

        return SaleLine.get_is_gift_card(
            [self], name='is_gift_card'
        )[self.id]

    @classmethod
    def get_is_gift_card(cls, lines, name):
        return {
            line.id: (
                line.product.is_gift_card if line.product else None
            )
            for line in lines
        }

    def get_invoice_line(self):
        """
        Pick up liability account from gift card configuration for invoices
        """
        GiftCardConfiguration = Pool().get('gift_card.configuration')

        lines = super(SaleLine, self).get_invoice_line()

        if lines and self.is_gift_card:
            liability_account = GiftCardConfiguration(1).liability_account

            if not liability_account:
                raise UserError(gettext('gift_card.missing_liability_account'))

            for invoice_line in lines:
                invoice_line.account = liability_account

        return lines

    @fields.depends('is_gift_card', 'product')
    def on_change_is_gift_card(self):
        ModelData = Pool().get('ir.model.data')

        if self.is_gift_card:
            self.product = None
            self.description = "Gift Card"
            self.unit = ModelData.get_id('product', 'uom_unit')
        else:
            self.description = None
            self.unit = None

    def create_gift_cards(self):
        '''
        Create the actual gift card for this line
        '''
        GiftCard = Pool().get('gift_card.gift_card')

        if not self.is_gift_card:
            # Not a gift card line
            return None

        product = self.product

        if product.allow_open_amount and not (
            product.gc_min <= self.unit_price <= product.gc_max
        ):
            from trytond.transaction import Transaction
            raise UserError(
                gettext('gift_card.amounts_out_of_range',
                    currency_code=self.sale.currency.code,
                    gc_min=product.gc_min,
                    gc_max=product.gc_max))

        # XXX: Do not consider cancelled ones in the gift cards.
        # card could have been cancelled for reasons like wrong message ?
        quantity_created = len(self.gift_cards)

        if self.sale.gift_card_method == 'order':
            quantity = self.quantity - quantity_created
        else:
            # On invoice paid
            quantity_paid = 0
            for invoice_line in self.invoice_lines:
                if invoice_line.invoice.state == 'paid':
                    invoice_line.quantity
                    quantity_paid += invoice_line.quantity

            # Remove already created gift cards
            quantity = quantity_paid - quantity_created

        if not quantity > 0:
            # No more gift cards to create
            return

        gift_cards = GiftCard.create([{
            'amount': self.unit_price,
            'sale_line': self.id,
            'message': self.message,
            'recipient_email': self.recipient_email,
            'recipient_name': self.recipient_name,
            'origin': '%s,%d' % (self.sale.__name__, self.sale.id),
        } for each in range(0, int(quantity))])

        GiftCard.activate(gift_cards)

        return gift_cards


class Sale(metaclass=PoolMeta):
    "Sale"
    __name__ = 'sale.sale'

    # Gift card creation method
    gift_card_method = fields.Selection([
        ('order', 'On Order Processed'),
        ('invoice', 'On Invoice Paid'),
    ], 'Gift Card Creation Method', required=True)

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()

        cls.gift_card_method.states = cls.shipment_method.states

    @staticmethod
    def default_gift_card_method():
        SaleConfig = Pool().get('sale.configuration')
        config = SaleConfig(1)

        return config.gift_card_method

    def create_gift_cards(self):
        '''
        Create the gift cards if not already created
        '''
        for line in [l for l in self.lines if l.is_gift_card]:
            line.create_gift_cards()

    @classmethod
    def get_payment_method_priority(cls):
        """Priority order for payment methods. Downstream modules can override
        this method to change the method priority.
        """
        return ('gift_card',) + \
            super(Sale, cls).get_payment_method_priority()

    @classmethod
    @ModelView.button
    def process(cls, sales):
        """
        Create gift card on processing sale
        """

        super(Sale, cls).process(sales)

        for sale in sales:
            if sale.state not in ('confirmed', 'processing', 'done'):
                continue        # pragma: no cover
            sale.create_gift_cards()

    def settle_manual_payments(self):
        super(Sale, self).settle_manual_payments()
        for payment in self.payments:
            if payment.amount_available and payment.method == "gift_card" and \
                    not payment.payment_transactions:
                payment_transaction = payment._create_payment_transaction(
                    payment.amount_available, payment.description)
                payment_transaction.save()
                payment.capture()
                self.payment_processing_state = None


class Payment(metaclass=PoolMeta):
    'Payment'
    __name__ = 'sale.payment'

    gift_card = fields.Many2One(
        "gift_card.gift_card", "Gift Card", states={
            'required': Eval('method') == 'gift_card',
            'invisible': ~(Eval('method') == 'gift_card'),
        }, domain=[('state', '=', 'active')], depends=['method']
    )

    def _create_payment_transaction(self, amount, description):
        """Creates an active record for gateway transaction.
        """
        payment_transaction = super(Payment, self)._create_payment_transaction(
            amount, description,
        )
        payment_transaction.gift_card = self.gift_card

        return payment_transaction

    @classmethod
    def validate(cls, payments):
        """
        Validate payments
        """
        super(Payment, cls).validate(payments)

        for payment in payments:
            payment.check_gift_card_amount()

    def check_gift_card_amount(self):
        """
        Payment should not be created if gift card has insufficient amount
        """
        if self.gift_card and self.gift_card.amount_available < self.amount:
            raise UserError(gettext(
                    'gift_card.insufficient_amount_to_pay',
                    self.gift_card.number, self.sale.currency.code,
                    self.amount))

    def get_payment_description(self, name):
        """
        Return a short description of the sale payment
        This can be used in documents to show payment details
        """
        if self.method == 'gift_card':
            number = ('x' * 5) + self.gift_card.number[-3:]
            return gettext('gift_card.gift_card_paid_message',
                number=number)
        return super(Payment, self).get_payment_description(name)


class AddSalePaymentView(metaclass=PoolMeta):
    """
    View for adding Sale Payments
    """
    __name__ = 'sale.payment.add_view'

    gift_card = fields.Many2One(
        "gift_card.gift_card", "Gift Card", states={
            'required': Eval('method') == 'gift_card',
            'invisible': ~(Eval('method') == 'gift_card'),
        }, domain=[('state', '=', 'active')], depends=['method']
    )

    @classmethod
    def __setup__(cls):
        super(AddSalePaymentView, cls).__setup__()

        for field in [
            'owner', 'number', 'expiry_year', 'expiry_month',
            'csc', 'swipe_data', 'payment_profile'
        ]:
            getattr(cls, field).states['invisible'] = (
                getattr(cls, field).states['invisible'] |
                (Eval('method') == 'gift_card')
            )

    @fields.depends('sale', 'gift_card', 'amount')
    def on_change_gift_card(self):
        amount_to_pay = Decimal('0.0')
        if self.sale:
            amount_to_pay = self.sale.total_amount - self.sale.payment_total
        if self.gift_card:
            if amount_to_pay > self.gift_card.amount_available:
                self.amount = self.gift_card.amount_available
            else:
                self.amount = amount_to_pay
        else:
            self.amount = amount_to_pay


class AddSalePayment(Wizard):
    """
    Wizard to add a Sale Payment
    """
    __name__ = 'sale.payment.add'

    def create_sale_payment(self, profile=None):
        """
        Helper function to create new payment
        """
        sale_payment = super(AddSalePayment, self).create_sale_payment(
            profile=profile
        )
        # XXX: While a value will exist for the field gift_card when
        # it's the Tryton client calling the wizard, it is not going
        # to be there as an attribute when called from API (from another
        # module/model for example).
        sale_payment.gift_card = (self.payment_info.method == 'gift_card')  \
            and self.payment_info.gift_card or None

        return sale_payment
