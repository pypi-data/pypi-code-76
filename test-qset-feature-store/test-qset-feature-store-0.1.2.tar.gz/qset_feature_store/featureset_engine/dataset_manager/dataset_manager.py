from qset_feature_store.repository import models

# todo: refactor code duplicate


class DatasetManager:
    def _format_generic_featureset(self, generic_featureset):
        if generic_featureset['_cls'] == 'DataSet':
            return models.cast_dict(generic_featureset, models.DataSet)
        elif generic_featureset['_cls'] == 'FeatureSet':
            return models.cast_dict(generic_featureset, models.FeatureSet)
        elif generic_featureset['_cls'] == 'DatasetSchema':
            return models.cast_dict(generic_featureset, models.DatasetSchema)

    def get(self, generic_featureset, config=None, params=None):
        generic_featureset = self._format_generic_featureset(generic_featureset)
        if generic_featureset['_cls'] == 'DataSet':
            return self.get_from_dataset(generic_featureset)
        elif generic_featureset['_cls'] == 'FeatureSet':
            return self.get_from_featureset(generic_featureset, config, params)
        elif generic_featureset['_cls'] == 'DatasetSchema':
            assert params is None
            return self.get_from_dataset_schema(generic_featureset, config)

    def put(self, df, dataset):
        assert dataset['_cls'] == 'DataSet' and dataset.get('materialization', {}).get('storage') == 'local'
        generic_featureset = self._format_generic_featureset(dataset)
        return self.put_dataset(df, generic_featureset)

    def get_from_dataset(self, dataset):
        raise NotImplementedError

    def get_from_featureset(self, featureset, config, params):
        raise NotImplementedError

    def get_from_dataset_schema(self, dataset_schema, config):
        raise NotImplementedError

    def put_dataset(self, df, dataset, **kwargs):
        raise NotImplementedError