

class InvalidPredictionException(Exception):
    """
    Base Exception for Prediction Output Validation
    """
    def __init__(self, message):
        super().__init__(message)
