from circle.resources.abstract import CreateableAPIResource, RetrievableAPIResource

from circle.resources.abstract.nested_resource_class_methods import (
    nested_resource_class_methods,
)
from circle.resources.wire_instruction import WireInstruction


# We support obtaining wire instructions on a specific account using a nested resource.
# In this case, circle.Wire.retrieve_instructions("your_wire_id")
@nested_resource_class_methods("instructions", WireInstruction, operations=["retrieve"])
class Wire(CreateableAPIResource, RetrievableAPIResource):
    OBJECT_NAME = "banks.wires"
