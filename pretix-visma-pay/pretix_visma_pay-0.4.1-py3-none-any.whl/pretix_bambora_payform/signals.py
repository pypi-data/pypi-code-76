from collections import OrderedDict

from django import forms
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from pretix.base.signals import register_global_settings, register_payment_providers


@receiver(register_payment_providers, dispatch_uid="payment_bambora_payform")
def register_payment_provider(sender, **kwargs):
    from .payment import BamboraPayformProvider
    return BamboraPayformProvider


@receiver(register_global_settings, dispatch_uid='bambora_payform_global_settings')
def register_global_settings(sender, **kwargs):
    return OrderedDict([
        ('payment_bambora_payform_api_key', forms.CharField(
            label=_('Visma Pay: API key'),
            required=False,
        )),
        ('payment_bambora_payform_private_key', forms.CharField(
            label=_('Visma Pay: Private key'),
            required=False,
        )),
        ('payment_bambora_payform_test_api_key', forms.CharField(
            label=_('Visma Pay: Test API key'),
            required=False,
        )),
        ('payment_bambora_payform_test_private_key', forms.CharField(
            label=_('Visma Pay: Test private key'),
            required=False,
        )),
    ])
