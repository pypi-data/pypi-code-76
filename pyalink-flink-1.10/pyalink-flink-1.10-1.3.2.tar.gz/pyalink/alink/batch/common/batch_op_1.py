#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import BatchOperator, BaseSinkBatchOp
from ..lazy.extract_model_info_batch_op import ExtractModelInfoBatchOp
from ..lazy.with_model_info_batch_op import WithModelInfoBatchOp
from ..lazy.with_train_info import WithTrainInfo


class AftSurvivalRegModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.AftSurvivalRegModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AftSurvivalRegModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class AftSurvivalRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.AftSurvivalRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AftSurvivalRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setQuantileProbabilities(self, val):
        return self._add_param('quantileProbabilities', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class AftSurvivalRegTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.AftSurvivalRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AftSurvivalRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCensorCol(self, val):
        return self._add_param('censorCol', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)


class AkSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.AkSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AkSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setNumFiles(self, val):
        return self._add_param('numFiles', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)


class AkSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.AkSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AkSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)


class AlsImplicitTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsImplicitTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsImplicitTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRateCol(self, val):
        return self._add_param('rateCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setNonnegative(self, val):
        return self._add_param('nonnegative', val)

    def setNumBlocks(self, val):
        return self._add_param('numBlocks', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setRank(self, val):
        return self._add_param('rank', val)


class AlsItemsPerUserRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsItemsPerUserRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsItemsPerUserRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setExcludeKnown(self, val):
        return self._add_param('excludeKnown', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class AlsModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class AlsRateRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsRateRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsRateRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class AlsSimilarItemsRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsSimilarItemsRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsSimilarItemsRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class AlsSimilarUsersRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsSimilarUsersRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsSimilarUsersRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class AlsTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRateCol(self, val):
        return self._add_param('rateCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setNonnegative(self, val):
        return self._add_param('nonnegative', val)

    def setNumBlocks(self, val):
        return self._add_param('numBlocks', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setRank(self, val):
        return self._add_param('rank', val)


class AlsUsersPerItemRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsUsersPerItemRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsUsersPerItemRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setExcludeKnown(self, val):
        return self._add_param('excludeKnown', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class AppendIdBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.AppendIdBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AppendIdBatchOp, self).__init__(*args, **kwargs)
        pass

    def setAppendType(self, val):
        return self._add_param('appendType', val)

    def setIdCol(self, val):
        return self._add_param('idCol', val)


class AsBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.AsBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AsBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)


class BinarizerBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.BinarizerBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BinarizerBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setThreshold(self, val):
        return self._add_param('threshold', val)


class BisectingKMeansModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.BisectingKMeansModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BisectingKMeansModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class BisectingKMeansPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.BisectingKMeansPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BisectingKMeansPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class BisectingKMeansTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.BisectingKMeansTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BisectingKMeansTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setMinDivisibleClusterSize(self, val):
        return self._add_param('minDivisibleClusterSize', val)

    def setRandomSeed(self, val):
        return self._add_param('randomSeed', val)


class BucketizerBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.BucketizerBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BucketizerBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setCutsArray(self, val):
        return self._add_param('cutsArray', val)

    def setCutsArrayStr(self, val):
        return self._add_param('cutsArrayStr', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class C45ModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.C45ModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(C45ModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class C45PredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.C45PredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(C45PredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class C45TrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.C45TrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(C45TrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class CartModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.CartModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CartModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class CartPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.CartPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CartPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class CartRegModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.CartRegModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CartRegModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class CartRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.CartRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CartRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class CartRegTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.CartRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CartRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class CartTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.CartTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CartTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class CatalogSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.CatalogSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CatalogSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCatalogObject(self, val):
        return self._add_param('catalogObject', val)


class CatalogSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.CatalogSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CatalogSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCatalogObject(self, val):
        return self._add_param('catalogObject', val)


class ChiSqSelectorBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.ChiSqSelectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ChiSqSelectorBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setFdr(self, val):
        return self._add_param('fdr', val)

    def setFpr(self, val):
        return self._add_param('fpr', val)

    def setFwe(self, val):
        return self._add_param('fwe', val)

    def setNumTopFeatures(self, val):
        return self._add_param('numTopFeatures', val)

    def setPercentile(self, val):
        return self._add_param('percentile', val)

    def setSelectorType(self, val):
        return self._add_param('selectorType', val)


class ChiSquareTestBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.statistics.ChiSquareTestBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ChiSquareTestBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)


class ChisqSelectorModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.ChisqSelectorModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ChisqSelectorModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class ColumnsToCsvBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.ColumnsToCsvBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToCsvBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)


class ColumnsToJsonBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.ColumnsToJsonBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToJsonBatchOp, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)


class ColumnsToKvBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.ColumnsToKvBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToKvBatchOp, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)


class ColumnsToTripleBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.ColumnsToTripleBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToTripleBatchOp, self).__init__(*args, **kwargs)
        pass

    def setTripleColumnValueSchemaStr(self, val):
        return self._add_param('tripleColumnValueSchemaStr', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)


class ColumnsToVectorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.ColumnsToVectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToVectorBatchOp, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)


class CorrelationBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.statistics.CorrelationBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CorrelationBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMethod(self, val):
        return self._add_param('method', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)


class CsvSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.CsvSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setFieldDelimiter(self, val):
        return self._add_param('fieldDelimiter', val)

    def setNumFiles(self, val):
        return self._add_param('numFiles', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setRowDelimiter(self, val):
        return self._add_param('rowDelimiter', val)


class CsvSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.CsvSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setFieldDelimiter(self, val):
        return self._add_param('fieldDelimiter', val)

    def setIgnoreFirstLine(self, val):
        return self._add_param('ignoreFirstLine', val)

    def setLenient(self, val):
        return self._add_param('lenient', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setRowDelimiter(self, val):
        return self._add_param('rowDelimiter', val)

    def setSkipBlankLine(self, val):
        return self._add_param('skipBlankLine', val)


class CsvToColumnsBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.CsvToColumnsBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToColumnsBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class CsvToJsonBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.CsvToJsonBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToJsonBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class CsvToKvBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.CsvToKvBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToKvBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class CsvToTripleBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.CsvToTripleBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToTripleBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setTripleColumnValueSchemaStr(self, val):
        return self._add_param('tripleColumnValueSchemaStr', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class CsvToVectorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.CsvToVectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToVectorBatchOp, self).__init__(*args, **kwargs)
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

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)


class DCTBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.DCTBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DCTBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setInverse(self, val):
        return self._add_param('inverse', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class DecisionTreeModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.DecisionTreeModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class DecisionTreePredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.DecisionTreePredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreePredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

