
import os

# Functions for checking error handling
def sample_valid_execute_function(params):
    return {'sum': params['x'] + params['y'], 'just_x': params['x']}

def sample_invalid_execute_function_list(params):
    return [params['x'] + params['y'], params['x']]

def sample_possibly_crashing_function(params):
    if params['x'] > 3:
        raise ValueError("x is greater than 3")
    return [params['x'] + params['y'], params['x']]


# Functions for checking if cleanup works
_TEST_FILE_PATH = '.test_temporary_file'
def _make_environment_dirty():
    with open(_TEST_FILE_PATH, 'w') as file_:
        file_.write("A very dirty string")

def _is_environment_dirty():
    return os.path.isfile(_TEST_FILE_PATH)

def _make_environment_clean():
    if _is_environment_dirty():
        os.remove(_TEST_FILE_PATH)

def sample_cleanup_function(params):
    _make_environment_clean()

def sample_execute_function_to_test_cleanup(params):
    was_environment_clean = 1 if not _is_environment_dirty() else 0
    _make_environment_dirty()
    return {'sum': params['x'] + params['y'], 'just_x': params['x'], 'was_environment_clean': was_environment_clean}

def sample_manual_func(*args, **kwargs):
    return (list(args), kwargs)
