""" Handles the parametrization of fetchers of known data sources """

import os
import re

from weasel_data_sources.releases import CDNJSFetcher, GitFetcher
from weasel_data_sources.vulnerabilities import CVESearchVulnFetcher

from .sources import SOURCES


class TechnologyBuilder:
    """
    A builder to create TechnologyHandler instances
    """

    def __init__(self, git_repository_storage, cvesearch_api_url=None):
        self._git_storage = git_repository_storage
        self._cvesearch_api_base = cvesearch_api_url

    def create_technology_handler(self, technology_name: str):
        """
        Creates a technology handler instance corresponding to the given technology name
        :param technology_name: The name of the technology
        """
        if technology_name in SOURCES:
            return TechnologyHandler(
                technology_name, self._git_storage, self._cvesearch_api_base
            )

        raise ValueError('Technology "{}" is not in known data sources')

    def get_all_technologies(self) -> dict:
        """
        Returns a dict of `TechnologyHandler` instances for all known data sources
        """
        return {name: self.create_technology_handler(name) for name in SOURCES}


class TechnologyHandler:
    """
    Handles the different data sources that are known for a technology
    and initializes corresponding fetchers.
    """

    def __init__(self, name: str, git_base_storage: str, cvesearch_api_url=None):
        self.name = name
        self.git_tag_regex = (
            SOURCES[self.name]["git_tag_regex"]
            if "git_tag_regex" in SOURCES[self.name]
            else None
        )
        self.git_tag_substitute = (
            SOURCES[self.name]["git_tag_substitute"]
            if "git_tag_substitute" in SOURCES[self.name]
            else None
        )

        self.cvesearch_api_base = cvesearch_api_url
        self.local_git_path = os.path.join(git_base_storage, self.safe_name)

    @property
    def safe_name(self):
        """
        The technology name in a form that is safe to use as a file name
        """
        tmp = self.name.strip().replace(" ", "_")
        return re.sub(r"(?u)[^-\w.]", "", tmp)

    @property
    def has_git(self):
        """
        True if a git repository for this technology is given in the known data sources
        """
        return SOURCES[self.name]["git"] is not None

    @property
    def has_cdnjs(self):
        """
        True if a cdnjs library name for this technology is given in the known data sources
        """
        return SOURCES[self.name]["cdnjs"] is not None

    @property
    def has_cpe(self):
        """
        True if the CPE for this technology is known
        """
        return SOURCES[self.name]["cpe"] is not None

    def create_git_fetcher(self) -> GitFetcher:
        """
        Initializes and returns a `GitFetcher` instance for the technology
        :raise ValueError: If their is no known git repository for this technology
        """
        if not self.has_git:
            raise ValueError("There is no known git repo for {}".format(self.name))

        return GitFetcher(
            SOURCES[self.name]["git"],
            self.local_git_path,
            self.git_tag_regex,
            self.git_tag_substitute,
        )

    def create_cdnjs_fetcher(self) -> CDNJSFetcher:
        """
        Initializes and returns a `CDNJSFetcher` instance for the technology
        :raise ValueError: If there is no known cdnjs library name for this technology
        """
        if not self.has_cdnjs:
            raise ValueError("There is no known cdnjs library for {}".format(self.name))

        return CDNJSFetcher(SOURCES[self.name]["cdnjs"])

    def create_cvesearch_vulnfetcher(self) -> CVESearchVulnFetcher:
        """
        Initializes and returns a `CVESearchVulnFetcher` instance for the technology
        :raise ValueError: If there is no known CPE for this technology or no CVESearch instance
        """
        if not self.has_cpe:
            raise ValueError("There is no known CPE for {}".format(self.name))

        if not self.cvesearch_api_base:
            raise ValueError("No CVESearch instance was defined")

        return CVESearchVulnFetcher(SOURCES[self.name]["cpe"], self.cvesearch_api_base)
