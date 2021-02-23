"""
Evaluation methods in the sample declair project.
"""
import torch

def thresholded_output_transform(output):
    """
    A function that transforms the output of train, validation and test engines
    into thresholded values understandable by some ignite.metrics metrics which
    require a classification threshold, like accuracy.
    Note that it implicitly thresholds at 0.5, which isn't a great practice; it's
    here only to show how to run the metrics correctly.
    """
    # metrics like accuracy, precision or recall expect y_pred to be integers
    y_pred = output[0]
    y = output[1]
    y_pred = torch.round(y_pred)
    return y_pred, y
