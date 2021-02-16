"""
service.py

Prediction service. 
"""
from importlib import import_module

from service_settings import mlops_settings

model_id = mlops_settings["model_id"]
model_module = import_module(mlops_settings["model_import_path"])
predict = model_module.predict
_initialization = model_module.initialization
ModelException = model_module.ModelException

from akerbp.mlops import __version__ as version
from akerbp.mlops.core import logger

logging=logger.get_logger()

logging.debug(f"MLOps framework version {version}")


def initialization(secrets):
    """
    Read initialization object required by `predict`
    """
    # This check adds a little overhead to each prediction
    if 'init_object' not in globals():
        global init_object
        artifact_folder = mlops_settings["model_artifact_folder"]
        init_object = _initialization(artifact_folder, secrets)
        logging.debug(f"Loaded initialization object")


def service(data, secrets):
    """
    Generate prediction for an input
    Inputs:
        data: input to the model (sent by a user through the API)
        secrets: api keys that the model may need during initialization
    Output:
        Dictionary with a status field ('ok' or 'error'). If status is 'ok', 
         there is a 'prediction' field as well. If status is 'error', there is 
         a 'message' field as well.
    """
    try:
        initialization(secrets)
        logging.debug(f"Predict {data=}")
        y = predict(data, init_object, secrets)
        logging.debug(f"Prediction is {y=}")
        return dict(status="ok", prediction=y, model_id=model_id)
    except ModelException as error:
        error_message = f"Could not get a prediction. Message: {error}"
        logging.error(error_message)
        return dict(status="error", message=error_message, model_id=model_id)
