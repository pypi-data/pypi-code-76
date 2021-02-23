import json
import os
import re
from enum import Enum, auto
from typing import List, Optional, Union
from dataclasses import dataclass


class SQLFunction(Enum):
    MAX = auto()
    MIN = auto()
    AVG = auto()
    COUNT = auto()
    SUM = auto()


class TimeDimensionGranularity(Enum):
    year = auto()
    quarter = auto()
    month = auto()
    week = auto()
    day = auto()
    hour = auto()
    interval = auto()


@dataclass
class Field:
    column: str
    aggregation: Optional[Union[SQLFunction, TimeDimensionGranularity, str]] = None
    dataset: Optional[str] = None
    entityType: Optional[str] = None
    alias: Optional[str] = None


class SQLOperator(Enum):
    EQ = auto()
    GOE = auto()
    GT = auto()
    LOE = auto()
    LT = auto()
    IN = auto()
    NOT_IN = auto()


@dataclass
class Condition:
    field: Field
    operator: Union[SQLOperator, str]
    value: List[Union[float, str]]
    type: Optional[str] = None


class SQLSorting(Enum):
    DESC = auto()
    ASC = auto()


@dataclass
class Sorting:
    field: str
    order: SQLSorting


@dataclass
class Setting:
    type: str


@dataclass
class Component:
    component_type: str
    setting: Optional[List[Setting]] = None


@dataclass
class From:
    dataset: str


@dataclass
class Query:
    fields: List[Field]
    datasets: Optional[List[From]] = None
    where: Optional[List[Condition]] = None
    orderBy: Optional[List[Sorting]] = None
    limit: Optional[Union[int, str]] = None

    def to_sql(self, dataset: str = None):
        sql = "SELECT {} FROM {}"

        fields_with_agg = []
        for field in self.fields:
            column = field.column
            if field.aggregation is not None:
                if isinstance(field.aggregation, SQLFunction) or isinstance(field.aggregation, TimeDimensionGranularity):
                    field_with_agg = field.aggregation.name + " ( " + column + " )"
                else:
                    field_with_agg = field.aggregation + " ( " + column + " )"
            else:
                field_with_agg = column
            if field.alias is not None:
                field_with_agg += " AS " + field.alias
            fields_with_agg.append(field_with_agg)

        formatted_fields = ", ".join(fields_with_agg)

        froms_array = []
        if self.datasets is not None:
            for f in self.datasets:
                froms_array.append(f.dataset)
            table = ", ".join(froms_array)
        elif dataset is not None:
            table = dataset
        else:
            table = "{{dataset.A}}"
        sql = sql.format(formatted_fields, table)

        where_conditions = []
        if self.where is not None:
            sql_where = " WHERE {}"

            for condition in self.where:
                vars = []
                for var in condition.value:
                    vars.append(str(var))
                formatted_value = "( " + ", ".join(vars) + " )"
                if isinstance(condition.operator, str):
                    operator = condition.operator
                else:
                    operator = condition.operator.name
                    if operator == "GOE":
                        operator = ">="
                    elif operator == "LOE":
                        operator = "<="
                    elif operator == "EQ":
                        operator = "=="
                    elif operator == "GT":
                        operator = ">"
                    elif operator == "LT":
                        operator = "<"
                field_with_agg = condition.field.column
                if condition.field.aggregation is not None:
                    if isinstance(condition.field.aggregation, SQLFunction) or isinstance(condition.field.aggregation, TimeDimensionGranularity):
                        field_with_agg = condition.field.aggregation.name + " ( " + field_with_agg + " )"
                    else:
                        field_with_agg = condition.field.aggregation + " ( " + field_with_agg + " )"
                else:
                    field_with_agg = field_with_agg
                where_condition = (
                        field_with_agg + " " + operator + " " + str(formatted_value)
                )
                where_conditions.append(where_condition)
            if where_conditions:
                formatted_where_conditions = " AND ".join(where_conditions)
                sql_where = sql_where.format(formatted_where_conditions)
                sql += sql_where

        sorting_conditions = []
        if self.orderBy is not None:
            sql_orderby = " ORDER BY {}"

            for sorting in self.orderBy:
                sort_order = sorting.order.name
                sort_condition = sorting.field + " " + sort_order
                sorting_conditions.append(sort_condition)

            formatted_sorting = ", ".join(sorting_conditions)
            sql_orderby = sql_orderby.format(formatted_sorting)
            sql += sql_orderby

        if self.limit is not None:
            sql += " LIMIT " + str(self.limit)

        return sql


@dataclass
class SmartQuery:
    queries: List[Query]
    components: Optional[List[Component]] = None  # use this for of charts
    javascript: Optional[List[str]] = None

    @staticmethod
    def _get_tokens():
        f = open(os.path.join(os.path.dirname(__file__), "askdata_config", "compression_tokens.json"))
        comp_tokens = json.load(f)
        f.close()
        return comp_tokens

    @staticmethod
    def compress(smartquery_json: str):
        comp_tokens = SmartQuery._get_tokens()
        for token in comp_tokens:
            extended = token['decode']
            code = token['code']
            if extended in smartquery_json:
                smartquery_json = re.sub(r"\b"+extended+r"\b", code, smartquery_json)
        return smartquery_json

    @staticmethod
    def decompress(smartquery_json: str):
        comp_tokens = SmartQuery._get_tokens()
        for token in comp_tokens:
            code = token['code']
            decode = token['decode']
            if code in smartquery_json:
                smartquery_json = re.sub(r"\b"+code+r"\b", decode, smartquery_json)
        return smartquery_json
