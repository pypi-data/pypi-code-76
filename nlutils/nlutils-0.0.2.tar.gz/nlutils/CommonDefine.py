from enum import Enum


class DevelopMode(Enum):
    DEBUG = 0
    RELEASE =1
class OperationStatus(Enum):
    SUCCESS = 0
    FAIL = 1
class FigureType(Enum):
    HEATMAP_PLOT = 0
    POLYLINE_PLOT = 1
    BAR_PLOT = 2
    SCATTER_PLOT = 3
    HISTOGRAM_PLOT = 4
    HISTOGRAM_2D_PLOT = 5

class ParameterType(Enum):
    MODEL = 0
    DATA = 1
    TRANINING = 2
    MISCELLANEOUS = 3

class ParameterHandlerOperation(Enum):
    INSERT = 0
    DELETE = 1
    UPDATE = 2
    SELECT = 3

class TaskTheme(Enum):
    NLP = 0
    CV = 1
    DS = 2

class NLPTaksType(Enum):
    NER = 0

class DataType(Enum):
    NUMPY_ARRAY = 0
    LIST = 1

class LogLevel(Enum):
    FATAL = 0
    ERROR = 1
    EXCEPTION = 2
    WARNING = 3
    INFO = 4
    PERFORMANCE = 5
    DEBUG = 6


DEV_MODE = DevelopMode.DEBUG