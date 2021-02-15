from .base_models import Prediction, LogInput, LogPrediction, LogPredictionError
from google.cloud.logging_v2.logger import Logger
from google.cloud.logging_v2.client import Client
from datetime import datetime

class SpikeLogger():
    """ Description class..."""

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
        
        self.log_name = str(log_name)
        self.user = user

        #Setup del cliente de GCP
        self.client = Client(project=project_name)
        self.client.get_default_handler()
        self.client.setup_logging()
        
        #TODO: Validar que el log_name existe en GCP
        #self.client.logger(self.log_name)
        self.logger = Logger(self.log_name,self.client)

    def log_input(self, input_data:dict, input_type:str):
        allowed_inputs_labels = ['raw_input']
        if input_type not in allowed_inputs_labels:
            raise ValueError("input_type must be one of these: {0}" \
                                    .format(",".join(allowed_inputs_labels)))
        if not input_data:
            raise ValueError("input_data is empty")
        #print(dir(self.client))
        log = LogInput(user=self.user, data=input_data, input_type=input_type)
        #print(type(self.client))
        self.logger.log_struct(log.dict())

    def log_prediction(self, 
                       prediction:dict = None,
                       input_features:dict = None,
                       model_id:str = None,
                       process_time:float = None,
                       date: str = None,
                       input_type:str = None
                       ):
        """ log_prediction send log with the information of the prediction.

        Parameters 
        ------------
         prediction: dictionary
            Prediction made by the model. 
         process_time: float
            Time taken to perform the prediction.
         date: string
            Date and time the prediction was made.
         model_id: string
            ID of the model that made the prediction.
         input_features: dictionary
            Features used by the model to perform the prediction.
         input_type: string
            Input type used by the model, can be 'raw_input' or 'model_features'.
        """
        allowed_inputs_labels = ['model_features']
        if input_type not in allowed_inputs_labels:
            raise ValueError("input_type must be one of these: {0}" \
                                    .format(",".join(allowed_inputs_labels)))
        if not input_features:
            raise ValueError("input_features are empty")
        if not prediction:
            raise ValueError("prediction is empty")
        if not model_id:
            raise ValueError("model_id is empty") 
        if not process_time:
            raise ValueError("process_time is empty") 
        
        # Classes Prediction and LogInput required by LogPrediction, contains infomation about prediction values and features used by the model
        pred = Prediction(prediction=prediction, time=process_time, prediction_date=date)
        log_in = LogInput(user=self.user, data=input_features, input_type=input_type)
        
        log = LogPrediction(predict=pred, input=log_in)
        print(log.dict())
        #print(dir(self.client))
        self.logger.log_struct(log.dict())
        pass

    def log_prediction_error(self, 
                       msg_error:str = None,
                       model_id:str =None,
                       error_date: str = None,
                       input_data:dict = None,
                       input_type:str = None
                       ):
        """ log_prediction_error send log with the description of the prediction error. 
         
        Parameters
        ------------
         msg_error: string 
            Message with the description of the error.
         model_id: string
            ID of the model that made the prediction.
         error_date: string 
            Date and time when the error was generated.
         input_data: dictionary
            Input used by the model to perform the prediction.
         input_type: string
            Input type used by the model, can be 'raw_input' or 'model_features'.
        """ 
        allowed_inputs_labels = ['raw_input','model_features']
        if input_type not in allowed_inputs_labels:
            raise ValueError("input_type must be one of these: {0}" \
                                    .format(",".join(allowed_inputs_labels)))
        if not msg_error:
            raise ValueError("The error message has not been entered")
        if not model_id:
            raise ValueError("model_id is empty")
        if not error_date:
            raise ValueError("error_date is empty")
        if not input_data:
            raise ValueError("input_data is empty")

        log_in = LogInput(user=self.user, data=input_data, input_type=input_type)
        log = LogPredictionError(msg=msg_error, model_id=model_id, date=error_date, input=log_in)
        self.logger.log_struct(log.dict())
        pass

if __name__ == "__main__":
    logger = Logger()
