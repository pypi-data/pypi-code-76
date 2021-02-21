from abc import ABCMeta, abstractmethod

from flask import request, Response
from pydantic import BaseModel

MIME_TYPE = 'application/json'


class AbstractRequestTransformer(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def transform(cls, *args, **kwargs) -> BaseModel:
        pass


class AbstractResponseTransformer(metaclass=ABCMeta):
    @abstractmethod
    def transform(self, *args, **kwargs) -> Response:
        pass


class EmptyResponseTransformer(AbstractResponseTransformer):
    @classmethod
    def transform(cls, *args, **kwargs):
        return Response(response="", status=204)


class YggdrasilRequestTransformer(AbstractRequestTransformer):
    @classmethod
    def transform(cls: BaseModel, *args, **kwargs):
        return cls.parse_raw(request.data)


class JSONResponseTransformer(AbstractResponseTransformer):
    def transform(self: BaseModel, *args, **kwargs):
        return Response(
            mimetype=MIME_TYPE,
            content_type=MIME_TYPE,
            response=self.json(exclude_none=True)
        )


class JSONErrorTransformer(AbstractResponseTransformer):
    def transform(self: BaseModel, *args, **kwargs):
        return Response(
            status=self.status,
            mimetype=MIME_TYPE,
            content_type=MIME_TYPE,
            response=self.copy(exclude={'status'}).json(exclude_none=True)
        )
