import logging
import os.path
import json

logger = logging.getLogger(__name__)


def validate_time(entered_time):
    logger.debug("inside time validation: {0}" .format(type(entered_time)))
    if entered_time > 360:
        logger.error("entered time: {0}".format(entered_time), " is more than allowed time")
        return False
    else:
        return True


def validator_decorator(validate_func):
    def wrapper(*args, **kwargs):
        logger.debug("validating if file exists")
        if os.path.isfile(*args):
            logger.debug("file exists: {0}".format(*args))
        else:
            logger.error("file does not exists: {0}".format(*args))
            raise SystemExit
        return validate_func(*args, **kwargs)
    return wrapper


@validator_decorator
def validate_json(filename):
    logger.debug("validating json")
    try:
        with open(filename) as f:
            if json.load(f):
                return True
    except:
        logger.error("validation of json failed")
        raise SystemExit
