"""
    CLASS LOADER from API TO S3, v2
    https://www.amocrm.com/developers/content/digital_pipeline/site_visit/
"""
import sys
import logging
import requests

PAGE_NUMBER_MAX = 1e6


def process_json(data, entity):
    """
    update data after retrieving from s3
    Args:
        data: row data json
    Returns: list
    """
    if entity in ("leads", "companies", "contacts", "tasks"):
        items = data["_embedded"]["items"]
    elif entity in "funnels":
        items = [item for key, item in data["_embedded"]["items"].items()]
    elif entity in "users":
        items = [item for key, item in data["_embedded"]["users"].items()]
    return items


class AmocrmApiLoader:
    """
    main class
    """

    def __init__(
            self,
            entity,
            s3_client,
            args_api,
            date_modified_from=None,
            with_offset=True,
            batch_api=500,
    ):
        """
        :param entity:   amocrm entities contacts/users/accounts e.t.c
        :param s3_client: s3 client from talenttech-oss library
        :param args_api: dict with AMO_USER_LOGIN/AMO_USER_HASH/AMO_AUTH_URL keys required
        :param date_modified_from: date update from where we are loading data
        :param with_offset:
        :param batch_api: size of batch to upload
        """
        log_format = "%(asctime)-15s %(name)s:%(levelname)s: %(message)s"
        logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)
        logging.basicConfig(format=log_format, stream=sys.stderr, level=logging.ERROR)
        logging.captureWarnings(True)
        self.logger = logging.getLogger(__class__.__name__)

        self.entity = entity

        self.args_api = args_api
        self.batch_api = batch_api
        self.auth_cookie_str = None

        self.date_modified_from = date_modified_from
        self.with_offset = with_offset
        self.rows_to_upload = 0

        self.s3_client = s3_client

    def __auth(self):
        """API authorization"""
        params = {
            "USER_LOGIN": self.args_api["AMO_USER_LOGIN"],
            "USER_HASH": self.args_api["AMO_USER_HASH"],
            "type": "json",
        }
        resp = requests.post(self.args_api["AMO_AUTH_URL"], data=params)
        response = resp.json()

        if response["response"]["auth"]:
            self.auth_cookie_str = resp.cookies
            self.logger.info(
                "AmoCRM: Authorized user %s ", self.args_api["AMO_AUTH_URL"]
            )
            return True

        self.logger.info(response["response"])
        raise ValueError("AmoCRM: Not authorized")

    def clear_s3_folder(self):
        """Clear all data from s3 folder"""
        if self.s3_client.path_exists(self.s3_client.root_dir):
            for file in self.s3_client.get_file_list(self.s3_client.root_dir):
                self.logger.info("Delete %s from s3", file)
                self.s3_client.delete_file(path=file)
            self.s3_client.delete_dir(self.s3_client.root_dir)  # remove directory

    def __get_file_name(self, offset, batch):
        """
        Returns: s3 file name
        """
        return "{dir_path}/{entity}_{offset}_{batch}.json".format(
            dir_path=self.s3_client.root_dir,
            entity=self.entity,
            offset=offset,
            batch=batch,
        )

    def extract(self):
        """load table from amocrm.api"""
        if self.__auth():
            if not self.s3_client.path_exists(self.s3_client.root_dir):
                self.s3_client.create_dir(self.s3_client.root_dir)
        self.clear_s3_folder()  # clear old before loading

        headers = {
            "Content-Type": "application/json",
        }
        url_base = self.args_api["amocrm_api_url"]
        cur_offset = 0
        count_uploaded = self.batch_api

        params = {}
        while cur_offset < PAGE_NUMBER_MAX and count_uploaded == self.batch_api:
            file_path = self.__get_file_name(cur_offset, self.batch_api)
            self.logger.info("Extracting page number %d ", cur_offset)
            if self.date_modified_from is not None:
                self.logger.info(
                    "Uploading data with after %s ", self.date_modified_from
                )
                url = url_base.format(batch_size_api=self.batch_api, offset=cur_offset)
                headers["IF-MODIFIED-SINCE"] = self.date_modified_from.strftime(
                    "%a, %d %b %Y %H:%M:%S UTC"
                )
            else:
                url = url_base
            self.logger.info(url)
            objects = requests.get(
                url, cookies=self.auth_cookie_str, headers=headers, params=params
            )
            try:
                count_uploaded = len(process_json(objects.json(), self.entity))
                self.logger.info(
                    "Saving data in file %s, count rows %d, total: %d",
                    file_path,
                    count_uploaded,
                    self.rows_to_upload,
                )
                self.s3_client.create_file(file_path, objects.content)
                self.rows_to_upload += count_uploaded
            except Exception as exc:
                self.logger.info("Can't load objects.content, exception: %s ", exc)
                self.logger.info("Objects.content: %s ", objects.content)
                return
            cur_offset += self.batch_api
        self.logger.info(
            "Total number of rows received from API is %d", self.rows_to_upload
        )
