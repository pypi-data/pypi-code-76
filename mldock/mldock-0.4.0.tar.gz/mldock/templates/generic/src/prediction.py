import os
import sys
import traceback

from mldock.platform_helpers.environment import Environment
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('mldock')

environment = Environment(base_dir='/opt/ml')
MODEL_DIR = environment.model_dir

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

class ModelService(object):
    model = None


    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model == None:
            logger.info("Loading Model Artifacts")
            # TODO place your model load code here
            # get your model from MODEL_DIR
            cls.model = None
        return cls.model

    @classmethod
    def predict(cls, input):
        """For the input, do the predictions and return them.

        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        model = cls.get_model()
        
        try:
            logger.info("Running Prediction")
            # TODO run model prediction has required

            # TODO Add any post processing

            return None
        except Exception as exception:
            # get stack trace as exception
            stack_trace = extract_stack_trace()
            reformatted_log_msg = (
                    'Server Error: {ex}'.format(ex=stack_trace)
            )
            return reformatted_log_msg


def predict(json_input):
    """
    Prediction given the request input
    :param json_input: [dict], request input
    :return: [dict], prediction
    """

    # TODO Transform json_input and assign the transformed value to model_input
    model_input = None
    
    result = ModelService.predict(model_input)
    logger.debug(result)

    return result
