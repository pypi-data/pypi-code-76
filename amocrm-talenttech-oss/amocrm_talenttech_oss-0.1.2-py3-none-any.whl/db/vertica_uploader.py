"""
Module for downloading data from s3 to vertica
"""

import logging
import sys
import json
import pandas as pd

from vconnector.vertica_connector import VerticaConnector
from converter.fields_converter_oneway import FieldsConverterOneWay

from amocrm.api.api_loader_amocrm_v4 import process_json


def get_date_str(path):
    """get suffix to temporary table using path"""
    return (
        path.split("/")[-2]
            .replace(" ", "")
            .replace("-", "")
            .replace(":", "")
            .replace("+", "")
            .replace(".", "")
    )


class UploaderDB:
    """
    Class to put the data from s3 into vertica
    """

    def __init__(
            self,
            s3_client,
            sql_credentials,
            entity,
            table_name,
            files_in_upload=5,
            json_columns=None,
    ):
        """
        :param s3_client: s3 client from talenttech-oss library
        :param sql_credentials: vertica variable dict
        :param entity:
        :param table_name:
        :param files_in_upload: a number of files in upload
        :param json_columns: list of columns need to beatify as json
        """
        log_format = "%(asctime)-15s %(name)s:%(levelname)s: %(message)s"
        logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)
        logging.basicConfig(format=log_format, stream=sys.stderr, level=logging.ERROR)
        logging.captureWarnings(True)
        self.logger = logging.getLogger(__class__.__name__)

        self.files_in_upload = files_in_upload
        self.sql_credentials = sql_credentials

        self.s3_client = s3_client

        self.uploaded_rows = 0
        self.table_name = table_name
        self.json_columns = json_columns or []

        self.entity = entity
        self.columns = None

    def __update_data(self, data, table_name):
        """
        Date transformation for further update
        :param data:
        :param table_name:
        :return: transformed data
        """
        converter = FieldsConverterOneWay(sql_credentials=None, db="vertica")
        df_original = pd.DataFrame(data=data).drop_duplicates(subset=["id"])
        df_updated = df_original.where(pd.notnull(df_original), None).dropna(
            how="all", axis=1
        )
        for column in self.json_columns:
            if column in df_updated.columns:
                df_updated[column] = df_updated.apply(
                    lambda x: json.dumps(x[column], ensure_ascii=False)
                    if x[column] is not None
                    else None,
                    axis=1,
                )
        items = converter.update_value_type(
            table_name=table_name,
            items=df_updated.to_dict(orient="records"),
            fields=self.columns,
        )
        return items

    def __generate_table_ddl(self, file_path):
        """
        Get approximate table ddl
        :param file_path:
        :return:
        """
        converter = FieldsConverterOneWay(sql_credentials=None, db="vertica")
        cur_data = process_json(
            json.loads(self.s3_client.read_file(file_path)), self.entity
        )
        return converter.create_table_from_dataframe(
            dataframe=pd.DataFrame(data=cur_data),
            table_name=self.table_name,
            to_create=False,
            schema=self.sql_credentials["schema"],
        )

    def __log_status(self, cty_upload):
        self.logger.info(
            "Loading %d rows to %s is successful,  cumulative number is %d",
            cty_upload,
            self.table_name,
            self.uploaded_rows,
        )

    def load_s3_to_db(self):
        """the main method for running class"""
        with VerticaConnector(
                user=self.sql_credentials["user"],
                password=self.sql_credentials["password"],
                database=self.sql_credentials["database"],
                vertica_configs=self.sql_credentials["vertica_configs"],
                sec_to_recconect=2,
                count_retries=1,
        ) as v_connector:
            data = []
            cur_file = 1
            paths = self.s3_client.get_file_list(self.s3_client.root_dir)
            total_files = len(paths)
            try:
                self.columns = v_connector.get_columns(
                    table_name=self.table_name, schema=self.sql_credentials["schema"]
                )
            except ModuleNotFoundError as exc:
                self.logger.warning(exc)
                self.logger.error(
                    "You should create table %s.%s",
                    self.sql_credentials["schema"],
                    self.table_name,
                )
                if total_files > 0:
                    self.logger.info(
                        "You can try to create table like that %s",
                        self.__generate_table_ddl(paths[0]),
                    )
                raise ModuleNotFoundError("Table not found exception") from exc

            for file_path in paths:
                self.logger.info("Loading data from the file %s", file_path)

                cur_data = process_json(
                    json.loads(self.s3_client.read_file(file_path)), self.entity
                )
                data += cur_data
                if cur_file % self.files_in_upload == 0 or cur_file == total_files:
                    data = self.__update_data(data=data, table_name=self.table_name)
                    v_connector.insert_merge_vertica(
                        table_name=self.table_name,
                        schema=self.sql_credentials["schema"],
                        staging_schema=self.sql_credentials["staging_schema"],
                        data=data,
                        staging_table_suffix=get_date_str(file_path),
                    )
                    self.uploaded_rows += len(data)
                    self.__log_status(cty_upload=len(data))
                    data = []
                cur_file += 1
