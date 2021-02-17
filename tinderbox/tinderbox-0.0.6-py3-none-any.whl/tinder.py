from pyspark.sql import DataFrame
from pyspark.sql import functions as f, Column
from pyspark.sql.window import Window

from tinderbox.smoke import Deffer, Columnable, get_name, DelayedCall


class DataFrameOperation(Deffer):

    @property
    def df(self) -> DataFrame:
        return self._tinder_context.get_df()

    def __init__(self, name, *args, **kwargs):
        self._name = name
        super(DataFrameOperation, self).__init__(*args, **kwargs)

    def exec(self):
        raise NotImplementedError()


class CompressRows(DataFrameOperation):
    def __init__(self, on: Columnable, order: Columnable, take: int = 1, with_rank: bool = None, **kwargs):
        """ Transformation that partitions the data in a window orders and ranks the data,
        and takes the first ranked item. Good for compressing incremental files into a usable data set.

        :param on: Column to partition on
        :param order: The order by, if a string is passed assumed desc(string).
        :param take: How many copies of a row should be in the result. When removing dupes from a dataframe
        typically this would b left at 1. Other use cases like finding the top 2 sales figure per Person
        take would be changed to 2.
        :param with_rank: Include the ranking column or not, if not set (None) with_rank will default to
        false when take is 1, if take is over 1 it will default to true.
        """
        super().__init__(f'CompressOn{on}', **kwargs)

        self.on = col(on)
        self.order = col(order)
        self.with_rank = with_rank if with_rank is not None else take > 1
        self.rng = list(range(1, 1 + take))

    def exec(self):
        if not self.with_rank:
            self.with_rank = True
        u_on = self._unravel(self.on)
        u_order = self._unravel(self.order)
        windowSpec = Window.partitionBy(u_on).orderBy(u_order)

        return self.df.withColumn("row_number", f.row_number().over(windowSpec)). \
            where(f.col("row_number").isin(self.rng))


class ScalarAggregation(DataFrameOperation):

    def __init__(self, agg_col: Columnable, *args, **kwargs):
        """ Returns a single value after runniing an aggregation on a column of a dataframe.
        This can be used directly and it is also the basis to make simple aggregators
        like max, min.

        :param func:
        :param a_name:
        :param col:
        :return:
        """

        super().__init__(self.get_spark_function().__name__, *args, **kwargs)
        self._aggregate_on = col(agg_col)

    @property
    def spark_function(self):
        return self.get_spark_function()

    def get_spark_function(self):
        raise NotImplementedError()

    def exec(self):
        me_col = self._unravel(self._aggregate_on)
        agg_fun = self.df.agg(self.spark_function(me_col)).collect()[0][0]
        return f.lit(agg_fun)


class MaxValue(ScalarAggregation):

    def get_spark_function(self):
        return f.max


class MinValue(ScalarAggregation):

    def get_spark_function(self):
        return f.min


class AddColumn(DataFrameOperation):

    def __init__(self, col_name, expr, *args, **kwargs):
        super().__init__(col_name, *args, **kwargs)
        self._expr = expr

    def exec(self) -> DataFrameOperation:
        eval_expr = self._unravel(self._expr)
        return self.df.withColumn(self._name, eval_expr)


def col(wannabe_column: Columnable, tinder_context=None) -> Column:
    if isinstance(wannabe_column, (Column, Deffer)):
        return wannabe_column
    c_name = get_name(wannabe_column)
    try:
        return f.col(c_name)
    except:
        return DelayedCall(f.col, get_name(wannabe_column), _tinder=tinder_context)
