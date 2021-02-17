import requests

from django_pay2.providers.tinkoff.entities.notify import Notify, NotifyValidator

from .entities.init import InitRequest, InitResponse
from .exceptions import TinkoffNetworkError, TinkoffResponseError


class TinkoffApi:
    def __init__(self, terminal_key: str, password: str):
        self.terminal_key = terminal_key
        self.password = password

    def init(self, init_request: InitRequest) -> InitResponse:
        init_request.bind_credentials(self.terminal_key, self.password)
        raw_response = requests.post(
            "https://securepay.tinkoff.ru/v2/Init", json=init_request.serialize()
        )
        if not raw_response.ok:
            raise TinkoffNetworkError(raw_response.status_code, raw_response.text)

        response = InitResponse(raw_response.json())
        if not response.is_success:
            raise TinkoffResponseError(
                response.error_code, response.message, response.details
            )
        return response

    def notify(self, data: dict) -> Notify:
        validator = NotifyValidator(data, self.terminal_key, self.password)
        validator.validate()
        notify = Notify(data)
        if not notify.is_success:
            raise TinkoffResponseError(notify.error_code)
        return notify
