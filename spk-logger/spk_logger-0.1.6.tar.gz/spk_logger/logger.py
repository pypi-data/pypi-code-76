from .base_models import Prediction, LogInput, LogPrediction, LogPredictionError, LogInfo
from google.cloud.logging_v2.logger import Logger
from google.cloud.logging_v2.client import Client
from datetime import datetime

class SpikeLogger():

    def __init__(self,
                project_name:str=None,
                log_name:str=None,
                user:str="SpikeDefaultLogger"):
        """ Construct a logger class. 
                Logger represent named target for log entries used by Google cloud logging.

        Parameters
        --------------
        project_name: string 
            Name of a existing project in Google CLoud.
        log_name: string
            Target log name used by logger to send log entries.
        user: string, optional (default='SpikeDefaultLogger')
            Username who instantiated Logger class.     

        .. note:
            To use the Logger class, both the project and the reference log must exists. In case one is missing, in README.md you will find the instructions to create them.
        """

        if project_name == None:
            raise ValueError(f"project_name is required")
        if log_name == None:
            raise ValueError(f"log_name is required")
        
        self.log_name = log_name
        self.user = user
        self.project_name = project_name

        #Setup del cliente de GCP
        self.client = Client(project=project_name)
        self.client.get_default_handler()
        self.client.setup_logging()
        
        #TODO: Validar que el log_name existe en GCP
        #self.client.logger(self.log_name)
        self.logger = Logger(self.log_name,self.client)

    def log_input(self, input_data:dict):
        """ log_input send log with the input data.

        Parameters 
        ------------
         input_data: dictionary
            The input data given by the user. 
        """
        if not input_data:
            raise ValueError("input_data is empty")
        log = LogInput(log_type="logInput", user=self.user, input_raw=input_data)
        self.logger.log_struct(log.dict())

    def log_info(self, info:dict=None):
        """ log_info send log with the information of the input data.

        Parameters 
        ------------
        info: dictionary
            The "info" dictionary is information of your choice that you need to log in.
        """
        log_date = str(datetime.now())
        log = LogInfo(log_type="LogInfo", user=self.user, project=self.project_name, date=log_date, info=info)
        self.logger.log_struct(log.dict())


    def log_prediction(self, 
                       prediction:dict = None,
                       input_raw:dict = None,
                       input_features:dict = None,
                       model_id:str = None,
                       process_time:float = None,
                       ):
        """ log_prediction send log with the information of the prediction.

        Parameters 
        ------------
         prediction: dictionary
            Prediction made by the model. 
         process_time: float
            Time taken to perform the prediction.
         model_id: string
            ID of the model that made the prediction.
         input_raw: dictionary
            Input sent by the user, not necessarily used by the model.
         input_features: dictionary
            Features used by the model to perform the prediction.
        """
        if not input_raw:
            raise ValueError("input_raw are empty")
        if not input_features:
            raise ValueError("input_features are empty")
        if not prediction:
            raise ValueError("prediction is empty")
        if not model_id:
            raise ValueError("model_id is empty") 
        if not process_time:
            raise ValueError("process_time is empty") 
        
        log_date = str(datetime.now())
        # Classes Prediction and LogInput required by LogPrediction, contains infomation about prediction values and features used by the model
        pred = Prediction(prediction=prediction, model_id=model_id, process_time=process_time, prediction_date=log_date, model_features=input_features)
        log_in = LogInput(log_type="LogInput", user=self.user, input_raw=input_raw) 
        
        log = LogPrediction(log_type="LogPrediction", predict=pred, input=log_in)
        self.logger.log_struct(log.dict())
        pass

    def log_prediction_error(self, 
                       msg_error:str = None,
                       model_id:str =None,
                       input_data:dict = None,
                       ):
        """ log_prediction_error send log with the description of the prediction error. 
         
        Parameters
        ------------
         msg_error: string 
            Message with the description of the error.
         model_id: string
            ID of the model that made the prediction.
         input_data: dictionary
            Input used by the model to perform the prediction.
        """ 
        if not msg_error:
            raise ValueError("The error message has not been entered")
        if not model_id:
            raise ValueError("model_id is empty")
        if not input_data:
            raise ValueError("input_data is empty")

        log_date = str(datetime.now())
        log_in = LogInput(log_type="logInput", user=self.user, input_raw=input_data,)
        log = LogPredictionError(log_type="logPredictionError", msg_error=msg_error, model_id=model_id, date=log_date, input=log_in)
        self.logger.log_struct(log.dict())
        pass

if __name__ == "__main__":
    logger = Logger()
