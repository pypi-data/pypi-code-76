import pandas as pd

from behalearn.features import FeatureExtractor


def test_segment_feature_extractor_fit():
    features = [
        'duration',
        ('length', {
            'columns': ['x', 'y'],
        })]
    data = pd.DataFrame()

    calculator = FeatureExtractor(features)

    assert calculator.fit(data) == calculator


def test_segment_feature_extractor_transform(mocker):
    features = [
        'duration',
        ('length', {
            'columns': ['x', 'y'],
        })]
    group_by_columns = ['test_grouper']
    data = pd.DataFrame(data={
        'test_grouper': [1, 2],
        'test1': [1, 3],
        'test2': [1, 3],
        'test3': [1, 3],
        'test_timestamp': ['timestamp1', 'timestamp2'],
        'x': [1, 3],
        'y': [1, 3]})

    test_result = 'test_res'

    extract_features_mock = mocker.patch(
        'behalearn.features.transformers.extract_features')
    extract_features_mock.return_value = test_result

    calculator = FeatureExtractor(
        features, group_by_columns=group_by_columns)
    calculator.fit(data)
    res_df = calculator.transform(data)

    extract_features_mock.assert_called_once_with(
        data,
        features,
        group_by_columns=group_by_columns)

    assert res_df == test_result
