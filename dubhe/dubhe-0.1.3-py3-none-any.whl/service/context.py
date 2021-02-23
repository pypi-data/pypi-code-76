from __future__ import annotations
from dubhe.service import dataset
from dubhe.service import out_dataset
import typing
import logging


class ContextKey:
    """
    Key to get algorithm id from context, Str.
    """
    KEY_ALGORITHM_ID = "algorithm_id"

    """
    Key to get epoch count from context, Int.
    """
    KEY_EPOCH_COUNT = "epoch_count"

    """
    Key to get which epoch to start from context, Int.
    If can not to start with this epoch ( for example, no such saved model file in cache folder ), raise an exception
    """
    KEY_EPOCH_START = "epoch_start"

    """
    Key to get batch size from context, Int.
    """
    KEY_BATCH_SIZE = "batch_size"

    """
    Key to get train dataset, dubhe.service.dataset.Dataset.
    Always available in train method.
    """
    KEY_TRAIN_DATASET = "train_dataset"

    """
    Key to get validation dataset, dubhe.service.dataset.Dataset.
    May available in train method, if None, do not do validation.
    """
    KEY_VALIDATION_DATASET = "validation_dataset"

    """
    Key to get test dataset, dubhe.service.dataset.Dataset.
    Always available in predict method.
    """
    KEY_TEST_DATASET = "test_dataset"

    class ContextKeyError(TypeError):
        pass

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise self.ContextKeyError(f'Can not set ContextKey {key}')
        self.__dict__[key] = value


class Context(object):
    def __init__(self, logger):
        self.logger = logger
        self.local_logger = logging.getLogger("dubhe")
        self.local_logger.setLevel(logging.INFO)

        self.int_map = {}
        self.str_map = {}
        self.ds_map = {}
        self.model_path = None
        self.cache_path = None
        self.out_dataset = None

    def getInt(self, key: str, default: int = 0) -> int:
        if key in self.int_map:
            return self.int_map[key]
        else:
            return default

    def getStr(self, key: str, default: str = "") -> str:
        if key in self.str_map:
            return self.str_map[key]
        else:
            return default

    def getDataset(self, key: str) -> dataset.Dataset:
        if key in self.ds_map:
            return self.ds_map[key]
        else:
            return None

    def getModelDir(self) -> str:
        """
        Return the path folder to save best model files and configure files.
        You can save best models here and also ask user to put config files here via dubhe cloud.
        This path is writeable on training and readonly on predicting.

        :return: model_path: the path to save model files
        """
        return self.model_path

    def getCacheDir(self) -> str:
        """
        Return the path folder to save cache files.
        You can save models here every epoch here.
        This folder may be cleared via dubhe cloud if need, so make sure your model cloud work an empty cache folder.
        This path is writeable on training and will be none on predicting.

        :return: cache_path: the path to save model files
        """
        return self.cache_path

    def log(self, msg, *args, **kwargs):
        self.local_logger.info(msg, *args, **kwargs)

        if self.logger is not None:
            pass

    def logProcess(self, process: int):
        self.local_logger.info("update all process to %d", process)
        if self.logger is not None:
            # todo, send log to cloud
            pass

    def logProcessInEpoch(self, epoch: int, process: int):
        self.local_logger.info("update epoch %d process to %d", epoch, process)
        if self.logger is not None:
            pass

    def logMetric(self, epoch: int, iterator: int, key: str, value: typing.Union[float, int]):
        self.local_logger.info("update metric epoch=%d iterator=%d key=%s value=%f", epoch, iterator, key, float(value))
        if self.logger is not None:
            pass

    def createOutDataset(self) -> out_dataset.OutDataset:
        return self.out_dataset


class ContextBuilder(object):
    def __init__(self, logger):
        self.ctx = Context(logger)

    def addInt(self, key: str, value: int) -> ContextBuilder:
        self.ctx.int_map[key] = value
        return self

    def addStr(self, key: str, value: str) -> ContextBuilder:
        self.ctx.str_map[key] = value
        return self

    def addDataset(self, key: str, ds: dataset.Dataset) -> ContextBuilder:
        self.ctx.ds_map[key] = ds
        return self

    def setModelDir(self, path: str) -> ContextBuilder:
        self.ctx.model_path = path
        return self

    def setCacheDir(self, path: str) -> ContextBuilder:
        self.ctx.cache_path = path
        return self

    def setOutDataset(self, ds: out_dataset.OutDataset) -> ContextBuilder:
        self.ctx.out_dataset = ds
        return self

    def build(self) -> Context:
        return self.ctx
