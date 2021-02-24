from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Any
from typing import List

from pydantic import BaseModel


class FilterType(Enum):
    IS = 1
    IS_NOT = 2
    IS_ONE_OF = 3
    IS_NOT_ONE_OF = 4
    IS_BETWEEN = 5
    IS_NOT_BETWEEN = 6
    EXISTS = 7
    DOES_NOT_EXIST = 8


class FilterClause(BaseModel):
    type: FilterType
    name: str
    value: Any = None


class Query(metaclass=ABCMeta):
    def __init__(self, topic: str):
        """
        构建面向topic的查询。

        :param topic: 数据所在的topic
        """

        self._topic = topic
        self._filters: List[FilterClause] = []
        self._page = None
        self._size = None

    @abstractmethod
    def get(self, data_id: str) -> dict:
        """
        返回指定数据

        :param data_id: 数据的ID
        """

    def field(self, name: str) -> 'FilterClauseBuilder':
        """
        基于筛选表达式检索数据。

        :param name: 筛选的字段名称
        """

        return FilterClauseBuilder(name, self)

    def paginate(self, page: int = 0, size: int = 10):
        """
        分页查询

        :param page: 分页的页码，从0开始
        :param size: 分页的大小
        """

        self._page = page
        self._size = size

    @abstractmethod
    def all(self, as_model=False) -> List[dict]:
        """
        返回命中查询的所有数据，默认进行了分页。
        """

    @abstractmethod
    def first(self, as_model=False) -> dict:
        """
        返回命中查询的第一条数据
        """


class FilterClauseBuilder:
    def __init__(self, name: str, query: Query):
        self._name = name
        self._query = query

    def is_(self, value: Any) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.IS,
                name=self._name,
                value=value,
            )
        )
        return self._query

    def is_not(self, value: Any) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.IS_NOT,
                name=self._name,
                value=value
            )
        )
        return self._query

    def is_one_of(self, *values: Any) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.IS_ONE_OF,
                name=self._name,
                value=list(values)
            )
        )
        return self._query

    def is_not_one_of(self, *values: Any) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.IS_NOT_ONE_OF,
                name=self._name,
                value=list(values)
            )
        )
        return self._query

    def is_between(self, lower_bound: Any = None, upper_bound: Any = None) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.IS_BETWEEN,
                name=self._name,
                value=(lower_bound, upper_bound),
            )
        )
        return self._query

    def is_not_between(self, lower_bound: Any = None, upper_bound: Any = None) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.IS_NOT_BETWEEN,
                name=self._name,
                value=(lower_bound, upper_bound),
            )
        )
        return self._query

    def exists(self) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.EXISTS,
                name=self._name,
            )
        )
        return self._query

    def does_not_exists(self) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.DOES_NOT_EXIST,
                name=self._name,
            )
        )
        return self._query
