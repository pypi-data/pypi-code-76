from benchling_api_client.api.exports import export_item
from benchling_api_client.models.async_task_link import AsyncTaskLink
from benchling_api_client.models.export_item_request import ExportItemRequest

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.base_service import BaseService


class ExportService(BaseService):
    @api_method
    def export(self, export_request: ExportItemRequest) -> AsyncTaskLink:
        response = export_item.sync_detailed(client=self.client, json_body=export_request)
        return model_from_detailed(response)
