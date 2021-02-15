from pathlib import Path

# loading configurations
SURVEY_DATA_PATH = (Path(__file__).parent.parent.parent / None).resolve()
S3_PROFILE_NAME = None
S3_BUCKET_NAME = None
S3_KEY = None


def LOCAL_LOAD_FUNC(path): pass


def S3_LOAD_FUNC(obj): pass


# Global variables
key_variable_A = None
key_variable_B = None
