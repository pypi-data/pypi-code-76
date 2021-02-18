from pydantic import BaseModel 

class LogInfo(BaseModel):
    log_type: str
    user: str
    project: str
    date: str
    info: dict

class Prediction(BaseModel):
    prediction: dict
    model_id: str
    process_time: float
    prediction_date: str
    model_features: dict
    
class LogInput(BaseModel):
    log_type: str
    user: str
    input_raw: dict

class LogPrediction(BaseModel):
    log_type: str
    predict: Prediction
    input: LogInput
    
class LogPredictionError(BaseModel):
    log_type: str 
    msg_error: str
    model_id: str
    date: str
    input: LogInput

