import uuid
from typing import Dict, Any
from dataclasses import dataclass
from clients_core.service_clients import E360ServiceClient
from .models import AnalyticDatasetDefinitionModel
from marshmallow import EXCLUDE


@dataclass
class AnalyticDatasetDefinitionClient(E360ServiceClient):
    """
    Subclasses dataclass `clients_core.service_clients.E360ServiceClient`.

    Args:
        client (clients_core.rest_client.RestClient): an instance of a rest client
        user_id (str): the user_id guid
        correlation_id (str): the correlation_id guid

    """
    correlation_id: str = str(uuid.uuid4())

    service_endpoint = ""
    extra_headers = {}  # type: Dict[str, str]

    def __post_init__(self) -> None:
        self.extra_headers.update({
            'x-correlation-id': self.correlation_id,
            **self.get_ims_claims()
        })

    def get(self, definition_id: str, **kwargs: Any) -> AnalyticDatasetDefinitionModel:
        """
        Gets the analytic dataset definition object by id.
        """
        response = self.client.get(definition_id, headers=self.extra_headers, raises=True, **kwargs)
        return AnalyticDatasetDefinitionModel.Schema(unknown=EXCLUDE).load(response.json())

    def delete(self, id_: str, **kwargs: Any) -> bool:
        """
        Delete the definition object by its id. Returns True when deleted successfully.
        """
        response = self.client.delete(id_, headers=self.service_headers, raises=True, **kwargs)
        return response.ok
