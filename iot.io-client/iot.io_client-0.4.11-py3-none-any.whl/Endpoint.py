import enum
from typing import Union, List, Dict

# type which counts both int and float as valid
num_type = Union[int, float]
filter_list = Union[str]
enum_list = Dict[str, str]


# valid endpoint types
class EndpointType(enum.Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    STRING = "string"
    ENUM = "enum"


# endpoint constraint object, used to define the constraints on the data which is accepted by the client endpoint
class EndpointConstraint:
    def __init__(self, min_v: num_type = None, max_v: num_type = None, increment: num_type = None, length: int = None,
                 allow_list: filter_list = None, deny_list: filter_list = None, values: enum_list = None):
        # integer constraints
        self.min = min_v
        self.max = max_v
        self.increment = increment

        # string constraints
        self.length = length
        self.allow_list = allow_list
        self.deny_list = deny_list

        # enum constraints
        self.values = values

    # get the constraint info as a dict given the type of endpoint
    def get_constraint_data(self, data_type: EndpointType) -> dict:
        data = {}

        # constraint for number
        if data_type == EndpointType.INTEGER:
            if self.min is not None:
                data["min"] = self.min

            if self.max is not None:
                data["max"] = self.max

            if self.increment is not None:
                data["increment"] = self.max
        # constraint for string
        elif data_type == EndpointType.STRING:
            if self.length is not None:
                data["length"] = self.length

            if self.allow_list is not None:
                data["allowList"] = self.allow_list

            if self.deny_list is not None:
                data["denyList"] = self.deny_list
        elif data_type == EndpointType.ENUM:
            if self.values is not None:
                data["values"] = self.values
            else:
                raise Exception("Endpoint's of type 'ENUM' require a constraint with the values field provided.")

        return data


# info about the endpoint such as it's generic name, specialId, and constraints
class EndpointInfo:
    def __init__(self, name: str, data_type: EndpointType, special_id: str = None,
                 constraints: EndpointConstraint = None):
        self.name = name
        self.type = data_type
        self.special_id = special_id
        self.constraints = constraints

    # return dict containing endpoint info given the endpoint's ID
    def get_info(self, endpoint_id: str):
        data = {
            "id": endpoint_id,
            "name": self.name,
            "type": self.type.value,
            "specialId": self.special_id
        }

        # if constraints are provided
        if self.constraints:
            if self.type == EndpointType.BOOLEAN:
                raise Exception("Endpoint's of type 'BOOLEAN' cannot accept constraints.")

            # get the constraints
            data["constraints"] = self.constraints.get_constraint_data(self.type)
        else:
            if self.type == EndpointType.ENUM:
                raise Exception("Endpoint's of type 'ENUM' require a constraint with the values field provided.")

            # populate the constraints field with null
            data["constraints"] = None

        return data
