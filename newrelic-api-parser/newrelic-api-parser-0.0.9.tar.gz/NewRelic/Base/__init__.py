import requests
import logging

from NewRelic import Config

logger = logging.getLogger()

class BaseNewRelic:

    def __init__(self, API_KEY: str = None):
        self.headers = {
            "X-Api-Key": API_KEY
        }
        self.BASE_URI = Config.BASE_URI

    def get_list(self):
        """
        override with your implementation of get list
        """
        pass

    def show(self):
        """
        override with your implementation of show
        """
        pass

    def create(self):
        """
        override with your implementation of create
        """
        pass

    def update(self):
        """
        override with your implementation of update
        """
        pass

    def delete(self, url: str):
        """
        override with your implementation to delete
        """
        try:
            response = requests.delete(url)
        except Exception as ex:
            self.handle_exception(ex)
            return None

    def get_data(self, url: str, options: dict = {}):
        try:
            response = requests.get(url, headers=self.headers, data=options)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as ex:
            self.handle_exception(ex)
            return None

    def fetch_data(self):
        pass

    def post_data(self, url: str, data: dict = {}):
        try:
            response = requests.post(url, headers=self.headers, data = data)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as ex:
            self.handle_exception(ex)
            return None

    def handle_exception(self, excep):
        logger.exception("Error processing new relic request: " + str(excep))