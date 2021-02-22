from typing import List, Optional
from pydantic import BaseModel, validator, EmailStr
from enum import Enum
from iso4217 import Currency
from pydantic.networks import HttpUrl
from datetime import datetime

class PaymentFrequency(str, Enum):
    DAILY='daily'
    WEEKLY='weekly'
    MONTHLY='monthly'


class PaymentSessionState(str, Enum):
    AWAITING_PROVIDER = 'awaiting_provider'
    AWAITING_PAYMENT_CONSENT = 'awaiting_payment_consent'
    PENDING = 'pending'
    SENT = 'sent'
    FAILED = 'failed'


class PaymentItem(BaseModel):
    name:str
    amount:int
    quantity:int
    currency:Currency


class Payee(BaseModel):
    name:str
    account_number:str
    sort_code:str

    @validator('sort_code')
    def check_uk_bank_sort_code(cls, v:str) -> str:
        if len(v) != 6 or not v.isnumeric():
            raise ValueError("must be 6-length numeric string")
        return v


class Payer(BaseModel):
    name:str
    email:EmailStr


class PaymentSessionBase(BaseModel):
    error_url:str
    success_url:str
    reference:str
    frequency:Optional[PaymentFrequency] = None
    line_items:List[PaymentItem]
    payee:Payee
    payer:Optional[Payer]=None


class PaymentSessionRequest(PaymentSessionBase):
    number_of_payments:Optional[int] = None


class PaymentSessionResponse(PaymentSessionBase):
    id:str
    amount:int
    currency:Currency
    state:PaymentSessionState
    created_at:str
    sent_at:Optional[str] = None
    url:HttpUrl

