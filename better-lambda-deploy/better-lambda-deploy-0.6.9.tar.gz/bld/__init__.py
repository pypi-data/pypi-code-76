import os
from .function import LambdaFunction  # NOQA
from .api_function import APIFunction  # NOQA
from .function import QueueFunction  # NOQA
from .function import ScheduleFunction  # NOQA


def get_env():
    environment = os.getenv("ENVIRONMENT", "local")
    return environment
