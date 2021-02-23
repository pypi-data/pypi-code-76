#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyflink.table import DataTypes

from ..common.utils.packages import is_flink_1_9

if not is_flink_1_9():
    from pyflink.table.udf import udf, ScalarFunction, udtf, TableFunction
    from pyflink.table.types import DataTypes
else:
    from .udtf import udtf, TableFunction
    from .udf import udf, ScalarFunction

__all__ = ["udf", "udtf", "ScalarFunction", "TableFunction", "DataTypes"]
