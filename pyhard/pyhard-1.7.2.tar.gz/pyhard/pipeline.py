import os
import logging
import pandas as pd
from importlib import import_module
from .context import Configuration


class Pipeline:
    def __init__(self, steps: tuple, data=None, config=None):
        self.logger = logging.getLogger(__name__)

        if config is None:
            with Configuration() as conf:
                self.config = conf.get_full()
        elif isinstance(config, dict):
            self.config = config
        else:
            raise TypeError("'config' is either None or a dictionary.")

        if data is None:
            file_path = self.config.get('datafile')
            if os.path.isfile(file_path):
                self.data = pd.read_csv(file_path)
            else:
                raise FileNotFoundError("No file '{0}'.".format(file_path))
        elif isinstance(data, pd.DataFrame):
            self.data = data.copy()
        else:
            raise TypeError("'data' must be passed as pandas DataFrame.")

        labels_col = self.config['labels_col']
        self.X = self.data.drop(columns=labels_col).values.copy()
        self.y = self.data[labels_col].values.copy()

        # scale, build, feature selec., matilda
        self.steps = steps

    def _call_method(self, name, **kwargs):
        return getattr(self, name)(**kwargs)

    def run(self):
        for step in self.steps:
            self._call_method(step)

    def scale(self):
        try:
            scaler = getattr(import_module('sklearn.preprocessing'), self.config['scaler'])()
            self.X = scaler.fit_transform(self.X)
        except AttributeError:
            self.logger.warning("Unknown scaler '{0}'. Using original data.".format(self.config['scaler']))
