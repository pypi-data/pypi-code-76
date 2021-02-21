import inspect
import pandas as pd
from sklearn.base import TransformerMixin
from . import logger


def get_feature_names(estimator):
    """
    Attempt to extract feature names based on a given estimator
    """
    if hasattr(estimator, 'classes_'):
        return estimator.classes_
    elif hasattr(estimator, 'get_feature_names'):
        return estimator.get_feature_names()
    return None


class PandasTransformerAdapter(object):

    def transform(self, *args, **kwargs):
        output = super().transform(*args, **kwargs)
        return pd.DataFrame(output, columns=get_feature_names(self))

    def fit_transform(self, *args, **kwargs):
        output = super().fit_transform(*args, **kwargs)
        return pd.DataFrame(output, columns=get_feature_names(self))


def adapt_as_pandas_transformer(base_class: type, class_name: str = None):
    """
    Adapt a single class into a pandas transformer
    :param base_class:
    :param class_name:
    :return:
    """
    name = f"{base_class.__name__}DF" if class_name is None else class_name
    bases = (PandasTransformerAdapter, base_class,)
    adapter = type(name, bases, {})
    return adapter


def adapt_all_as_pandas_transformer(module):
    """
    Adapt all transformers in a given module as a pandas adapter..
    This will create a corresponding pandas adapter. For instance
    adapt_all_as_pandas_transformer(sklearn.preprocessing) will lead to
    following new classes
    sklearn.preprocessing.LabelBinarizerDF
    sklearn.preprocessing.MixMaxScalarDF
    :param module: Module
    :return:
    """
    members = inspect.getmembers(
        module,
        predicate=lambda o: inspect.isclass(o) and
        issubclass(o, TransformerMixin) and
        not issubclass(o, PandasTransformerAdapter)
    )
    mod_name = module.__name__

    for name, cls in members:
        cls_df = adapt_as_pandas_transformer(cls)
        logger.info(f"Register {name} as {mod_name}.{cls_df.__name__}")
        setattr(module, cls_df.__name__, cls_df)
