from collections import Mapping

from .page_params import PageParams
from .sort_params import SortParams


class ListParams(Mapping):
    """
    Parameters for lists (sort, pagination, query)
    """

    __dict: dict = {}

    def __init__(
        self, sort: SortParams = None, page: PageParams = None, query: str = None
    ):
        """
        :param sort: sort params
        :param page: pagination params
        :param query: search query;
        format `foo="some value" and ($baz="other value" or $bar="third value")`;
        example `$id="123"`
        """
        self.__dict["sort"] = sort
        self.__dict["page"] = page
        self.__dict["query"] = query

    def __getitem__(self, k):
        return self.__dict.__getitem__(k)

    def __len__(self):
        return self.__dict.__len__()

    def __iter__(self):
        return self.__dict.__iter__()

    @property
    def page(self) -> PageParams:
        return self.__dict.get("page")

    @property
    def sort(self) -> SortParams:
        return self.__dict.get("sort")

    @property
    def query(self) -> str:
        return self.__dict.get("query")
