# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields, ModelSQL, ModelView
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Bool

from trytond.i18n import gettext
from trytond.exceptions import UserError


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'

    is_gift_card = fields.Boolean("Is Gift Card ?")

    gift_card_delivery_mode = fields.Selection([
        ('virtual', 'Virtual'),
        ('physical', 'Physical'),
        ('combined', 'Combined'),
    ], 'Gift Card Delivery Mode')

    allow_open_amount = fields.Boolean("Allow Open Amount ?")
    gc_min = fields.Numeric("Gift Card Minimum Amount")

    gc_max = fields.Numeric("Gift Card Maximum Amount")

    gift_card_prices = fields.One2Many(
        'product.product.gift_card.price', 'product', 'Gift Card Prices',
    )

    @classmethod
    def view_attributes(cls):
        return super(Product, cls).view_attributes() + [
            ('//page[@id="gift_card_details"]', 'states', {
                'invisible': ~Bool(Eval('is_gift_card'))
            })]

    @staticmethod
    def default_gift_card_delivery_mode():
        return 'physical'

    @staticmethod
    def default_is_gift_card():
        return False

    @staticmethod
    def default_allow_open_amount():
        return False

    @classmethod
    def validate(cls, products):
        """
        Validates each product product
        """
        super(Product, cls).validate(products)

        for product in products:
            product.check_product_type()
            product.check_gc_min_max()

    def check_gc_min_max(self):
        """
        Check minimum amount to be smaller than maximum amount
        """
        if not self.allow_open_amount:
            return

        if self.gc_min < 0 or self.gc_max < 0:
            raise UserError(gettext(
                    'gift_card.negative_amount_not_allowed'))

        if self.gc_min > self.gc_max:
            raise UserError(gettext(
                    'gift_card.invalid_amount'))

    def check_product_type(self):
        '''
        Product type of gift cards must be service.
        '''
        if not self.is_gift_card:
            return

        if self.type != 'service':
            raise UserError(
                gettext('gift_card.inappropriate_product_type',
                    self.rec_name))


class GiftCardPrice(ModelSQL, ModelView):
    "Gift Card Price"
    __name__ = 'product.product.gift_card.price'

    product = fields.Many2One(
        "product.product", "Product", required=True, select=True
    )

    price = fields.Numeric("Price", required=True)

    def get_rec_name(self, name):
        return str(self.price)

    @classmethod
    def validate(cls, prices):
        """
        Validate product price for gift card
        """
        super(GiftCardPrice, cls).validate(prices)

        for price in prices:
            price.check_price()

    def check_price(self):
        """
        Price can not be negative
        """
        if self.price < 0:
            raise UserError(gettext('gift_card.negative_amount'))
