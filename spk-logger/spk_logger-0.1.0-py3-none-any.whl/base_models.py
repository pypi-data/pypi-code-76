from pydantic import BaseModel 
"""
class Log_info(BaseModel):
    model_id: int
    log_type: str
    project_id: id
    prediction_date: datetime
    user: str
"""

class Prediction(BaseModel):
    prediction: dict
    time: float
    prediction_date: str

class LogInput(BaseModel):
    user: str
    data: dict
    input_type: str

class LogPrediction(BaseModel):
    predict: Prediction
    input: LogInput
    
class LogPredictionError(BaseModel):  
    msg: str
    model_id: str
    date: str
    input: LogInput

