from qset_feature_store.featureset_engine.dataset_manager.dataset_manager import DatasetManager
from qset_feature_store.featureset_engine.dataset_manager.local_dataset_manager import LocalDatasetManager
from qset_feature_store.repository import models
from qset_feature_store.reflexion import extract_feature_set
from qset_feature_store.featureset_engine.featureset import FeatureSet
from utils_ak.builtin import list_get

# todo: pass repository client as an argument to engine dataset manager

class EngineDatasetManager(DatasetManager):
    def __init__(self, dataset_managers, repository_client):
        self.dataset_managers = dataset_managers
        self.ldm = list_get([dm for dm in self.dataset_managers if isinstance(dm, LocalDatasetManager)])
        assert self.ldm is not None
        self.repository_client = repository_client

    def get_from_dataset(self, dataset):
        raise Exception(f'Use get method to get dataset from dataset managers')

    def get_from_featureset(self, featureset, scope, params):
        # todo: make use of config properly
        featureset = models.cast_dict(featureset, models.FeatureSet)
        assert featureset['engine'] == 'pandas/v1'
        cls = extract_feature_set(featureset['config']['code'])
        featureset_instance = cls()
        return self.calc(featureset_instance, featureset['inputs'], scope, params)

    def calc(self, featureset_instance, inputs, scope, params):
        featureset_instance.inputs = inputs
        featureset_instance.params = params
        featureset_instance.scope = scope
        featureset_instance.dataset_provider = self
        return featureset_instance.calc()

    def get_from_dataset_schema(self, dataset_schema, scope):
        # fetch local dataset if possible
        datasets = self.repository_client.get_many('dataset', dataset_schema=dataset_schema['_id'], scope=scope, materialization={'storage': 'local'})

        if datasets:
            assert len(datasets) == 1, 'Only one local dataset allowed for current dataset schema'
            try:
                return self.get(datasets[0])
            except:
                pass

        featureset = models.cast_dict(dataset_schema['featureset'], models.FeatureSet)
        return self.get_from_featureset(featureset, scope, dataset_schema['params'])

    def get(self, generic_featureset, scope=None, params=None):
        generic_featureset = super()._format_generic_featureset(generic_featureset)

        # try to get from data managers first
        for manager in self.dataset_managers:
            try:
                return manager.get(generic_featureset, scope, params)
            except:
                pass

        # try to calc otherwise
        return super().get(generic_featureset, scope, params)

    def put(self, df, dataset):
        assert dataset.get('materialization', {}).get('storage') == 'local', 'Only local storage is supported.'
        return self.ldm.put(df, dataset)



def test_calc():
    import sys
    sys.path.append(r'C:\Users\Mi\Desktop\master\code\git\2020.09-qset\qset-feature-store')
    from qset_feature_store import FeatureSet
    import pandas as pd
    class TrivialFeatureSet(FeatureSet):
        def calc(self):
            return pd.DataFrame([1, 2, 3], columns=['a'])

    import sys
    sys.path.append(r'C:\Users\Mi\Desktop\master\code\git\2020.09-qset\qset-feature-store')
    from qset_feature_store import FeatureSet
    import pandas as pd
    class FeatureSetUsingTimebars(FeatureSet):
        def calc(self):
            return self.get(self.inputs['timebars']) * 2

    from qset_feature_store.repository.client import QsetRepositoryClient
    cli = QsetRepositoryClient('akadaner', db='feature-store-test')

    dms = []
    dms.append(LocalDatasetManager('data/'))
    qdm = qset_dataset_manager = EngineDatasetManager(dms, cli)

    # clean
    for key in ['featureset', 'dataset_schema', 'dataset']:
        for doc in cli.get_many(key):
            cli.delete(key, doc)

    # create timebars featureset
    fs = cli.create_featureset('timebars', 'external')
    fs = cli.push('featureset', fs)

    dss = cli.create_dataset_schema('timebars_schema', fs, {'period': 600})
    dss = cli.push('dataset_schema', dss)

    ds = cli.create_dataset('timebars_local', scope={'universe': 'binance'}, dataset_schema=dss, materialization={'storage': 'local'})
    ds = cli.push('dataset', ds)

    df = pd.DataFrame([[1, 4], [2, 5], [3, 6]], columns=['a', 'b'])

    qdm.put(df, ds)

    print(qdm.get(ds).head())
    print(qdm.calc(TrivialFeatureSet(), inputs={}, scope={'universe': 'binance'}, params={}))
    print(qdm.calc(FeatureSetUsingTimebars(), inputs={'timebars': dss}, scope={'universe': 'binance'}, params={}))

    # create configured with pandas

    code = r'''
import sys
sys.path.append(r'C:\Users\Mi\Desktop\master\code\git\2020.09-qset\qset-feature-store')
from qset_feature_store import FeatureSet
import pandas as pd
class TrivialFeatureSet(FeatureSet):
    def calc(self):
        return pd.DataFrame([1, 2, 3], columns=['a'])
'''

    fs = cli.create_featureset('my_pandas_featureset', 'pandas/v1', {'code': code})
    fs = cli.push('featureset', fs)
    print(fs)

    # note: using get now - since it is a repository featureset
    print(qdm.get(fs, scope={'universe': 'binance'}, params={}))


if __name__ == '__main__':
    test_calc()