from typing import Dict, List, Optional

from sqlalchemy.orm.session import Session

from lilili.apis.api import Api
from lilili.apis.github import extract_github_repository_url
from lilili.db.defs import Basis, Domain, License
from lilili.utils import determine_spdx, fetch_json


class RubygemsApi(Api):
    domain = Domain.RUBYGEMS
    BASE_URL = "https://rubygems.org/api/v1"

    def __init__(self, session: Session, name: str, version: str) -> None:
        super().__init__(session, name, version)
        self.exact_info_url = f"{RubygemsApi.BASE_URL}/versions/{name}.json"
        self.exact_info = None
        self.latest_info_url = f"{RubygemsApi.BASE_URL}/gems/{name}.json"
        self.latest_info = None

    def fetch_info(self) -> None:
        for info in fetch_json(self.exact_info_url) or []:
            if info["number"] == self.version:
                self.exact_info = info
                break
        self.latest_info = fetch_json(self.latest_info_url)

    def get_download_url(self) -> Optional[str]:
        return f"https://rubygems.org/gems/{self.name}-{self.version}.gem"

    def get_homepage(self) -> Optional[str]:
        # self.exact_info has no information about homepage.
        if self.latest_info is not None:
            return self.latest_info.get("homepage_uri", None)
        return None

    @staticmethod
    def _get_urls(info: Dict) -> List[str]:
        return [value for key, value in info.items() if key.endswith("_uri")]

    def get_github_url(self) -> Optional[str]:
        # self.exact_info has no information about github_url.
        if self.latest_info is None:
            return None
        urls = self._get_urls(self.latest_info)
        if "metadata" in self.latest_info:
            urls += self._get_urls(self.latest_info["metadata"])
        return extract_github_repository_url(urls)

    def get_exact_licenses(self) -> List[License]:
        if self.exact_info is None:
            return []
        basis = Basis.API_EXACT
        licenses = []
        for license_name in self.exact_info.get("licenses", []):
            spdx = determine_spdx(license_name)
            if spdx is not None:
                licenses.append(
                    License(spdx=spdx, basis=basis, source_url=self.exact_info_url)
                )
        return licenses

    def get_latest_licenses(self) -> List[License]:
        if self.latest_info is None:
            return []
        basis = Basis.API_LATEST
        licenses = []
        for license_name in self.latest_info.get("licenses", []):
            spdx = determine_spdx(license_name)
            if spdx is not None:
                licenses.append(
                    License(spdx=spdx, basis=basis, source_url=self.latest_info_url)
                )
        return licenses
