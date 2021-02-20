# -*- coding: utf-8 -*-

import abc
from typing import List, Union

__doc__ = """The base class.
"""


class Scraper(abc.ABC):
    """The base scraper class.
    """

    def __init__(self, *args, **kwargs):
        self._url = None

    @property
    def url(self) -> Union[None, str, List[str]]:
        """The url object.

        Returns
        -------
        Union[None, str, List[str]]
            The url object.

        """
        return self._url

    @url.setter
    def url(self, val: Union[str, List[str]]) -> None:
        """Set a new url or a list of urls.

        Parameters
        ----------
        val : Union[str, List[str]]
            A single url or a list of urls.

        """
        self._url = val

    @abc.abstractmethod
    def load(self, url: Union[str, List[str]]):
        """Abstract method for loading url content.
        """

    @abc.abstractmethod
    def parse(self):
        """Abstract method for parsing url content.
        """
