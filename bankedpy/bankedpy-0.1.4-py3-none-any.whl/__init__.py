__version__ = '0.1.4'

from .common import SessionHandler
from .payment_session import * 


class BankedClientBase:
    @property
    def payment_session(self) -> PaymentSessionClientBase:
        raise NotImplementedError


class BankedClient(BankedClientBase):
    def __init__(self, key:str, secret:str):
        self._session_handler = SessionHandler(
            base_url='https://api.banked.com/v2/',
            key=key,
            secret=secret)

        self._payment_session_client = None


    @staticmethod
    def with_credentials(key:str, secret:str) -> 'BankedClient':
        return BankedClient(key, secret)
    
    @property
    def payment_session(self) -> PaymentSessionClientBase:
        if not self._payment_session_client:
            self._payment_session_client = PaymentSessionClient(self._session_handler)
        return self._payment_session_client
