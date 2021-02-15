# This file is automatically generated by the rmf-codegen project.
#
# The Python code generator is maintained by Lab Digital. If you want to
# contribute to this project then please do not edit this file directly
# but send a pull request to the Lab Digital fork of rmf-codegen at
# https://github.com/labd/rmf-codegen
import re
import typing

import marshmallow
import marshmallow_enum

from commercetools import helpers

from ... import models

# Fields


# Marshmallow Schemas
class ImageSearchResponseSchema(helpers.BaseSchema):
    count = marshmallow.fields.Integer(allow_none=True, missing=None)
    offset = marshmallow.fields.Float(allow_none=True, missing=None)
    total = marshmallow.fields.Integer(allow_none=True, missing=None)
    results = helpers.LazyNestedField(
        nested=helpers.absmod(__name__, ".ResultItemSchema"),
        allow_none=True,
        many=True,
        unknown=marshmallow.EXCLUDE,
        missing=None,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data, **kwargs):

        return models.ImageSearchResponse(**data)


class ResultItemSchema(helpers.BaseSchema):
    image_url = marshmallow.fields.String(
        allow_none=True, missing=None, data_key="imageUrl"
    )
    product_variants = helpers.LazyNestedField(
        nested=helpers.absmod(__name__, ".common.ProductVariantSchema"),
        allow_none=True,
        many=True,
        unknown=marshmallow.EXCLUDE,
        missing=None,
        data_key="productVariants",
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data, **kwargs):

        return models.ResultItem(**data)
