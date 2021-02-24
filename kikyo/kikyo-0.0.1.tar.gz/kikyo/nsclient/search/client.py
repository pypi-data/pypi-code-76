from abc import ABCMeta, abstractmethod

from kikyo.nsclient.search.query import Query


class SearchClient(metaclass=ABCMeta):
    """
    提供全文检索服务
    """

    @abstractmethod
    def query(self, topic: str) -> Query:
        """
        对指定topic构建查询。

        :param topic: topic名称
        """
