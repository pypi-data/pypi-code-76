import logging

from abc import ABC
from abc import abstractmethod

from google.cloud import bigquery
from google.oauth2 import service_account

from google.cloud.bigquery import Client


class BaseMetrics(ABC):

    def __init__(self,  credential_dict: dict):
        self._client = self._create_client(credential_dict)
        self._logger = self._create_logger()

    def execute_bq_query(self, query: str) -> list:
        result = self._client.query(query=query)
        data = [row for row in result]
        return self._format_data(data)

    def insert_rows_bq(self, table_id: str, rows: list) -> any:
        self._logger.info(f"Writing {len(rows)} rows to {table_id}")
        errors = self._client.insert_rows_json(table=table_id, json_rows=rows)
        if len(errors) == 0:
            self._logger.info(f"Successfully wrote {len(rows)} rows to {table_id}")

    def _create_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        logger.addHandler(handler)

        return logger

    @abstractmethod
    def get_metrics(self) -> list:
        raise NotImplementedError()

    @staticmethod
    def _create_client(credential_dict: dict) -> Client:
        creds = service_account.Credentials.from_service_account_info(credential_dict)
        return bigquery.Client(credentials=creds, project=creds.project_id)

    @staticmethod
    def _format_data(data: list) -> list:
        return [{column_name: value for column_name, value in row.items()} for row in data]
