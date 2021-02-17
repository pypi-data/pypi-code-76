from typing import List, Optional

from django.urls import reverse
from ipware.ip import get_client_ip

from django_pay2.decorators import handle_debug
from django_pay2.exceptions import CreatePaymentError
from django_pay2.models import Payment
from django_pay2.providers.tinkoff.entities.init import InitRequest, Item, Receipt
from django_pay2.settings import payment_settings

from .exceptions import TinkoffApiError
from .functions import get_tinkoff_api


@handle_debug
def create_tinkoff_payment(
    request,
    amount,
    desc,
    receiver,
    items: List[Item],
    client_email: Optional[str] = None,
    client_phone: Optional[str] = None,
):
    payment = Payment.objects.create(amount=amount, receiver=receiver)
    try:
        api = get_tinkoff_api()

        init_request = construct_init_request(
            request, amount, desc, items, str(payment.id), client_email, client_phone
        )
        init_response = api.init(init_request)
        return init_response.payment_url
    except TinkoffApiError as exc:
        payment.reject()
        raise CreatePaymentError(str(exc))


def construct_init_request(
    request,
    amount,
    desc,
    items: List[Item],
    order_id: str,
    client_email: Optional[str] = None,
    client_phone: Optional[str] = None,
) -> InitRequest:
    ip, _ = get_client_ip(request)
    notification_url = reverse("django_pay2:tinkoff:notify")
    success_url = reverse("django_pay2:success")
    fail_url = reverse("django_pay2:fail")
    return InitRequest(
        amount_rub=amount,
        order_id=order_id,
        ip=ip,
        description=desc,
        notification_url=request.build_absolute_uri(notification_url),
        success_url=request.build_absolute_uri(success_url),
        fail_url=request.build_absolute_uri(fail_url),
        receipt=Receipt(
            email=client_email,
            phone=client_phone,
            email_company=payment_settings.TINKOFF.email_company,
            taxation=payment_settings.TINKOFF.taxation,
            items=items,
        ),
    )
