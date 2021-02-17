from decimal import Decimal

from django.utils.functional import cached_property

from django_pay2.models import Payment
from django_pay2.providers.tinkoff.exceptions import TinkoffNotifyValidationError
from django_pay2.providers.tinkoff.tokens import build_token


class NotifyValidator:
    def __init__(self, data, terminal_key, password):
        self.data = data
        self.terminal_key = terminal_key
        self.password = password

    def validate(self):
        terminal_key = self.data.get("TerminalKey")
        if terminal_key != self.terminal_key:
            print(f"Received terminal key={terminal_key}, expected={self.terminal_key}")
            raise TinkoffNotifyValidationError(
                "Received terminal key does not equal to expected"
            )

        token = self.data.get("Token")
        if build_token(self.data, self.password) != token:
            print(
                f"Received token={token}, expected={build_token(self.data, self.password)}"
            )
            raise TinkoffNotifyValidationError("Received token is incorrect")

        order_id = self.data.get("OrderId")
        try:
            payment = Payment.objects.get(pk=order_id)
        except Payment.DoesNotExist:
            raise TinkoffNotifyValidationError(
                f"Payment with id={order_id} does not exist"
            )

        amount = self.data.get("Amount")
        if amount != int(payment.amount * 100):
            raise TinkoffNotifyValidationError("Payment amounts is not equal")


class Notify:
    def __init__(self, data):
        self.order_id: str = data.get("OrderId")
        self.is_success: bool = data.get("Success")
        self.payment_id: int = data.get("PaymentId")
        self.error_code: str = data.get("ErrorCode")
        self.amount_rub = Decimal(data.get("Amount")) / 100

    @cached_property
    def payment(self):
        return Payment.objects.get(pk=self.order_id)
