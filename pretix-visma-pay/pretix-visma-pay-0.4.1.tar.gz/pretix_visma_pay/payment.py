from secrets import token_urlsafe

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from pretix.base.payment import BasePaymentProvider

from .utils import get_credentials
from .visma_pay import VismaPayClient


class VismaPayProvider(BasePaymentProvider):
    def __init__(self, event):
        super().__init__(event)

        credentials = get_credentials(event)
        self.client = VismaPayClient(
            credentials.get('api_key'),
            credentials.get('private_key')
        )

    def checkout_confirm_render(self, request):
        return _('You will be redirected to Visma Pay to complete the payment')

    def execute_payment(self, request, payment):
        callback_url = request.build_absolute_uri(
            reverse(
                'plugins:pretix_visma_pay:visma_pay_callback',
                kwargs={
                    'payment_id': payment.id,
                    'organizer_id': payment.order.event.organizer.id,
                }
            )
        )

        order_number = '{}_{}'.format(payment.order.code, token_urlsafe(16))
        token = self.client.get_token(
            order_number=order_number,
            amount=int(payment.amount * 100),
            email=payment.order.email,
            callback_url=callback_url,
        )

        return self.client.payment_url(token)

    @property
    def identifier(self):
        return 'visma_pay'

    def payment_is_valid_session(self, request):
        return True

    def payment_form_render(self, request, total):
        return render_to_string('pretix_visma_pay/payment_form.html')

    @property
    def public_name(self):
        return '{} – {}'.format(_('Bank and credit card payments'), self.verbose_name)

    @property
    def test_mode_message(self):
        return _('Payment will be simulated while the shop is in test mode. No money will be transferred. Read more at: %(url)s') % {'url': 'https://payform.bambora.com/docs/web_payments/?page=testing'}

    @property
    def verbose_name(self):
        return 'Visma Pay'
