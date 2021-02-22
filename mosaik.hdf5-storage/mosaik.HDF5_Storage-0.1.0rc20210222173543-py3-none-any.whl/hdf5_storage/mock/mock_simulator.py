from mosaik_api import Simulator

from mosaik_hdf5_storage.hdf5_storage.mock.mock_meta import MOCK_META


class MockSimulator(Simulator):

    def __init__(self):
        super().__init__(MOCK_META)

        self._models = {}

    def create(self, num, model, **model_params):
        return

    def step(self, time, inputs):
        return time + 1

    def get_data(self, outputs):
        return outputs
