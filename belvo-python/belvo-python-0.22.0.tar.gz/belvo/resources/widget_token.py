from typing import Optional

from belvo.resources.base import Resource


class WidgetToken(Resource):
    endpoint = "/api/token/"

    def create(
        self,
        *,
        scopes: Optional[str] = None,
        link: Optional[str] = None,
        raise_exception: bool = False,
    ):
        if scopes is None:
            scopes = "read_institutions,write_links,read_links"

        data = {
            "id": self.session._secret_key_id,
            "password": self.session._secret_key_password,
            "scopes": scopes,
        }

        if link:
            data.update(link_id=link)

        return self.session.post(self.endpoint, data=data, raise_exception=raise_exception)
