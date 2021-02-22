from .schemas import *
from bankedpy.common import EntityClient, SessionHandler, NotFoundError
from urllib.parse import urljoin


class PaymentSessionClientBase(EntityClient):
    def create(self, payment_session:PaymentSessionRequest) -> PaymentSessionResponse:
        raise NotImplementedError

    def retrieve(self, id:str) -> PaymentSessionResponse:
        raise NotImplementedError

    def remove(self, id:str):
        raise NotImplementedError


class PaymentSessionClient(PaymentSessionClientBase):
    def __init__(self, session:SessionHandler) -> None:
        super().__init__(uri='payment_sessions', session=session)
    
    def create(self, payment_session:PaymentSessionRequest) -> PaymentSessionResponse:
        data = payment_session.json(exclude_unset=True)
        res = self._session.post(self._uri, data=data)
        if res.status_code == 201:
            return PaymentSessionResponse(**res.json())
        raise Exception(f"Unexpected Response {res.status_code}")

    def retrieve(self, id:str) -> PaymentSessionResponse:
        res = self._session.get(f'{self._uri}/{id}')
        if res.status_code == 200:
            return PaymentSessionResponse(**res.json())
        if res.status_code == 404:
            raise NotFoundError 
        raise Exception(f"Unexpected Response {res.status_code}")
    
    def remove(self, id:str):
        res = self._session.delete(f'{self._uri}/{id}')
        if res.status_code == 404:
            raise NotFoundError
        if res.status_code != 204:
            raise Exception(f"Unexpected Response {res.status_code}")
