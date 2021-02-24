from datetime import date
from typing import Dict, List, Union

from belvo.resources.base import Resource


class Balances(Resource):
    endpoint = "/api/balances/"

    def create(
        self,
        link: str,
        date_from: str,
        *,
        date_to: str = None,
        account: str = None,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Union[List[Dict], Dict]:

        date_to = date_to or date.today().isoformat()

        data = {"link": link, "date_from": date_from, "date_to": date_to, "save_data": save_data}

        if account:
            data.update(account=account)
        if token:
            data.update(token=token)
        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )
