from typing import Dict, List, Union

from belvo.resources.base import Resource


class Invoices(Resource):
    endpoint = "/api/invoices/"

    def create(
        self,
        link: str,
        date_from: str,
        date_to: str,
        type_: str,
        *,
        attach_xml: bool = False,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Union[List[Dict], Dict]:

        data = {
            "link": link,
            "date_from": date_from,
            "date_to": date_to,
            "type": type_,
            "attach_xml": attach_xml,
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
