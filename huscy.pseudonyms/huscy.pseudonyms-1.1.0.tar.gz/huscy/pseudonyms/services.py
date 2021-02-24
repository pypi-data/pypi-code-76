import uuid

from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction

from huscy.pseudonyms.models import Pseudonym


def _get_content_type_object(content_type):
    if isinstance(content_type, ContentType):
        return content_type
    if isinstance(content_type, str):
        return ContentType.objects.get_by_natural_key(*content_type.split('.'))
    raise Exception(f'Type {type(content_type).__name__} not supported.')


def _generate_code():
    return uuid.uuid1().hex


def create_pseudonym(subject, content_type, object_id=None):
    content_type_object = _get_content_type_object(content_type)
    code = _generate_code()
    try:
        with transaction.atomic():
            return Pseudonym.objects.create(
                subject=subject, code=code, content_type=content_type_object, object_id=object_id
            )
    except IntegrityError:
        # try again if code is already in use
        return create_pseudonym(subject, content_type_object, object_id)


def get_pseudonym(subject, content_type, object_id=None):
    filters = {
        'subject': subject,
        'content_type': _get_content_type_object(content_type)
    }
    if object_id:
        filters['object_id'] = object_id
    return Pseudonym.objects.get(**filters)


def get_or_create_pseudonym(subject, content_type, object_id=None):
    content_type_object = _get_content_type_object(content_type)
    try:
        return get_pseudonym(subject, content_type_object, object_id)
    except Pseudonym.DoesNotExist:
        return create_pseudonym(subject, content_type_object, object_id)


def get_subject(pseudonym):
    return Pseudonym.objects.select_related('subject').get(code=pseudonym).subject


def get_subjects(pseudonyms):
    return {
        pseudonym.code: pseudonym.subject
        for pseudonym in Pseudonym.objects.filter(code__in=pseudonyms).select_related('subject')
    }
