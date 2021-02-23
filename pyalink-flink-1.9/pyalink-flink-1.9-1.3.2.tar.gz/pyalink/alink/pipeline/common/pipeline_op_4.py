#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import Estimator, Transformer, Model, TuningEvaluator
from ..tuning.base import BaseGridSearch, BaseRandomSearch
from ..lazy.has_lazy_print_model_info import HasLazyPrintModelInfo
from ..lazy.has_lazy_print_train_info import HasLazyPrintTrainInfo
from ..local_predictor import LocalPredictable


class VectorApproxNearestNeighbor(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.similarity.VectorApproxNearestNeighbor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorApproxNearestNeighbor, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setNumHashTables(self, val):
        return self._add_param('numHashTables', val)

    def setNumProjectionsPerTable(self, val):
        return self._add_param('numProjectionsPerTable', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setProjectionWidth(self, val):
        return self._add_param('projectionWidth', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setSolver(self, val):
        return self._add_param('solver', val)

    def setTopN(self, val):
        return self._add_param('topN', val)


class VectorApproxNearestNeighborModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.similarity.VectorApproxNearestNeighborModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorApproxNearestNeighborModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)


class VectorAssembler(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorAssembler'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorAssembler, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class VectorElementwiseProduct(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorElementwiseProduct'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorElementwiseProduct, self).__init__(*args, **kwargs)
        pass

    def setScalingVector(self, val):
        return self._add_param('scalingVector', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class VectorImputer(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorImputer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorImputer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setFillValue(self, val):
        return self._add_param('fillValue', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setStrategy(self, val):
        return self._add_param('strategy', val)


class VectorImputerModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorImputerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorImputerModel, self).__init__(*args, **kwargs)
        pass

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)


class VectorInteraction(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorInteraction'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorInteraction, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class VectorMaxAbsScaler(Estimator, HasLazyPrintModelInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorMaxAbsScaler'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMaxAbsScaler, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)


class VectorMaxAbsScalerModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorMaxAbsScalerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMaxAbsScalerModel, self).__init__(*args, **kwargs)
        pass

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)


class VectorMinMaxScaler(Estimator, HasLazyPrintModelInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorMinMaxScaler'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMinMaxScaler, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMax(self, val):
        return self._add_param('max', val)

    def setMin(self, val):
        return self._add_param('min', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)


class VectorMinMaxScalerModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorMinMaxScalerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMinMaxScalerModel, self).__init__(*args, **kwargs)
        pass

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)


class VectorNearestNeighbor(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.similarity.VectorNearestNeighbor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorNearestNeighbor, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)


class VectorNearestNeighborModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.similarity.VectorNearestNeighborModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorNearestNeighborModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)


class VectorNormalizer(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorNormalizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorNormalizer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setP(self, val):
        return self._add_param('p', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class VectorPolynomialExpand(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorPolynomialExpand'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorPolynomialExpand, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setDegree(self, val):
        return self._add_param('degree', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class VectorSizeHint(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorSizeHint'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorSizeHint, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setSize(self, val):
        return self._add_param('size', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class VectorSlicer(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorSlicer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorSlicer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setIndices(self, val):
        return self._add_param('indices', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class VectorStandardScaler(Estimator, HasLazyPrintModelInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorStandardScaler'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorStandardScaler, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setWithMean(self, val):
        return self._add_param('withMean', val)

    def setWithStd(self, val):
        return self._add_param('withStd', val)


class VectorStandardScalerModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.vector.VectorStandardScalerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorStandardScalerModel, self).__init__(*args, **kwargs)
        pass

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)


class VectorToColumns(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.VectorToColumns'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToColumns, self).__init__(*args, **kwargs)
        pass

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class VectorToCsv(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.VectorToCsv'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToCsv, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class VectorToJson(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.VectorToJson'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToJson, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class VectorToKv(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.VectorToKv'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToKv, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class Word2Vec(Estimator, HasLazyPrintTrainInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.Word2Vec'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Word2Vec, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setMinCount(self, val):
        return self._add_param('minCount', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setPredMethod(self, val):
        return self._add_param('predMethod', val)

    def setRandomWindow(self, val):
        return self._add_param('randomWindow', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)

    def setWindow(self, val):
        return self._add_param('window', val)

    def setWordDelimiter(self, val):
        return self._add_param('wordDelimiter', val)


class Word2VecModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.Word2VecModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Word2VecModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setPredMethod(self, val):
        return self._add_param('predMethod', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setWordDelimiter(self, val):
        return self._add_param('wordDelimiter', val)

