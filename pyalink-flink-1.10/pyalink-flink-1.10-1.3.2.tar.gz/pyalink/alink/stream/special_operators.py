from .common import FtrlPredictStreamOp as _FtrlPredictStreamOp
from .common import FtrlTrainStreamOp as _FtrlTrainStreamOp
from .common import PyBinaryScalarFunctionStreamOp as _PyBinaryScalarFunctionStreamOp
from .common import PyBinaryTableFunctionStreamOp as _PyBinaryTableFunctionStreamOp
from ..py4j_util import get_java_class
from ..stream import StreamOperator
from ..udf.utils import do_set_op_udf, do_set_op_udtf

__all__ = ['UDFStreamOp', 'UDTFStreamOp', 'FtrlTrainStreamOp', 'FtrlPredictStreamOp', 'TableSourceStreamOp']


class UDFStreamOp(_PyBinaryScalarFunctionStreamOp):
    def __init__(self, *args, **kwargs):
        super(UDFStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFunc(self, val):
        """
        set UDF: object with eval attribute, lambda function, or PyFlink udf object
        """
        return do_set_op_udf(self, val)


class UDTFStreamOp(_PyBinaryTableFunctionStreamOp):
    def __init__(self, *args, **kwargs):
        super(UDTFStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFunc(self, val):
        """
        set UDTF: object with eval attribute or lambda function
        """
        return do_set_op_udtf(self, val)


class FtrlTrainStreamOp(_FtrlTrainStreamOp):
    def __init__(self, model, *args, **kwargs):
        self.model = model
        super(FtrlTrainStreamOp, self).__init__(model=model, *args, **kwargs)
        pass

    def linkFrom(self, *args):
        self.inputs = [self.model] + [x for x in args]
        return super(FtrlTrainStreamOp, self).linkFrom(*args)


class FtrlPredictStreamOp(_FtrlPredictStreamOp):
    def __init__(self, model, *args, **kwargs):
        self.model = model
        super(FtrlPredictStreamOp, self).__init__(model=model, *args, **kwargs)
        pass

    def linkFrom(self, *args):
        self.inputs = [self.model] + [x for x in args]
        return super(FtrlPredictStreamOp, self).linkFrom(*args)


class TableSourceStreamOp(StreamOperator):
    def __init__(self, table, *args, **kwargs):
        from pyflink.table import Table
        if not isinstance(table, Table):
            raise ValueError("Invalid table: only accept PyFlink Table")
        table_source_stream_op_cls = get_java_class("com.alibaba.alink.operator.stream.source.TableSourceStreamOp")
        j_op = table_source_stream_op_cls(table._j_table)
        super(TableSourceStreamOp, self).__init__(j_op=j_op, *args, **kwargs)
        pass
