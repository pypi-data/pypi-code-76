#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyflink.table import DataTypes

from .udtf import udtf, TableFunction
from ..common.utils.packages import is_flink_1_9

if not is_flink_1_9():
    from pyflink.table.udf import udf, ScalarFunction
else:
    from .udf import udf, ScalarFunction

__all__ = ["udf", "udtf", "ScalarFunction", "TableFunction", "DataTypes"]
