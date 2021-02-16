from pandas import DataFrame
from collections import Iterable

class AnarciObject:
    """Wrapper class for using multiindexing on pandas DataFrames
    """
    def __init__(self, dataframe=DataFrame(), indices=['annotation_type','position']):
        self.dataframe = dataframe
        self.indices = indices
        self._set_columns()
    
    def _set_columns(self):
        self.dataframe = self.dataframe.set_index(keys=self.indices)