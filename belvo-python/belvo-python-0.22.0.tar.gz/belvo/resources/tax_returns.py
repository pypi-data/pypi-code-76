from datetime import date
from typing import Dict, List, Union

from belvo.resources.base import Resource


class TaxReturns(Resource):
    endpoint = "/api/tax-returns/"

    def create(
        self,
        link: str,
        year_from: str,
        year_to: str,
        *,
        attach_pdf: bool = False,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Union[List[Dict], Dict]:

        year_to = year_to or str(date.today().year)

        data = {
            "link": link,
            "year_from": year_from,
            "year_to": year_to,
            "attach_pdf": attach_pdf,
            "save_data": save_data,
        }

        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )

    def resume(
        self,
        session: str,
        token: str,
        *,
        link: str = None,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Dict:
        raise NotImplementedError()
