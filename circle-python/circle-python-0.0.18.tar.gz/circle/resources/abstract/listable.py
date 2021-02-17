from circle import util
from circle.api_requestor import APIRequestor
from circle.resources.abstract.api_resource import APIResource


class ListableAPIResource(APIResource):
    @classmethod
    def list(cls, api_key=None, **params):
        requestor = APIRequestor(api_key)
        url = cls.class_url()
        response, api_key = requestor.request("get", url, params)
        circle_object = util.convert_to_circle_object(response, api_key)
        return circle_object
