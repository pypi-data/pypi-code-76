from ehelply_bootstrapper.integrations.integration import Integration
from ehelply_bootstrapper.utils.state import State
from datetime import datetime
from typing import Union
from ehelply_microservice_library.integrations.fact import get_fact_endpoint


class Note(Integration):
    """
    Note integration is used to talk to the ehelply-notes microservice
    """

    def __init__(self) -> None:
        super().__init__("note")

        self.m2m = State.integrations.get("m2m")

    def init(self):
        super().init()

    def load(self):
        super().load()

    def get_base_url(self) -> str:
        return get_fact_endpoint('ehelply-notes') + "/notes"

    def create(self, content: str, author: str) -> Union[dict, bool]:
        """
        Sends a request to the notes microservice to create a new note
        :param content:
        :param author:
        :return:
        """
        if type(content) is not str or type(author) is not str:
            State.logger.warning('Note entry discarded due to invalid payload.')
            return False

        data: dict = {
            "note": {
                "content": content,
                "time": datetime.utcnow().isoformat(),
                "meta": {
                    "original_author": author,
                    "author": author,
                }
            }
        }
        return self.m2m.requests.post(self.get_base_url(), json=data).json()

    def get(self, note_uuid: str, history: int = 0, history_content: bool = True) -> Union[dict, bool, None]:
        """
        Sends a request to the notes microservice to retrieve a note
        :param note_uuid:
        :param history:
        :return:
        """
        if type(note_uuid) is not str:
            State.logger.warning('Note entry discarded due to invalid payload.')
            return False

        response = self.m2m.requests.get(self.get_base_url() + "/" + note_uuid,
                                params={"history": history, "history_content": history_content})

        if response.status_code == 404:
            return None

        return response.json()

    def delete(self, note_uuid: str, method: str = "previous") -> Union[dict, bool, None]:
        """
        Sends a request to the notes microservice to delete a note
        :param note_uuid:
        :param method:
        :return:
        """
        if type(note_uuid) is not str:
            State.logger.warning('Note entry discarded due to invalid payload.')
            return False

        response = self.m2m.requests.delete(self.get_base_url() + "/" + note_uuid, params={"method": method})

        if response.status_code == 404:
            return None

        return response.json()

    def update(self, note_uuid: str, content: str, author: str) -> Union[dict, bool, None]:
        """
        Sends a request to the notes microservice to update a note
        :param note_uuid:
        :param content:
        :param author:
        :return:
        """
        if type(content) is not str or type(author) is not str or type(note_uuid) is not str:
            State.logger.warning('Note entry discarded due to invalid payload.')
            return False

        data: dict = {
            "note": {
                "content": content,
                "time": datetime.utcnow().isoformat(),
                "meta": {
                    "author": author,
                }
            }
        }

        response = self.m2m.requests.put(self.get_base_url() + "/" + note_uuid, json=data)

        if response.status_code == 404:
            return None

        return response.json()
