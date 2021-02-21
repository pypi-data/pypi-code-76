import typing

import pandas as pd
from sqlalchemy import Column, DateTime, and_, func, select

from bakplane.extensions.base import (
    ReadRequestBuildingBlocks,
    Modifier,
    DataStoreHelper,
)


class NearestModifier(Modifier):
    NEAREST_COLUMN_NAME = "nearest"

    def __init__(
        self,
        n: int,
        partition_fields: typing.List[str],
        ordered_fields: typing.List[typing.Tuple[str, str]],
    ):
        self.partition_fields = partition_fields
        self.ordered_fields = ordered_fields
        self.n = n

    def execute(
        self, r: ReadRequestBuildingBlocks, h: DataStoreHelper
    ) -> ReadRequestBuildingBlocks:

        if r.modifier_context and "frequency" in r.modifier_context:
            frequency_tbl = r.modifier_context["frequency"]["table"]
            column_name = FrequencyModifier.FREQUENCY_COLUMN_NAME
        elif r.effective_dating_table is not None:
            frequency_tbl = r.effective_dating_table
            column_name = "dt"
        elif r.valid_dating_table is not None:
            frequency_tbl = r.valid_dating_table
            column_name = "dt"
        else:
            raise ValueError(
                "Building blocks do not contain a frequency table."
            )

        p = [r.asset_table.c.get(x) for x in self.partition_fields] + [
            frequency_tbl.c.get(column_name)
        ]
        o = [
            r.asset_table.c.get(x[0]).desc()
            if x[1] == "desc"
            else r.asset_table.c.get(x[0]).desc()
            for x in self.ordered_fields
        ]

        r.columns.append(
            func.row_number()
            .over(partition_by=p, order_by=o)
            .label(NearestModifier.NEAREST_COLUMN_NAME)
        )
        cte = (
            select(r.columns)
            .select_from(r.selectable)
            .where(and_(*r.constraints))
            .cte("nearest")
        )

        r.selectable = cte
        r.columns = [cte.c.get(x.name) for x in r.columns]
        r.constraints = [
            cte.c.get(NearestModifier.NEAREST_COLUMN_NAME) <= self.n
        ]

        return r


class FrequencyModifier(Modifier):
    FREQUENCY_COLUMN_NAME = "frequency_dt"
    PREFIX_NAME = "t_frequency"

    def __init__(self, frequency: str):
        self.frequency = frequency

    def execute(
        self, r: ReadRequestBuildingBlocks, h: DataStoreHelper
    ) -> ReadRequestBuildingBlocks:

        if r.effective_dating_table is not None:
            raise ValueError(
                "A frequency modifier cannot be applied to non range queries."
            )

        ranges = pd.bdate_range(
            start=r.effective_start_dt,
            end=r.effective_end_dt,
            freq=self.frequency,
        )

        tbl = h.create_temporary_table(
            prefix=FrequencyModifier.PREFIX_NAME,
            columns=[
                Column(
                    FrequencyModifier.FREQUENCY_COLUMN_NAME,
                    DateTime,
                    nullable=False,
                )
            ],
            rows=[
                {FrequencyModifier.FREQUENCY_COLUMN_NAME: x.to_pydatetime()}
                for x in ranges
            ],
        )

        r.selectable = r.selectable.join(
            tbl,
            and_(
                tbl.c.get(FrequencyModifier.FREQUENCY_COLUMN_NAME)
                >= r.asset_table.c.effective_start_dt,
                tbl.c.get(FrequencyModifier.FREQUENCY_COLUMN_NAME)
                < r.asset_table.c.effective_end_dt,
            ),
        )

        r.columns.append(tbl.c.get(FrequencyModifier.FREQUENCY_COLUMN_NAME))

        if r.modifier_context is None:
            r.modifier_context = {}

        r.modifier_context["frequency"] = {"table": tbl}

        return r
