from django_pay2.settings import payment_settings

from .api import TinkoffApi


def get_tinkoff_api() -> TinkoffApi:
    return TinkoffApi(
        payment_settings.TINKOFF.terminal_key,
        payment_settings.TINKOFF.password,
    )
