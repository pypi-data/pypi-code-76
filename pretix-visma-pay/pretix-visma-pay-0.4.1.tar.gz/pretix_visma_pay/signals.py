from collections import OrderedDict

from django import forms
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from pretix.base.signals import register_global_settings, register_payment_providers


@receiver(register_payment_providers, dispatch_uid="payment_visma_pay")
def register_payment_provider(sender, **kwargs):
    from .payment import VismaPayProvider
    return VismaPayProvider


@receiver(register_global_settings, dispatch_uid='visma_pay_global_settings')
def register_global_settings(sender, **kwargs):
    return OrderedDict([
        ('payment_visma_pay_api_key', forms.CharField(
            label=_('Visma Pay: API key'),
            required=False,
        )),
        ('payment_visma_pay_private_key', forms.CharField(
            label=_('Visma Pay: Private key'),
            required=False,
        )),
        ('payment_visma_pay_test_api_key', forms.CharField(
            label=_('Visma Pay: Test API key'),
            required=False,
        )),
        ('payment_visma_pay_test_private_key', forms.CharField(
            label=_('Visma Pay: Test private key'),
            required=False,
        )),
    ])
