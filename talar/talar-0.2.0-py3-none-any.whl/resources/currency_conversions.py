import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from talar.resources.abstract import Resource


class Conversion(BaseModel):
    amount: Decimal
    from_currency: str
    to_currency: str
    rate: Decimal
    result: Decimal
    date: datetime.date


class CurrencyConversions(Resource):
    resource = "currency-conversions/convert/"

    def convert(
        self,
        amount: Decimal,
        from_currency: str,
        to_currency: str,
        date: Optional[datetime.date] = None,
    ) -> Conversion:
        path = f"{self.get_resource()}{amount}/{from_currency}/{to_currency}/"
        if date:
            path = f"{path}{date}/"
        output = self.client.get(path)
        return Conversion(
            from_currency=output["from"], to_currency=output["to"], **output
        )
