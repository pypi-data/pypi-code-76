from django.urls import reverse
import functools

from .settings import payment_settings
from .models import Payment


def handle_debug(func):
    @functools.wraps(func)
    def wrapped(request, amount, desc, receiver, *args, **kwargs):
        if payment_settings.DEBUG_MODE:
            payment = Payment.objects.create(
                amount=amount,
                receiver=receiver,
            )
            return reverse("django_pay2:debug_payment", args=[payment.id])
        return func(request, amount, desc, receiver, *args, **kwargs)

    return wrapped
