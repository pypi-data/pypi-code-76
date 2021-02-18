from pydantic import BaseModel 

class logInfo(BaseModel):
    log_type: str
    user: str
    project: str
    date: str

class Prediction(BaseModel):
    prediction: dict
    time: float
    prediction_date: str

class LogInput(BaseModel):
    log_type: str
    user: str
    data: dict
    input_type: str

class LogPrediction(BaseModel):
    log_type: str
    predict: Prediction
    input: LogInput
    
class LogPredictionError(BaseModel):
    log_type: str 
    msg: str
    model_id: str
    date: str
    input: LogInput

