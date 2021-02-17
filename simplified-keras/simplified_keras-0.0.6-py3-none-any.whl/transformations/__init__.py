import numpy as np


def predictions_to_classes(predictions):
    return np.argmax(predictions, axis=-1)


def one_hot_to_sparse(tensor):
    return np.argmax(tensor, axis=1)
