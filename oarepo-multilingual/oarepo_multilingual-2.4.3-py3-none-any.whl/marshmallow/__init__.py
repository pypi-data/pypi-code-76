"""Support for multilingual strings in oarepo invenio repository."""

import re

import pycountry
from flask import current_app

from marshmallow import INCLUDE, Schema, ValidationError, validates_schema
from marshmallow.fields import Nested

validation_error = lambda v: ValidationError(
    v,
    'Language must be a lower-cased 2-letter ISO 639-2 string, followed optionally by "-" and another '
    '2-letter lower-cased locale/country string (e.g. "cs-cz").',
)


def validate_iso639_2(value):
    """Validate that language is ISO 639-2 value."""
    if not pycountry.languages.get(alpha_2=value):
        raise validation_error(value)


class MultilingualStringPartSchemaV2(Schema):

    @validates_schema
    def validate_schema(self, data, **kwargs):
        list_data = list(data)
        for s in list_data:
            if s == "_": continue #defalut value
            try:
                if "SUPPORTED_LANGUAGES" in current_app.config and s not in current_app.config["SUPPORTED_LANGUAGES"]:
                    raise ValidationError(s, "Wrong language name. Supported languages: %s" % current_app.config[
                        "SUPPORTED_LANGUAGES"])
                continue
            except ValidationError:
                raise
            except RuntimeError:  # thrown if not in app_context
                pass
            if not re.match('^[a-z][a-z]$', s) and not re.match('^[a-z][a-z]-[a-z][a-z]$', s):
                raise validation_error(s)

            validate_iso639_2(s[0:2])

            if not isinstance((data[s]), str):
                raise ValidationError(s, "Wrong data type")

    class Meta:
        unknown = INCLUDE


def MultilingualStringV2(**kwargs):
    """Return a schema for multilingual string."""
    return Nested(MultilingualStringPartSchemaV2(), **kwargs)


__all__ = ('MultilingualStringV2',)
