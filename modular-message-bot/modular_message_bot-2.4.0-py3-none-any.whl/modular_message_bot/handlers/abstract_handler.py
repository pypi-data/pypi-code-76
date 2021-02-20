from abc import ABC, abstractmethod

from modular_message_bot.config.config_collection import ConfigCollection
from modular_message_bot.config.config_interpolator import ConfigInterpolator
from modular_message_bot.models.job import JobConfigSection
from modular_message_bot.string_interpolator import StringInterpolator


class AbstractHandler(ABC):
    """
    Sub class for all inputs and outputs
    """

    def __init__(
        self,
        config: ConfigCollection,
        dynamic_config_interpolator: ConfigInterpolator,
        job_string_interpolator: StringInterpolator,
    ):
        self.config = config
        self.dynamic_config_interpolator = dynamic_config_interpolator
        self.job_string_interpolator = job_string_interpolator

    @classmethod
    @abstractmethod
    def get_code(cls) -> str:
        """
        Gets the unique code of this handler
        :return:
        """
        raise NotImplementedError

    def validate_job_config(self, job_config: JobConfigSection) -> str:
        return ""
