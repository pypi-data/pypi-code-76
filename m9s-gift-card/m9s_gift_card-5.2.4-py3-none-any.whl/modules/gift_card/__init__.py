# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import gift_card
from . import sale
from . import configuration
from . import gateway
from . import product

__all__ = ['register']


def register():
    Pool.register(
        configuration.Configuration,
        configuration.GiftCardConfigurationSequence,
        configuration.GiftCardLiabilityAccount,
        gift_card.GiftCard,
        gift_card.GiftCardRedeemStart,
        gift_card.GiftCardRedeemDone,
        sale.SaleConfiguration,
        sale.SaleGiftCardMethod,
        sale.SaleLine,
        sale.Sale,
        sale.AddSalePaymentView,
        sale.Payment,
        gateway.PaymentGateway,
        gateway.PaymentTransaction,
        product.GiftCardPrice,
        product.Product,
        module='gift_card', type_='model'
        )
    Pool.register(
        gift_card.GiftCardReport,
        module='gift_card', type_='report'
        )
    Pool.register(
        gift_card.GiftCardRedeemWizard,
        sale.AddSalePayment,
        module='gift_card', type_='wizard'
        )
