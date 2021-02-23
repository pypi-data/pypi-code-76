#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import BatchOperator, BaseSinkBatchOp
from ..lazy.extract_model_info_batch_op import ExtractModelInfoBatchOp
from ..lazy.with_model_info_batch_op import WithModelInfoBatchOp
from ..lazy.with_train_info import WithTrainInfo


class DecisionTreeRegModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.DecisionTreeRegModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class DecisionTreeRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.DecisionTreeRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class DecisionTreeRegTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.DecisionTreeRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegTrainBatchOp, self).__init__(*args, **kwargs)
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


class DecisionTreeTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.DecisionTreeTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeTrainBatchOp, self).__init__(*args, **kwargs)
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

    def setTreeType(self, val):
        return self._add_param('treeType', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class DistinctBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.DistinctBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DistinctBatchOp, self).__init__(*args, **kwargs)
        pass


class DocCountVectorizerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.DocCountVectorizerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocCountVectorizerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class DocCountVectorizerTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.DocCountVectorizerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocCountVectorizerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setFeatureType(self, val):
        return self._add_param('featureType', val)

    def setMaxDF(self, val):
        return self._add_param('maxDF', val)

    def setMinDF(self, val):
        return self._add_param('minDF', val)

    def setMinTF(self, val):
        return self._add_param('minTF', val)

    def setVocabSize(self, val):
        return self._add_param('vocabSize', val)


class DocHashCountVectorizerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.DocHashCountVectorizerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocHashCountVectorizerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class DocHashCountVectorizerTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.DocHashCountVectorizerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocHashCountVectorizerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setFeatureType(self, val):
        return self._add_param('featureType', val)

    def setMinDF(self, val):
        return self._add_param('minDF', val)

    def setMinTF(self, val):
        return self._add_param('minTF', val)

    def setNumFeatures(self, val):
        return self._add_param('numFeatures', val)


class DocWordCountBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.DocWordCountBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocWordCountBatchOp, self).__init__(*args, **kwargs)
        pass

    def setContentCol(self, val):
        return self._add_param('contentCol', val)

    def setDocIdCol(self, val):
        return self._add_param('docIdCol', val)

    def setWordDelimiter(self, val):
        return self._add_param('wordDelimiter', val)


class EqualWidthDiscretizerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.EqualWidthDiscretizerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EqualWidthDiscretizerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class EqualWidthDiscretizerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.EqualWidthDiscretizerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EqualWidthDiscretizerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class EqualWidthDiscretizerTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.EqualWidthDiscretizerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EqualWidthDiscretizerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setNumBuckets(self, val):
        return self._add_param('numBuckets', val)

    def setNumBucketsArray(self, val):
        return self._add_param('numBucketsArray', val)


class EvalBinaryClassBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalBinaryClassBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalBinaryClassBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setPositiveLabelValueString(self, val):
        return self._add_param('positiveLabelValueString', val)


class EvalClusterBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalClusterBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalClusterBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class EvalMultiClassBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalMultiClassBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalMultiClassBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)


class EvalMultiLabelBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalMultiLabelBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalMultiLabelBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLabelRankingInfo(self, val):
        return self._add_param('labelRankingInfo', val)

    def setPredictionRankingInfo(self, val):
        return self._add_param('predictionRankingInfo', val)


class EvalRankingBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalRankingBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalRankingBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLabelRankingInfo(self, val):
        return self._add_param('labelRankingInfo', val)

    def setPredictionRankingInfo(self, val):
        return self._add_param('predictionRankingInfo', val)


class EvalRegressionBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalRegressionBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalRegressionBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)


class FeatureHasherBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.FeatureHasherBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FeatureHasherBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setNumFeatures(self, val):
        return self._add_param('numFeatures', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class FilterBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.FilterBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FilterBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)


class FirstNBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.FirstNBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FirstNBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSize(self, val):
        return self._add_param('size', val)


class FlattenKObjectBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.FlattenKObjectBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FlattenKObjectBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setOutputColTypes(self, val):
        return self._add_param('outputColTypes', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class FmClassifierModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.FmClassifierModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmClassifierModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class FmClassifierPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.FmClassifierPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmClassifierPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class FmClassifierTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.FmClassifierTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmClassifierTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setInitStdev(self, val):
        return self._add_param('initStdev', val)

    def setLambda0(self, val):
        return self._add_param('lambda0', val)

    def setLambda1(self, val):
        return self._add_param('lambda1', val)

    def setLambda2(self, val):
        return self._add_param('lambda2', val)

    def setLearnRate(self, val):
        return self._add_param('learnRate', val)

    def setMinibatchSize(self, val):
        return self._add_param('minibatchSize', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumFactor(self, val):
        return self._add_param('numFactor', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setWithLinearItem(self, val):
        return self._add_param('withLinearItem', val)


class FmItemsPerUserRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.FmItemsPerUserRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmItemsPerUserRecommBatchOp, self).__init__(*args, **kwargs)
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


class FmPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.common.fm.FmPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class FmRateRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.FmRateRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRateRecommBatchOp, self).__init__(*args, **kwargs)
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


class FmRecommBinaryImplicitTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.FmRecommBinaryImplicitTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRecommBinaryImplicitTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setInitStdev(self, val):
        return self._add_param('initStdev', val)

    def setItemCategoricalFeatureCols(self, val):
        return self._add_param('itemCategoricalFeatureCols', val)

    def setItemFeatureCols(self, val):
        return self._add_param('itemFeatureCols', val)

    def setLambda0(self, val):
        return self._add_param('lambda0', val)

    def setLambda1(self, val):
        return self._add_param('lambda1', val)

    def setLambda2(self, val):
        return self._add_param('lambda2', val)

    def setLearnRate(self, val):
        return self._add_param('learnRate', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumFactor(self, val):
        return self._add_param('numFactor', val)

    def setRateCol(self, val):
        return self._add_param('rateCol', val)

    def setUserCategoricalFeatureCols(self, val):
        return self._add_param('userCategoricalFeatureCols', val)

    def setUserFeatureCols(self, val):
        return self._add_param('userFeatureCols', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setWithLinearItem(self, val):
        return self._add_param('withLinearItem', val)


class FmRecommTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.FmRecommTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRecommTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRateCol(self, val):
        return self._add_param('rateCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setInitStdev(self, val):
        return self._add_param('initStdev', val)

    def setItemCategoricalFeatureCols(self, val):
        return self._add_param('itemCategoricalFeatureCols', val)

    def setItemFeatureCols(self, val):
        return self._add_param('itemFeatureCols', val)

    def setLambda0(self, val):
        return self._add_param('lambda0', val)

    def setLambda1(self, val):
        return self._add_param('lambda1', val)

    def setLambda2(self, val):
        return self._add_param('lambda2', val)

    def setLearnRate(self, val):
        return self._add_param('learnRate', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumFactor(self, val):
        return self._add_param('numFactor', val)

    def setUserCategoricalFeatureCols(self, val):
        return self._add_param('userCategoricalFeatureCols', val)

    def setUserFeatureCols(self, val):
        return self._add_param('userFeatureCols', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setWithLinearItem(self, val):
        return self._add_param('withLinearItem', val)


class FmRegressorModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.FmRegressorModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRegressorModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class FmRegressorPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.FmRegressorPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRegressorPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class FmRegressorTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.FmRegressorTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRegressorTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setInitStdev(self, val):
        return self._add_param('initStdev', val)

    def setLambda0(self, val):
        return self._add_param('lambda0', val)

    def setLambda1(self, val):
        return self._add_param('lambda1', val)

    def setLambda2(self, val):
        return self._add_param('lambda2', val)

    def setLearnRate(self, val):
        return self._add_param('learnRate', val)

    def setMinibatchSize(self, val):
        return self._add_param('minibatchSize', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumFactor(self, val):
        return self._add_param('numFactor', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setWithLinearItem(self, val):
        return self._add_param('withLinearItem', val)


class FmUsersPerItemRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.FmUsersPerItemRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmUsersPerItemRecommBatchOp, self).__init__(*args, **kwargs)
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


class FpGrowthBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.associationrule.FpGrowthBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FpGrowthBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemsCol(self, val):
        return self._add_param('itemsCol', val)

    def setMaxConsequentLength(self, val):
        return self._add_param('maxConsequentLength', val)

    def setMaxPatternLength(self, val):
        return self._add_param('maxPatternLength', val)

    def setMinConfidence(self, val):
        return self._add_param('minConfidence', val)

    def setMinLift(self, val):
        return self._add_param('minLift', val)

    def setMinSupportCount(self, val):
        return self._add_param('minSupportCount', val)

    def setMinSupportPercent(self, val):
        return self._add_param('minSupportPercent', val)


class FullOuterJoinBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.FullOuterJoinBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FullOuterJoinBatchOp, self).__init__(*args, **kwargs)
        pass

    def setJoinPredicate(self, val):
        return self._add_param('joinPredicate', val)

    def setSelectClause(self, val):
        return self._add_param('selectClause', val)

    def setType(self, val):
        return self._add_param('type', val)


class GbdtModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.GbdtModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class GbdtPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.GbdtPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class GbdtRegModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GbdtRegModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class GbdtRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GbdtRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class GbdtRegTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GbdtRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setAlgoType(self, val):
        return self._add_param('algoType', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCriteriaType(self, val):
        return self._add_param('criteriaType', val)

    def setFeatureImportanceType(self, val):
        return self._add_param('featureImportanceType', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setMinSumHessianPerLeaf(self, val):
        return self._add_param('minSumHessianPerLeaf', val)

    def setNewtonStep(self, val):
        return self._add_param('newtonStep', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setSketchEps(self, val):
        return self._add_param('sketchEps', val)

    def setSketchRatio(self, val):
        return self._add_param('sketchRatio', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setUseEpsilonApproQuantile(self, val):
        return self._add_param('useEpsilonApproQuantile', val)

    def setUseMissing(self, val):
        return self._add_param('useMissing', val)

    def setUseOneHot(self, val):
        return self._add_param('useOneHot', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class GbdtTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.GbdtTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setAlgoType(self, val):
        return self._add_param('algoType', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCriteriaType(self, val):
        return self._add_param('criteriaType', val)

    def setFeatureImportanceType(self, val):
        return self._add_param('featureImportanceType', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setMinSumHessianPerLeaf(self, val):
        return self._add_param('minSumHessianPerLeaf', val)

    def setNewtonStep(self, val):
        return self._add_param('newtonStep', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setSketchEps(self, val):
        return self._add_param('sketchEps', val)

    def setSketchRatio(self, val):
        return self._add_param('sketchRatio', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setUseEpsilonApproQuantile(self, val):
        return self._add_param('useEpsilonApproQuantile', val)

    def setUseMissing(self, val):
        return self._add_param('useMissing', val)

    def setUseOneHot(self, val):
        return self._add_param('useOneHot', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class GeoKMeansPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GeoKMeansPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GeoKMeansPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setPredictionDistanceCol(self, val):
        return self._add_param('predictionDistanceCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class GeoKMeansTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GeoKMeansTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GeoKMeansTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLatitudeCol(self, val):
        return self._add_param('latitudeCol', val)

    def setLongitudeCol(self, val):
        return self._add_param('longitudeCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setInitMode(self, val):
        return self._add_param('initMode', val)

    def setInitSteps(self, val):
        return self._add_param('initSteps', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setRandomSeed(self, val):
        return self._add_param('randomSeed', val)


class GlmEvaluationBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GlmEvaluationBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GlmEvaluationBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFamily(self, val):
        return self._add_param('family', val)

    def setFitIntercept(self, val):
        return self._add_param('fitIntercept', val)

    def setLink(self, val):
        return self._add_param('link', val)

    def setLinkPower(self, val):
        return self._add_param('linkPower', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOffsetCol(self, val):
        return self._add_param('offsetCol', val)

    def setRegParam(self, val):
        return self._add_param('regParam', val)

    def setVariancePower(self, val):
        return self._add_param('variancePower', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class GlmModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GlmModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GlmModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass


class GlmPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GlmPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GlmPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLinkPredResultCol(self, val):
        return self._add_param('linkPredResultCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)


class GlmTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GlmTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GlmTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFamily(self, val):
        return self._add_param('family', val)

    def setFitIntercept(self, val):
        return self._add_param('fitIntercept', val)

    def setLink(self, val):
        return self._add_param('link', val)

    def setLinkPower(self, val):
        return self._add_param('linkPower', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOffsetCol(self, val):
        return self._add_param('offsetCol', val)

    def setRegParam(self, val):
        return self._add_param('regParam', val)

    def setVariancePower(self, val):
        return self._add_param('variancePower', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class GmmModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GmmModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GmmModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass

