# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
'''

    Manual payment gateway

    Often payment modes are offline like cash, external credit card terminals
    etc. This gateway implements that
'''

from trytond.model import fields
from trytond.pool import Pool, PoolMeta


class PaymentGatewayManual(metaclass=PoolMeta):
    "COD, Cheque and Bank Transfer Implementation"
    __name__ = 'payment_gateway.gateway'

    @classmethod
    def get_providers(cls, values=None):
        """
        Downstream modules can add to the list
        """
        rv = super(PaymentGatewayManual, cls).get_providers()
        self_record = ('manual', 'Manual')
        if self_record not in rv:
            rv.append(self_record)
        return rv

    @fields.depends('provider')
    def get_methods(self):
        if self.provider == 'manual':
            return [
                ('manual', 'Manual/Offline'),
            ]
        return super(PaymentGatewayManual, self).get_methods()


class ManualTransaction(metaclass=PoolMeta):
    """
    Implement the authorize and capture methods
    """
    __name__ = 'payment_gateway.transaction'

    def authorize_manual(self, card_info=None):
        """
        Authorize a manual payment
        """
        self.state = 'authorized'
        self.save()

    def settle_manual(self):
        """
        Capture a manual payment.
        All that needs to be done is post the transaction.
        """
        self.state = 'completed'
        self.save()
        self.safe_post()

    def capture_manual(self):
        """
        Capture a manual payment.
        All that needs to be done is post the transaction.
        """
        self.state = 'completed'
        self.save()
        self.safe_post()

    def refund_manual(self):
        self.state = 'completed'
        self.save()
        self.safe_post()

    def cancel_dummy(self):
        """
        Cancel a dummy transaction
        """
        if self.state != 'authorized':
            self.raise_user_error('cancel_only_authorized')
        else:
            self.state = 'cancel'
            self.save()
