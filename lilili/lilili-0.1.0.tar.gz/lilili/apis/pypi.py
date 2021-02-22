from typing import Dict, List, Optional

from sqlalchemy.orm.session import Session

from lilili.apis.api import Api
from lilili.apis.github import extract_github_repository_url
from lilili.db.defs import Basis, Domain, License
from lilili.utils import determine_spdx, fetch_json


class PypiApi(Api):
    domain = Domain.PYPI
    BASE_URL = "https://pypi.org/pypi"

    def __init__(self, session: Session, name: str, version: str) -> None:
        super().__init__(session, name, version)
        self.exact_info_url = f"{PypiApi.BASE_URL}/{name}/{version}/json"
        self.exact_info = None
        self.latest_info_url = f"{PypiApi.BASE_URL}/{name}/json"
        self.latest_info = None

    def fetch_info(self) -> None:
        self.exact_info = fetch_json(self.exact_info_url)
        self.latest_info = fetch_json(self.latest_info_url)

    def get_download_url(self) -> Optional[str]:
        if self.exact_info is None:
            return None
        return self.exact_info["urls"][0]["url"]

    def get_homepage(self) -> Optional[str]:
        homepage = None
        if self.exact_info is not None:
            homepage = self.exact_info["info"]["home_page"]
        if homepage is None and self.latest_info is not None:
            homepage = self.latest_info["info"]["home_page"]
        return homepage

    def _github_url(self, info: Dict) -> Optional[str]:
        urls = [self.get_homepage(), info["project_url"]]

        project_urls = info.get("project_urls", None)
        if project_urls is None:
            return extract_github_repository_url(urls)

        urls += list(project_urls.values())
        return extract_github_repository_url(urls)

    def get_github_url(self) -> Optional[str]:
        url = None
        if self.exact_info is not None:
            url = self._github_url(self.exact_info["info"])
        if url is None and self.latest_info is not None:
            url = self._github_url(self.latest_info["info"])
        return url

    def get_exact_licenses(self) -> List[License]:
        if self.exact_info is None:
            return []
        license_name = self.exact_info["info"]["license"]
        spdx = determine_spdx(license_name)
        if spdx is None:
            return []
        basis = Basis.API_EXACT
        return [License(spdx=spdx, basis=basis, source_url=self.exact_info_url)]

    def get_latest_licenses(self) -> List[License]:
        if self.latest_info is None:
            return []
        license_name = self.latest_info["info"]["license"]
        spdx = determine_spdx(license_name)
        if spdx is None:
            return []
        basis = Basis.API_LATEST
        return [License(spdx=spdx, basis=basis, source_url=self.latest_info_url)]
