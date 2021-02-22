from abc import ABC, abstractmethod
from logging import INFO, getLogger

from user_agent import generate_user_agent

logger = getLogger()
logger.setLevel(INFO)


class RequestBaseDownloader(ABC):
    def __init__(self, header: dict = None, proxy: dict = None):
        self._header = header or self.custom_header
        self.proxies = proxy

    @abstractmethod
    def get(self, *args, **kwargs):
        """Need to be implemented"""

    @abstractmethod
    def post(self, *args, **kwargs):
        """Need to be implemented"""

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, headers: dict):
        self._header = headers

    @property
    def custom_header(self):
        return {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/84.0.4147.125 "
                "Safari/537.36"
            ),
        }

    @property
    def random_user_agent(self):
        return generate_user_agent()
