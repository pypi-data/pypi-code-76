from http import HTTPStatus

from django.conf import settings
from gramedia.django.drf import convert_env_boolean
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler

from kitchenart import _logger


class TimestampedSerializerMixin:
    """ Automatically attaches the modified_by to a model.

    .. warning::
        This is only for use with Timestemped models, with an attribute 'modified_by'
    """
    def modified_user(self):
        user = self.context['request'].user
        return f'{user.get_full_name()} <{user.email}>'

    def create(self, validated_data):
        validated_data['modified_by'] = self.modified_user()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['modified_by'] = self.modified_user()
        return super().update(instance, validated_data)


class SoftDeleteViewSetMixin:
    def get_queryset(self):
        if convert_env_boolean(self.request.query_params.get('include_deleted', '')):
            return self.queryset
        else:
            return self.queryset.filter(deleted__isnull=True)


class TranslationViewSetMixin:
    @action(detail=True, name='translation')
    def translation(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)


def get_entity_href_serializer(model_class, meta_extra_kwargs=None, *init_args, **init_kwargs):
    class EntityHrefSerializer(serializers.HyperlinkedModelSerializer):
        name = serializers.CharField(required=False)

        class Meta:
            model = model_class
            fields = ('href', 'name',)
            extra_kwargs = meta_extra_kwargs or {'href': {'lookup_field': 'slug', }, }
    return EntityHrefSerializer(*init_args, **init_kwargs)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {}
        if hasattr(exc, 'detail') and hasattr(exc.detail, 'items'):
            response.data['detail'] = exc.detail

        if isinstance(exc, APIException):
            response.data['message'] = exc.detail if isinstance(exc.detail, str) else exc.default_detail
        else:
            response.data['message'] = str(exc)
    else:
        _logger.error(exc)
        if not settings.DEBUG:
            response = Response({
                'message': HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                'detail': []
            }, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return response
