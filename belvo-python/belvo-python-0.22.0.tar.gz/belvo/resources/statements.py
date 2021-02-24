from typing import Dict, List, Union

from belvo.resources.base import Resource


class Statements(Resource):
    endpoint = "/api/statements/"

    def create(
        self,
        link: str,
        account: str,
        year: str,
        month: str,
        *,
        attach_pdf: bool = False,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Union[List[Dict], Dict]:

        data = {
            "link": link,
            "account": account,
            "year": year,
            "month": month,
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
        account: str = None,
        raise_exception: bool = False,
        **kwargs,
    ) -> Union[List[Dict], Dict]:

        data = {"session": session, "token": token}

        if link is not None:
            data.update(link=link)

        if account is not None:
            data.update(account=account)

        return self.session.patch(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )
