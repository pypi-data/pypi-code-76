import logging
from typing import List

import jsons
from cms.models import Page
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.template.defaultfilters import title
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from link_all.cms_plugins import SelectableModelInstance
from link_all.dataclasses import LinkAllModel
from link_all.models import FilerFileLinkable
from link_all.settings import LINK_ALL_MODELS


logger = logging.getLogger(__name__)


@api_view(['GET'])
def link_type_list_view(request: Request) -> Response:
    for model in LINK_ALL_MODELS:
        content_type = ContentType.objects.get(app_label=model.app_label, model=model.model_name)
        model.content_type_pk = content_type.pk

        if not model.verbose_name:
            Model = apps.get_model(content_type.app_label, content_type.model)
            model.verbose_name = title(str(Model._meta.verbose_name))

    return Response(jsons.dump(LINK_ALL_MODELS))


@api_view(['GET'])
def link_type_detail_view(request: Request, **kwargs) -> Response:
    content_type_pk = kwargs.get('pk')
    content_type = ContentType.objects.get(pk=content_type_pk)
    Model = apps.get_model(content_type.app_label, content_type.model)
    selectable_model_instances: List[SelectableModelInstance] = []
    link_all_model: LinkAllModel = _get_link_all_model_by_content_type(content_type)
    if Model == Page:
        instances_all = Model.objects.filter(publisher_is_draft=False)
    elif Model == FilerFileLinkable:
        instances_all = Model.objects.all().prefetch_related('file')
    else:
        instances_all = Model.objects.all()
    for instance in instances_all:
        selectable_model_instances.append(
            SelectableModelInstance(
                pk=instance.pk,
                url=get_link_instance_url(instance, link_all_model),
                label=str(instance),
                is_show_url_in_select=link_all_model.is_show_url_in_select,
            )
        )
    return Response(jsons.dump(selectable_model_instances))


def get_link_instance_url(instance: Model, link_all_model: LinkAllModel) -> str:
    url_attr = getattr(instance, link_all_model.url_method, None)
    if url_attr is None:
        error = f"Link all: the specified url method returned a None, falling back to rendering an empty url."
        if instance is None:
            logger.error(error)
        else:
            try:
                logger.error(
                    error,
                    extra={
                        'instance': instance,
                        'model': instance.link_content_type.model if instance.link_content_type else None,
                        'page': instance.page,
                        'link_all_model.model_name': link_all_model.model_name,
                        'link_all_model.url_method': link_all_model.url_method,
                    },
                )
            except:
                logger.error("Link rendering logging failed.")
        return ''
    if type(url_attr) == str:
        return url_attr
    else:
        return url_attr()


def _get_link_all_model_by_content_type(content_type: ContentType) -> LinkAllModel:
    for model in LINK_ALL_MODELS:
        if (
            model.app_label == content_type.app_label and
            model.model_name == content_type.model
        ):
            return model
    else:
        raise Exception("Invalid content type.")
