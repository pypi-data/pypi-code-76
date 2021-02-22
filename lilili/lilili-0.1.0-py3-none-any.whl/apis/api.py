import logging
from abc import ABCMeta, abstractmethod
from typing import List, Optional

from sqlalchemy.orm.session import Session

from lilili.apis.github import GithubRepository
from lilili.db.defs import Library, License
from lilili.db.helpers import add_library, query_library

logger = logging.getLogger(__name__)


class Api(metaclass=ABCMeta):
    def __init__(self, session: Session, name: str, version: str) -> None:
        self.session = session
        self.name = name
        self.version = version

    def find_library(self) -> Library:
        lib = query_library(self.session, self.domain, self.name, self.version)
        if lib is not None:
            logger.debug(f"found in db: {self.name} {self.version}")
            return lib

        self.fetch_info()

        lib = Library(
            domain=self.domain,
            name=self.name,
            version=self.version,
            download_url=self.get_download_url(),
            homepage=self.get_homepage(),
            git_url=self.get_github_url(),
        )
        lib.licenses = self.find_licenses()

        licenses_are_ok = all([lic.spdx is not None for lic in lib.licenses])
        urls_are_ok = lib.download_url is not None and lib.homepage is not None
        if licenses_are_ok and urls_are_ok:
            # If enough information is obtained, it is saved in the database.
            add_library(self.session, lib)

        return lib

    @abstractmethod
    def fetch_info(self) -> None:
        pass

    @abstractmethod
    def get_download_url(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_homepage(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_github_url(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_exact_licenses(self) -> List[License]:
        pass

    @abstractmethod
    def get_latest_licenses(self) -> List[License]:
        pass

    def find_licenses(self) -> List[License]:
        licenses = self.get_exact_licenses()
        if len(licenses) != 0:
            return licenses

        licenses += self.get_latest_licenses()
        licenses += GithubRepository.find_licenses(self.get_github_url())
        if len(licenses) == 0:
            licenses = [License(spdx=None, basis=None, source_url=None)]
        return licenses
