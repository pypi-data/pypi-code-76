from circle.resources.abstract import (
    CreateableAPIResource,
    ListableAPIResource,
    RetrievableAPIResource
)


class Transfer(CreateableAPIResource, ListableAPIResource):
    """
    https://developers.circle.com/reference#payouts-transfers-create
    """

    OBJECT_NAME = "transfers"  # The object name as it maps to the API resource.
