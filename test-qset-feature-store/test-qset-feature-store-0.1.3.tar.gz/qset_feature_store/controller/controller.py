from qset_feature_store.repository import QsetRepositoryClient
from qset_feature_store.featureset_engine.dataset_manager import LocalDatasetManager, EngineDatasetManager


class Controller:
    def __init__(self, account, repository_host='localhost'):
        self.account = account
        self.repository = QsetRepositoryClient(account=account, db='feature-store', host=repository_host)

        dms = []
        dms.append(LocalDatasetManager('data/'))
        self.datasets = EngineDatasetManager(dms, self.repository)
