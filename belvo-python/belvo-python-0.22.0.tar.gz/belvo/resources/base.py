from typing import Dict, Generator, List, Union

from belvo.http import APISession


class Resource:
    endpoint: str

    def __init__(self, session: APISession) -> None:
        self._session = session

    @property
    def session(self) -> APISession:
        return self._session

    def list(self, **kwargs) -> Generator:
        endpoint = self.endpoint
        return self.session.list(endpoint, params=kwargs)

    def get(self, id: str, **kwargs) -> Dict:
        return self.session.get(self.endpoint, id, params=kwargs)

    def delete(self, id: str) -> bool:
        return self.session.delete(self.endpoint, id)

    def resume(
        self, session: str, token: str, *, link: str = None, raise_exception: bool = False, **kwargs
    ) -> Union[List[Dict], Dict]:

        data = {"session": session, "token": token}

        if link is not None:
            data.update(link=link)

        return self.session.patch(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )
