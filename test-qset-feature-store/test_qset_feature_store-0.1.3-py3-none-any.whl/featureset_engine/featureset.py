class FeatureSet:
    def __init__(self):
        self.params = {}
        self.inputs = {}

        self.scope = None
        self.dataset_provider = None

    def calc(self):
        raise Exception('Not implemented')

    def get(self, generic_featureset, params=None):
        if self.dataset_provider is None:
            raise Exception('Data provider not set')
        return self.dataset_provider.get(generic_featureset, scope=self.scope, params=params)
