__version__ = '0.1.2'

import datetime
import logging
import os
from IPython.core import magic_arguments
from IPython.core.magic import Magics
from pyspark.sql.utils import AnalysisException
from pyspark.sql.dataframe import DataFrame

class DoraContext:
    def __init__(self,spark,debug=False):
        self.logger = logging.getLogger()
        log_name = f"{datetime.datetime.today().strftime('%Y%m%d%I%M%S')}"
        fhandler = logging.FileHandler(filename=f"/dora/logs/{log_name}")
        shandler = logging.StreamHandler()
        fhandler.setFormatter(logging.Formatter('%(asctime)s|%(levelname)s|%(funcName)s|%(message)s'))
        shandler.setFormatter(logging.Formatter('%(levelname)s:%(message)s'))
        self.logger.addHandler(fhandler)
        self.logger.addHandler(shandler)
        self.logger.setLevel(getattr(logging, os.environ.get('LOG_LEVEL','INFO')))
        self.spark = spark
        self.verbose = debug
    
    def sql(self, query, **kwargs):
        self.verbose = kwargs.get("verbose")
        self.logger.debug('sql:parameters:%s',kwargs, )
        time_before_spark = datetime.datetime.now()
        try:
            spark_data_frame = self.spark.sql(query)
            return spark_data_frame
        except AnalysisException as analysis_exception:
            self.logger.error(analysis_exception)
            return None
        finally:
            if self.verbose:
                self.logger.info("Execution Time: %s", (datetime.datetime.now() - time_before_spark).total_seconds(), )

class DoraMagic(Magics):
    from IPython.core.magic import register_cell_magic
    ipython  = get_ipython()
    def __init__(self, DoraContext):
        self.isa = DoraContext
        self.ipython.register_magic_function(self.sql, 'cell')

    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--verbose', '-v',action='store_true',help='Print Debug messages')
    @magic_arguments.argument('--limit', '-l', type=int, default=100, help='Show limit')
    @magic_arguments.argument('--out', '-o',help='The variable to return the results in')
    def sql(self, line, query):
        args = magic_arguments.parse_argstring(self.sql, line)
        args = vars(args)
        if args.get("out") is None:
            response = self.isa.sql(query,**args)
            if isinstance(response, DataFrame):
                return response.limit(args.get("limit")).toPandas()
            return response
        else:
            response = self.isa.sql(query,**args)
            self.ipython.user_ns[args.get("out")] = response
            return response

if __name__ == "__main__":
    dora = DoraContext(spark)
    DoraMagic(dora)
