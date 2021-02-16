from circle import api_requestor, util
from circle.resources.abstract.api_resource import APIResource


class CreateableAPIResource(APIResource):
    @classmethod
    def create(cls, api_key=None, idempotency_key=None, **params):

        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url()
        response, api_key = requestor.request("post", url, params)
        return util.convert_to_circle_object(
            response, api_key, klass_name=cls.OBJECT_NAME
        )
