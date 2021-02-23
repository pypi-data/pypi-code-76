from .common import PyBinaryScalarFunctionBatchOp as _PyBinaryScalarFunctionBatchOp
from .common import PyBinaryTableFunctionBatchOp as _PyBinaryTableFunctionBatchOp
from ..batch import BatchOperator
from ..py4j_util import get_java_class
from ..udf.utils import do_set_op_udf, do_set_op_udtf

__all__ = ['UDFBatchOp', 'UDTFBatchOp', 'TableSourceBatchOp']


class UDFBatchOp(_PyBinaryScalarFunctionBatchOp):
    def __init__(self, *args, **kwargs):
        super(UDFBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFunc(self, val):
        """
        set UDF: object with eval attribute, lambda function, or PyFlink udf object
        """
        return do_set_op_udf(self, val)


class UDTFBatchOp(_PyBinaryTableFunctionBatchOp):
    def __init__(self, *args, **kwargs):
        super(UDTFBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFunc(self, val):
        """
        set UDTF: object with eval attribute or lambda function
        """
        return do_set_op_udtf(self, val)


class TableSourceBatchOp(BatchOperator):
    def __init__(self, table, *args, **kwargs):
        from pyflink.table import Table
        if not isinstance(table, Table):
            raise ValueError("Invalid table: only accept PyFlink Table")

        table_source_batch_op_cls = get_java_class("com.alibaba.alink.operator.batch.source.TableSourceBatchOp")
        j_op = table_source_batch_op_cls(table._j_table)
        super(TableSourceBatchOp, self).__init__(j_op=j_op, *args, **kwargs)
        pass
