import os
import re
from typing import Dict, List, Optional, Tuple

from lilili import __title__
from lilili.db.defs import Basis, License
from lilili.utils import determine_spdx, fetch_json


def find_github_owner_repo(url: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """Find the owner's name and repository name from the URL representing the GitHub
    repository.

    Parameters
    ----------
    url : Optional[str]
        Any string (expect it to be a URL).

    Returns
    -------
    owner : str or None
        Owner's name, or None if not found.
    repo : str or None
        Repository name, or None if not found.

    Examples
    --------
    >>> owner, repo = find_github_owner_repo("https://github.com/poyo46/lilili.git#foo")
    >>> assert owner == "poyo46"
    >>> assert repo == "lilili"

    >>> owner, repo = find_github_owner_repo("https://www.example.com")
    >>> assert owner is None
    >>> assert repo is None
    """
    if url is None:
        return None, None
    m = re.match(r"[^:/]+://github.com/(?P<owner>[^/]+)/(?P<repo>[^/#]+)", url)
    if m is None:
        return None, None
    repo = m.group("repo")
    if repo.endswith(".git"):
        repo = repo[:-4]
    return m.group("owner"), repo


def extract_github_repository_url(urls: List[str]) -> Optional[str]:
    """Extract a GitHub repository URL among the given URLs.

    Parameters
    ----------
    urls : List[str]
        A list of URLs.

    Returns
    -------
    Optional[str]
        GitHub repository URL, or None if not found.

    Notes
    -----
    If a URL is found, it will be normalized to the form
    ``https://github.com/{owner}/{repo}`` .

    Examples
    --------
    >>> urls = ["http://foo.jp", "http://github.com/poyo46/lilili#foo", "http://bar.jp"]
    >>> url = extract_github_repository_url(urls)
    >>> assert url == "https://github.com/poyo46/lilili"

    >>> assert extract_github_repository_url(["foo", "bar"]) is None
    """
    for url in urls:
        owner, repo = find_github_owner_repo(url)
        if owner is not None and repo is not None:
            return f"https://github.com/{owner}/{repo}"
    return None


class GithubApi:
    BASE_URL = "https://api.github.com"
    ACCESS_TOKEN = os.getenv(f"{__title__.upper()}_GITHUB_ACCESS_TOKEN")

    @staticmethod
    def get_headers() -> Dict[str, str]:
        if GithubApi.ACCESS_TOKEN is None:
            return {}
        else:
            return {"Authorization": "token " + GithubApi.ACCESS_TOKEN}


class GithubRepository:
    @staticmethod
    def find_licenses(github_url: str) -> List[License]:
        owner, repo = find_github_owner_repo(github_url)
        if owner is None or repo is None:
            return []
        licenses = []
        registered_license = GithubRepository.fetch_registered_license(owner, repo)
        if registered_license is not None:
            licenses.append(registered_license)
        # TODO: Implement other means (e.g., refer to package.json).
        return licenses

    @staticmethod
    def fetch_registered_license(owner: str, repo: str) -> Optional[License]:
        """Fetch a license that is explicitly registered in the repository.

        Parameters
        ----------
        owner : str
            Repository owner's name.
        repo : str
            Repository name.

        Returns
        -------
        license : License or None
            Registered license, or None if not found.

        See Also
        --------
        https://docs.github.com/en/rest/reference/licenses#get-the-license-for-a-repository
        """
        url = f"{GithubApi.BASE_URL}/repos/{owner}/{repo}/license"
        license_json = fetch_json(url, GithubApi.get_headers())
        if license_json is None:
            return None
        if "license" not in license_json.keys():
            return None
        spdx = determine_spdx(license_json["license"]["spdx_id"])
        if spdx is None:
            return None
        basis = Basis.GITHUB_LICENSES_API
        return License(spdx=spdx, basis=basis, source_url=url)
