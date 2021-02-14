from enum import Enum, auto, unique


class AutoName(Enum):
    """
    This class enables us to customize/enhance the basic
    functionality of Enum. Please prefer to extend AutoName
    class instead of Enum when creating your own Enums.
    """

    def _generate_next_value_(self, start, count, last_values):
        """
        This method is over-ridden from original definition
        in order to return enum_member.name when auto() is
        called to assign values to enum members. It will
        keep values more consistent across the project
        without hard-coding them. Saves refactoring effort.
        """
        return self


class SubmissionTypeEnum(AutoName):
    NER_TRAINING = auto()
    APPLY_NER = auto()
    CLASSIFICATION_TRAINING = auto()
    APPLY_CLASSIFICATION = auto()
    TABLE_EXTRACTION_TRAINING = auto()


class SubmissionModeEnum(AutoName):
    UI = auto()
    BATCH_SYNC = auto()


class SubmissionExecutionFlowEnum(AutoName):
    RUNTIME = auto()
    TRAINING = auto()


class StatusEnum(AutoName):
    IN_PROCESS = auto()
    COMPLETE = auto()
    ERROR = auto()

class ProfileTypeEnum(AutoName):
    DATABASE = auto()
    FILE = auto()
    COMPUTE = auto()
    FAAS = auto()    


@unique
class ExecutionStepEnum(Enum):
    CREATE_NEW_SUBMISSION = ("CREATE_NEW_SUBMISSION",
                             "/bizai/create_submission")
    CREATE_NEW_REQUEST = ("CREATE_NEW_REQUEST", "/bizai/create_request")
    SPLIT_PDF = ("SPLIT_PDF", "/bizai/create_request")
    CONVERT_TO_IMAGE = ("CONVERT_TO_IMAGE", "")
    CONVERT_IMAGE_TO_HOCR = ("CONVERT_IMAGE_TO_HOCR", "")
    PARSE_HOCR = ("PARSE_HOCR", "/bizai/parse_hocr")
    STOPWORDS_FILTER = ("STOPWORDS_FILTER", "/bizai/stopwords_filter")
    NER_PREDICTION = ("NER_PREDICTION", "/bizai/ner_prediction")
    ANNOTATION = ("ANNOTATION", "/bizai/save_annotation")
    ERROR = ("ERROR", "/bizai/handle_error")
    LIST = ("LIST", "/bizai/list")
    SAVE_ENTITY = ("SAVE_ENTITY", "/bizai/save_entity")
    TASK_NER_TRAINING = ("TASK_NER_TRAINING", "/bizai/run_ner_task")

    #Client on-boarding functions
    DEFAULT_CONFIG = ("DEFAULT_CONFIG", "/bizai/default_config")
    CREATE_CLIENT = ("CREATE_CLIENT", "/bizai/create_client")
    CREATE_USER = ("CREATE_USER", "/bizai/create_user")
    CREATE_CLOUD_PROFILE = ("CREATE_CLOUD_PROFILE", "/bizai/onboarding/create_cloud_profile")
    CREATE_DB = ("CREATE_DB", "/bizai/onboarding/create_db")
    CREATE_OS = ("CREATE_OS", "/bizai/onboarding/create_os")
    CREATE_RUNTIME = ("CREATE_RUNTIME", "/bizai/onboarding/create_runtime")
    CREATE_TRAINING = ("CREATE_TRAINING", "/bizai/onboarding/create_training")

    def __init__(self, step, action):        
        self._step = step       
        self._action = action   

    def get_action(self):
        print ("action", self._action)
        return self._action