import base64

from importlib import import_module
from django.conf import settings
from django.db import models
from django.core.files.base import ContentFile

try:
    from rest_framework.serializers import SerializerMetaclass
    from rest_framework.response import Response
    from rest_framework import status
    from rest_framework import serializers
except ModuleNotFoundError:
    pass


class Base(models.Model):
    @classmethod
    def classname(cls):
        return cls.__name__

    @classmethod
    def get_serializer_name(cls) -> str:
        return '{}Serializer'.format(cls.classname())

    @classmethod
    def get_short_serializer_name(cls) -> str:
        return '{}ShortSerializer'.format(cls.classname())

    @classmethod
    def get_serializer(cls) -> SerializerMetaclass:
        name = cls.get_serializer_name()
        module = import_module(settings.SERIALIZERS_PATH)

        return getattr(module, name)

    @classmethod
    def get_short_serializer(cls) -> SerializerMetaclass:
        name = cls.get_short_serializer_name()
        module = import_module( settings.SERIALIZERS_PATH )

        return getattr( module, name )

    @property
    def serialize_data(self):
        serializer = self.__class__.get_serializer()
        if isinstance(serializer, SerializerMetaclass):
            return serializer(instance=self).data

        return None

    def _serialize_data(self, request):
        serializer = self.__class__.get_serializer()
        if isinstance(serializer, SerializerMetaclass):
            return serializer(instance=self, context={'request': request}).data

        return None

    @property
    def short_serialize_data(self):
        serializer = self.__class__.get_short_serializer()

        if isinstance(serializer, SerializerMetaclass):
            return serializer(instance=self).data

        return None

    def get_default_queryset(self):
        return self.objects.all()

    class Meta:
        abstract = True


class ImageBase64Field(serializers.ImageField):
    def to_representation(self, value):
        return super().to_representation(value)

    def to_internal_value(self, value):
        base64_image = value
        data = value
        if base64_image.startswith('data:image'):
            format, imgstr = base64_image.split(';base64,')
            ext = format.split( '/' )[-1]
            name = f'{uuid.uuid4()}.{ext}'
            data = ContentFile(base64.b64decode(imgstr), name=name)

        return super(ImageBase64Field, self).to_internal_value(data)


class Error:
    def __init__(self, message):
        self.message = message

    def render(self):
        error = {
            "code": 1000,
            "message": self.message,
            "errors": []
        }

        return error


class ResponsesMixin:
    def simple_text_response(self, message=None):
        if message is None:
            message = "Your request was successfully accepted and processed"
        data = {
            "detail": message
        }

        return Response(data, status=status.HTTP_200_OK)

    def success_objects_response(self, data):
        return Response(data, status=status.HTTP_200_OK)

    def error_response(self, error_message):
        error = error_message
        if type(error_message) is str:
            error = Error(error_message).render()

        return Response(error, status=status.HTTP_400_BAD_REQUEST)
