"""Language aware filters, matchers and facets for invenio-records-rest."""
import logging

from elasticsearch_dsl import Q
from invenio_i18n.selectors import get_locale

log = logging.getLogger('oarepo-multilingual.rest')


def language_aware_field(fld):
    """
    Return callable that adds language code to the field.

    :param fld field name
    :return callable adding current language
    """

    def ev():
        try:
            locale = get_locale()
        except:
            log.error('Exception in get_locale. Are you sure that you have added invenio_i18n to api_apps?')
            raise
        return f'{fld}.{locale}'

    return ev


def language_aware_text_terms_filter(field, suffix='.raw'):
    """
    Return terms filter on field.{language}.raw (the default suffix for raw subfield in text field).

    :param field  name of the field
    :param suffix the suffix to add to the localized field name
    :return invenio terms filter
    """
    field = language_aware_field(field)

    def inner(values):
        return Q('terms', **{f'{field()}{suffix}': values})

    return inner


def language_aware_terms_filter(field):
    """
    Return terms filter on field.{language} (the default suffix for raw subfield in text field).

    :param field  name of the field
    :return invenio terms filter
    """
    return language_aware_text_terms_filter(field, suffix='')


def language_aware_text_match_filter(field, **kwargs):
    """
    Return fulltext match on field.{language}.

    :param field  name of the field
    :param kwargs extra arguments (for example, analyzer) to add to the matcher
    :return invenio matcher filter
    """
    field = language_aware_field(field)

    def inner(values):
        if not len(values):
            return Q('match_none')
        fld = field()
        args = {
            k: v(field=fld) if callable(v) else v for k, v in kwargs.items()
        }

        if len(values) == 1:
            return Q('match', **{
                f'{fld}': {
                    'query': values[0],
                    **args
                }
            })

        return Q('bool', should=[
            Q('match', **{
                f'{fld}': {
                    'query': val,
                    **args
                }
            }) for val in values
        ], minimum_should_match=1)

    return inner


def language_aware_text_term_facet(field, order_field="_count", order='desc', size=100, suffix='.raw'):
    """
    Return terms facet on field.{language}.raw (the default suffix for raw subfield in text field).

    :param field  name of the field
    :param suffix the suffix to add to the localized field name
    :param order_field  on wich field to order the facet
    :param order        order direction
    :param size         how many bucket values to return
    :return invenio rest facet
    """
    field = language_aware_field(field)

    def inner():
        return {
            'terms': {
                'field': f'{field()}{suffix}',
                'size': size,
                "order": {order_field: order}
            },
        }

    return inner


def language_aware_term_facet(field, order_field="_count", order='desc', size=100):
    """
    Return terms facet on field.{language}.raw (the default suffix for raw subfield in text field).

    :param field  name of the field
    :param order_field  on wich field to order the facet
    :param order        order direction
    :param size         how many bucket values to return
    :return invenio rest facet
    """
    return language_aware_text_term_facet(field=field, order_field=order_field, order=order, size=size, suffix='')


__all__ = (
    'language_aware_field',
    'language_aware_text_terms_filter',
    'language_aware_terms_filter',
    'language_aware_text_match_filter',

    'language_aware_text_term_facet',
    'language_aware_term_facet'
)
