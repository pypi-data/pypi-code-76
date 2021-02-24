import os

from . import resources
from .exceptions import BelvoAPIException
from .http import APISession


class Client:
    def __init__(self, secret_key_id: str, secret_key_password: str, url: str = None) -> None:
        if url is None:
            url = os.getenv("BELVO_API_URL")

        if not url:
            raise BelvoAPIException("You need to provide a URL.")

        self.session = APISession(url)

        if not self.session.login(secret_key_id, secret_key_password):
            raise BelvoAPIException("Login failed.")

        self._links = resources.Links(self.session)
        self._accounts = resources.Accounts(self.session)
        self._transactions = resources.Transactions(self.session)
        self._balances = resources.Balances(self.session)
        self._institutions = resources.Institutions(self.session)
        self._incomes = resources.Incomes(self.session)
        self._owners = resources.Owners(self.session)
        self._invoices = resources.Invoices(self.session)
        self._tax_returns = resources.TaxReturns(self.session)
        self._tax_status = resources.TaxStatus(self.session)
        self._tax_compliance_status = resources.TaxComplianceStatus(self.session)
        self._statements = resources.Statements(self.session)
        self._widget_token = resources.WidgetToken(self.session)

    @property
    def Links(self):
        return self._links

    @property
    def Accounts(self):
        return self._accounts

    @property
    def Transactions(self):
        return self._transactions

    @property
    def Balances(self):
        return self._balances

    @property
    def Institutions(self):
        return self._institutions

    @property
    def Incomes(self):
        return self._incomes

    @property
    def Owners(self):
        return self._owners

    @property
    def Invoices(self):
        return self._invoices

    @property
    def TaxReturns(self):
        return self._tax_returns

    @property
    def TaxComplianceStatus(self):
        return self._tax_compliance_status

    @property
    def TaxStatus(self):
        return self._tax_status

    @property
    def Statements(self):
        return self._statements

    @property
    def WidgetToken(self):
        return self._widget_token
