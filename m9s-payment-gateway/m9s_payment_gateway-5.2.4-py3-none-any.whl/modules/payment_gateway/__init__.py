# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import transaction
from . import dummy
from . import manual
from . import party

__all__ = ['register']


def register():
    Pool.register(
        party.Party,
        transaction.PaymentGateway,
        transaction.PaymentProfile,
        transaction.PaymentTransaction,
        transaction.TransactionLog,
        transaction.AddPaymentProfileView,
        transaction.TransactionUseCardView,
        dummy.PaymentGatewayDummy,
        dummy.AddPaymentProfileViewDummy,
        dummy.DummyTransaction,
        manual.PaymentGatewayManual,
        manual.ManualTransaction,
        transaction.PaymentGatewayResUser,
        transaction.User,
        transaction.AccountMove,
        transaction.AccountMoveLine,
        module='payment_gateway', type_='model')
    Pool.register(
        transaction.AddPaymentProfile,
        dummy.AddPaymentProfileDummy,
        transaction.TransactionUseCard,
        transaction.CreateRefund,
        party.PartyErase,
        module='payment_gateway', type_='wizard')
