"""
    CLASS API LOADER to S3 Directory
    https://www.amocrm.com/developers/content/api_v4/leads-2/
"""
import sys
from datetime import datetime, timedelta
import logging
import json
import requests

PAGE_NUMBER_MAX = 1e6


def get_limit_from_url(objects):
    """
    get page limit form response
    :param objects:
    :return:
    """
    import urllib.parse as urlparse

    url = objects.json()["_links"]["self"]["href"]
    par = urlparse.parse_qs(urlparse.urlparse(url).query)
    return int(par["limit"][0])


def process_json(data, entity):
    """
    update data after retrieving from s3
    Args:
        data: row data json
    Returns: list
    """
    return data["_embedded"][entity]


class AmocrmApiLoader:
    """
    The main class
    """

    def __init__(
        self,
        entity,
        s3_client,
        args_api,
        date_modified_from=None,
        with_offset=True,
        batch_api=250,
    ):
        """
        :param entity:   amocrm entities contacts/users/accounts e.t.c
        :param s3_client: s3 client from talenttech-oss library
        :param args_api: dict with AMO_USER_LOGIN/AMO_USER_HASH/AMO_AUTH_URL
        :param date_modified_from:
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
        self.date_modified_from = date_modified_from
        self.with_offset = with_offset

        self.s3_client = s3_client

        self.access_token = None
        self.rows_to_upload = 0

    def __save_tokens_s3(self, data):
        """
        Save data with tokens to s3
        :return:None
        """
        expires_in_datetime = datetime.now() + timedelta(seconds=data["expires_in"])
        data["expires_in_datetime"] = expires_in_datetime.strftime("%Y-%m-%d %H:%M")
        self.logger.info("Modifying config %s...", self.s3_client.secret_dir)
        self.s3_client.create_file(self.s3_client.secret_dir, json.dumps(data))
        self.logger.info(
            "Save new refresh and access token to %s... ", self.s3_client.secret_dir
        )

    def __get_tokens(self, args):
        """
        Get tokens and additional params
        :param args: dict with code or refresh_token
        :return: dict with refresh and access token
        """
        data = {
            "client_secret": self.args_api["CLIENT_SECRET"],
            "client_id": self.args_api["CLIENT_ID"],
            "redirect_uri": self.args_api["REDIRECT_URL"],
        }
        data.update(args)
        resp = requests.post(self.args_api["AUTH_URL"], data=data).json()
        if "refresh_token" not in resp and "access_token" not in resp:
            raise Exception(
                "An error occurred while retrieving auth params: " + str(resp)
            )
        return resp

    def auth(self, code_auth=None):
        """API authorization auth2"""
        # read file from s3 if exists
        try:
            self.logger.info(
                "Load refresh and access token from file %s ", self.s3_client.secret_dir
            )
            response = json.loads(self.s3_client.read_file(self.s3_client.secret_dir))
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            if (
                now_str < response["expires_in_datetime"]
            ):  # check if access token is still valid
                self.access_token = response["access_token"]
                return

            response = self.__get_tokens(
                args={
                    "refresh_token": response["refresh_token"],
                    "grant_type": "refresh_token",
                }
            )
        except Exception as exp:
            self.logger.warning(
                "If you got here you should to regenerate refresh token"
            )
            if code_auth is None:
                raise NotImplementedError(
                    "You should pass code_auth argument to save the new refresh and access tokens "
                    " (or get and save  them the first time) "
                ) from  exp
            response = self.__get_tokens(
                args={"code": code_auth, "grant_type": "authorization_code"}
            )

        self.access_token = response["access_token"]
        self.__save_tokens_s3(response)

    def get_headers(self):
        """init header for amocrm.api request"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token,
        }
        return headers

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
        self.auth()
        if not self.s3_client.path_exists(self.s3_client.root_dir):
            self.s3_client.create_dir(self.s3_client.root_dir)
        self.clear_s3_folder()  # clear old before loading

        url_base = self.args_api["amocrm_api_url"]
        cur_page = 1

        params = {}
        if self.date_modified_from is not None:
            self.logger.info("Uploading data with after %s ", self.date_modified_from)
            params["filter[updated_at][from]"] = int(
                self.date_modified_from.timestamp()
            )
        has_next = True
        while has_next and cur_page < PAGE_NUMBER_MAX:
            self.logger.info("Extracting page №%d", cur_page)
            file_path = self.__get_file_name(cur_page, self.batch_api)

            if self.with_offset == 1:
                url = url_base.format(limit=self.batch_api, page=cur_page)
            else:
                url = url_base

            objects = requests.get(url, headers=self.get_headers(), params=params)
            self.logger.info(objects.url)
            if objects.status_code == 204:
                self.logger.warning(
                    "Warning! API sent no result %d", objects.status_code
                )
                return

            limit_from_url = get_limit_from_url(objects)
            if "next" not in objects.json()["_links"]:
                has_next = False

            if limit_from_url != self.batch_api:
                logging.warning(
                    "Batch API: %d is too large, changing to default value %d",
                    self.batch_api,
                    limit_from_url,
                )
                self.batch_api = limit_from_url

            count_uploaded = len(process_json(objects.json(), self.entity))
            self.rows_to_upload += count_uploaded
            self.logger.info(
                "Saving data in the file %s, a number of rows %d, total number: %d",
                file_path,
                count_uploaded,
                self.rows_to_upload,
            )
            self.s3_client.create_file(file_path, objects.content)

            cur_page += 1
        self.logger.info(
            "Total number of rows received from API is %d", self.rows_to_upload
        )
