"""types module"""

from enum import Enum
import click


class Resource(Enum):
    """Matatika resource type enum"""

    WORKSPACE = 0
    DATASET = 1


class DataFormat(Enum):
    """Data format type enum"""

    RAW = 0
    CHARTJS = 1
    CSV = 2

    @classmethod
    def list_names(cls) -> tuple:
        """Get all data format names"""

        return tuple(cls.__members__.keys())

    @classmethod
    def get(cls, name: str):
        """Get a data format by name"""

        return cls.__members__.get(name.upper())


class DataFormatParamType(click.ParamType):
    """Custom data format click parameter type"""

    name = "data format"

    def convert(self, value, param, ctx):

        data_format = DataFormat.get(value)

        if not data_format:

            message = f"{value} is not a valid data format - choose from: " + \
                " | ".join(DataFormat.list_names())

            self.fail(message, param, ctx)

        return data_format


DATA_FORMAT = DataFormatParamType()
