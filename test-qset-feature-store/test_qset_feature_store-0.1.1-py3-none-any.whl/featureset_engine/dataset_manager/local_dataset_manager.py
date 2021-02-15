from utils_ak.interactive_imports import *
from qset_feature_store.featureset_engine.dataset_manager.dataset_manager import DatasetManager


class LocalDatasetManager(DatasetManager):
    def __init__(self, data_path):
        self.data_path = data_path
        makedirs(self.data_path)

    def _fn(self, dataset):
        base_fn = str(dataset['_id'])
        return os.path.join(self.data_path, 'local', base_fn, base_fn + '.parquet')

    def get_from_dataset(self, dataset):
        if not os.path.exists(self._fn(dataset)):
            raise KeyError('Local configured featureset not found')
        # todo: make index properly
        df = pd_read(self._fn(dataset))
        return df

    def put_dataset(self, df, dataset, **kwargs):
        makedirs(self._fn(dataset))
        pd_write(df, self._fn(dataset))


def test_local_dataset_manager():
    from qset_feature_store.repository.client import QsetRepositoryClient
    cli = QsetRepositoryClient('akadaner', db='feature-store-test')

    for key in ['featureset', 'dataset_schema', 'dataset']:
        for fs in cli.get_many(key):
            cli.delete(key, fs)

    fs = cli.create_featureset('my_featureset', engine='pandas/v1', config={'code': 'print("Hello World")'})
    fs = cli.push('featureset', fs)

    dss = cli.create_dataset_schema('my_dataset_schema', fs, params={'param': 'foo'})
    dss = cli.push('dataset_schema', dss)

    ds = cli.create_dataset('my_dataset', {'universe': 'binance'}, dss, materialization={'storage': 'local'})
    ds = cli.push('dataset', ds)

    ldm = LocalDatasetManager('data/')

    df = pd.DataFrame([1, 2, 3], columns=['a'])

    ldm.put(df, ds)

    print(ldm.get(ds))


if __name__ == '__main__':
    test_local_dataset_manager()
