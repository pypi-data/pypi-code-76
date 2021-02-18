import requests
from .exceptions import (
    InvalidServiceResponseException,
    ValidationErrorException,
    DuplicateConstraintViolationException,
    ResourceNotFoundException,
    ConnectionTimeoutException,
    ReadTimeoutException
)


class BaseClient:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.url = "http://{}:{}/".format(ip, port)
        self.session = requests.Session()

    def get(self, path):
        response = self.session.get(self.url + path)
        return self.decode_response(response=response)

    def post(self, path, **data):
        response = self.session.post(self.url + path, data=data)
        return self.decode_response(response=response)

    def put(self, path, **data):
        response = self.session.put(self.url + path, data=data)
        return self.decode_response(response=response)

    def delete(self, path, **data):
        response = self.session.delete(self.url + path, data=data)
        return self.decode_response(response=response)

    def version(self):
        return self.get("/version")

    def decode_response(self, response):
        """
        This method is used to decode and/or parse the returned response object from requests
        Implementers can (and should) use this method to tailor the client to the format of
        their usual responses. This default method assumes the old (slightly weird) convention
        of having either a response or error object in the return body with the actual data in it.
        """
        status = response.status_code
        try:
            body = response.json()
        except Exception:
            # If valid response (200-299) this will cause InvalidServiceBlah, else correct exception will propagate:)
            body = {'error': {'message': response.body}}

        if (200 <= status <= 299) or status in [400, 404, 409, 502, 504]:
            # handle 200's - Everything is ok
            if 200 <= status <= 299:
                if body.get('response') is None:
                    raise InvalidServiceResponseException(status_code=status, message="Unable to decode the response "
                                                                                      "received from the api due to "
                                                                                      "missing 'response' element.")
                return body['response']
            # handle 400 - Client error/ validation errors
            if status == 400:
                raise ValidationErrorException(status_code=status, message=body['error']['message'])
            # handle 404 - Resource not found
            if status == 404:
                raise ResourceNotFoundException(status_code=status, message=body['error']['message'])
            # handle 409 - Conflicting resource
            if status == 409:
                raise DuplicateConstraintViolationException(status_code=status, message=body['error']['message'])
            # handle 502 - Connecting to service timed out
            if status == 502:
                raise ConnectionTimeoutException(status_code=status, message=body['error']['message'])
            # handle 504 - Read timed out
            if status == 504:
                raise ReadTimeoutException(status_code=status, message=body['error']['message'])
        else:
            raise InvalidServiceResponseException(status_code=status, message=body.get('error', {}).
                                                  get('message',
                                                      "An error occurred during communication with the api."))
