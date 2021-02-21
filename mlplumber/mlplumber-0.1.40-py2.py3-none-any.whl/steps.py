from baikal import Step
from sklearn_pandas import DataFrameMapper


class DataFrameMapperStep(Step, DataFrameMapper):

    def __init__(self, *args, name=None, n_outputs=1, **kwargs):
        super().__init__(*args, name=name, n_outputs=n_outputs, **kwargs)
        self._nodes = []

    def __getstate__(self):
        state = super().__getstate__()
        state["_name"] = self._name
        state["_nodes"] = self._nodes
        state["_n_outputs"] = self._n_outputs
        return state

    def __setstate__(self, state):
        self._name = state["_name"]
        self._nodes = state["_nodes"]
        self._n_outputs = state["_n_outputs"]
        super().__setstate__(state)
        return
