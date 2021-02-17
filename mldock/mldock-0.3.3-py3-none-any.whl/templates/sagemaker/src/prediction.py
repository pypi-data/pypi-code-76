import os
import sys
import io
import csv
import traceback
import logging
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(None)
logger.setLevel(logging.INFO)

MODEL_DIR = '/opt/ml/model'

def extract_stack_trace() -> str:
    """Extracts full stacktrace from thown exception
    Returns:
        str: traceback of error thrown
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    stack_trace = traceback.format_exception(
        exc_type,
        exc_value,
        exc_traceback
    )
    return repr(stack_trace)

def array_to_csv(array_like):
    """Convert an array-like object to CSV.
    To understand better what an array-like object is see:
    https://docs.scipy.org/doc/numpy/user/basics.creation.html#converting-python-array-like-objects-to-numpy-arrays
    Args:
        array_like (np.array or Iterable or int or float): array-like object
            to be converted to CSV.
    Returns:
        (str): object serialized to CSV
    """
    stream = io.StringIO()
    
    np.savetxt(stream, array_like, delimiter=",", fmt="'%s'")
    return stream.getvalue()

class ModelService(object):
    model = None

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model == None:
            # TODO place your model load code here
            # get your model from MODEL_DIR
            cls.model = None
        return cls.model

    @staticmethod
    def input_load(data):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            return pd.DataFrame([data])
        elif isinstance(data, bytes):
            return pd.read_csv(io.BytesIO(data), sep=",")
        else:
            raise TypeError("Expected payload to have type list or dict")
    
    @staticmethod
    def input_transform(data: pd.DataFrame, cols: list) -> pd.DataFrame:
        """transform the input dataset

        Args:
            data (pd.DataFrame): dataframe of input data

        Returns:
            pd.DataFrame: transformed data
        """
        return data.filter(cols, axis=1)

    @staticmethod
    def output_transform_json(pred):
        """transform numpy array of predictions into json payload"""
        results = pred.tolist()
        return {'results': results}

    @staticmethod
    def output_transform_csv(pred):
        """Transform numpy array of predictions in to csv"""
        predictions = pred.tolist()

        # create results
        results = [('idx','prediction')]
        # append values
        [
            results.append(
                (i,
                pred)
            ) for (i, pred) in enumerate(predictions)
        ]

        return array_to_csv(results)

    @classmethod
    def predict(cls, input, content_type='json'):
        """For the input, do the predictions and return them.

        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        model = cls.get_model()
        
        try:
            # load input data
            data = cls.input_load(data=input)

            # TODO run input processing as needed
            # keep this light
            # input_transform(data=data, cols=[])

            # TODO run model prediction has required
            # pred = model.predict(data)
            pred = np.array(['pred_1', 'pred_2', 'pred_3'])

            # TODO Add any post processing
            if content_type == 'csv':
                results = cls.output_transform_csv(pred)
            else:
                results = cls.output_transform_json(pred)
            return results

        except Exception as exception:
            # get stack trace as exception
            stack_trace = extract_stack_trace()
            reformatted_log_msg = (
                    'Server Error: {ex}'.format(ex=stack_trace)
            )
            return reformatted_log_msg


def predict(json_input, content_type='json'):
    """
    Prediction given the request input
    :param json_input: [dict], request input
    :return: [dict], prediction
    """

    # TODO Transform json_input and assign the transformed value to model_input
    model_input = json_input
    
    result = ModelService.predict(model_input, content_type=content_type)
    logger.info(result)

    return result
