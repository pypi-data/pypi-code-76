import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, SupportsInt

from django_pay2.providers.tinkoff.tokens import build_token
from django_pay2.utils import clear_none


class Languages(str, Enum):
    RU = "ru"
    EN = "en"


class PayTypes(str, Enum):
    O = "O"  # noqa
    T = "T"


class Taxations(str, Enum):
    OSN = "osn"
    USN_INCOME = "usn_income"
    USN_INCOME_OUTCOME = "usn_income_outcome"
    PATENT = "patent"
    ENVD = "envd"
    ESN = "esn"


class PaymentMethods(str, Enum):
    FULL_PAYMENT = "full_payment"
    FULL_PREPAYMENT = "full_prepayment"
    PREPAYMENT = "prepayment"
    ADVANCE = "advance"
    PARTIAL_PAYMENT = "partial_payment"
    CREDIT = "credit"
    CREDIT_PAYMENT = "credit_payment"


class Taxes(str, Enum):
    NONE = "none"
    VAT0 = "vat0"
    VAT10 = "vat10"
    VAT20 = "vat20"
    VAT110 = "vat110"
    VAT120 = "vat120"


class PaymentObjects(str, Enum):
    COMMODITY = "commodity"
    EXCISE = "excise"
    JOB = "job"
    SERVICE = "service"
    GAMBLING_BET = "gambling_bet"
    GAMBLING_PRIZE = "gambling_price"
    LOTTERY = "lottery"
    LOTTERY_PRIZE = "lottery_prize"
    INTELLECTUAL_ACTIVITY = "intellectual_activity"
    PAYMENT = "payment"
    AGENT_COMMISSION = "agent_commission"
    COMPOSITE = "composite"
    ANOTHER = "another"


@dataclass
class Item:
    name: str
    quantity: int
    amount_rub: SupportsInt
    price_rub: SupportsInt
    tax: Taxes
    payment_method: Optional[PaymentMethods] = None
    payment_object: Optional[PaymentObjects] = None

    def serialize(self):
        return clear_none(
            {
                "Name": self.name,
                "Quantity": self.quantity,
                "Amount": int(self.amount_rub * 100),
                "Price": int(self.price_rub * 100),
                "PaymentMethod": self.payment_method,
                "PaymentObject": self.payment_object,
                "Tax": self.tax,
            }
        )


@dataclass
class Receipt:
    items: List[Item]
    email: Optional[str] = None
    phone: Optional[str] = None
    email_company: Optional[str] = None
    taxation: Optional[Taxations] = None

    def serialize(self):
        return clear_none(
            {
                "Email": self.email,
                "Phone": self.phone,
                "EmailCompany": self.email_company,
                "Taxation": self.taxation,
                "Items": [item.serialize() for item in self.items],
            }
        )


@dataclass
class InitRequest:
    amount_rub: SupportsInt
    order_id: str
    ip: Optional[str] = None
    description: Optional[str] = None
    lang: Optional[Languages] = None
    notification_url: Optional[str] = None
    success_url: Optional[str] = None
    fail_url: Optional[str] = None
    pay_type: Optional[PayTypes] = None
    receipt: Optional[Receipt] = None

    def bind_credentials(self, terminal_key: str, password: str):
        self.terminal_key = terminal_key
        self.password = password

    def serialize_tokenless(self):
        return clear_none(
            {
                "TerminalKey": self.terminal_key,
                "Amount": int(self.amount_rub * 100),
                "OrderId": self.order_id,
                "IP": self.ip,
                "Description": self.description,
                "Language": self.lang,
                "NotificationURL": self.notification_url,
                "SuccessURL": self.success_url,
                "FailURL": self.fail_url,
                "PayType": self.pay_type,
                "Receipt": self.receipt.serialize() if self.receipt else None,
            }
        )

    def calculate_token(self):
        tokenless_data = self.serialize_tokenless()
        tokenless_data.pop("Receipt", None)
        tokenless_data["Password"] = self.password
        sorted_data = {k: tokenless_data[k] for k in sorted(tokenless_data.keys())}
        prehash_str = "".join(str(k) + str(v) for k, v in sorted_data.items())
        hash_obj = hashlib.sha256(prehash_str.encode("utf-8"))
        return hash_obj.hexdigest()

    def serialize(self):
        return {
            **self.serialize_tokenless(),
            "Token": build_token(self.serialize_tokenless(), self.password),
        }


class InitResponse:
    def __init__(self, raw_data):
        self.is_success: str = raw_data["Success"]
        self.payment_id: int = raw_data.get("PaymentId")
        self.error_code: str = raw_data["ErrorCode"]
        self.payment_url: Optional[str] = raw_data.get("PaymentURL")
        self.message: Optional[str] = raw_data.get("Message")
        self.details: Optional[str] = raw_data.get("Details")
