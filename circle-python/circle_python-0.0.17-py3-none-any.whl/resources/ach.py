from circle.resources.abstract import (
    CreateableAPIResource,
    RetrievableAPIResource
)


class Ach(CreateableAPIResource, RetrievableAPIResource):

    OBJECT_NAME = "banks.ach"
