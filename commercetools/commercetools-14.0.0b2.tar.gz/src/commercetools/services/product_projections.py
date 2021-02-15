# DO NOT EDIT! This file is automatically generated
import typing

import marshmallow
from marshmallow import fields

from commercetools.helpers import OptionalList, RemoveEmptyValuesMixin
from commercetools.platform.models.product import (
    ProductProjection,
    ProductProjectionPagedQueryResponse,
    ProductProjectionPagedSearchResponse,
)
from commercetools.typing import OptionalListStr

from . import abstract, traits


class _ProductProjectionGetSchema(traits.ExpandableSchema, traits.PriceSelectingSchema):
    staged = fields.Bool(required=False, missing=False)


class _ProductProjectionQuerySchema(
    traits.ExpandableSchema,
    traits.SortableSchema,
    traits.PagingSchema,
    traits.QuerySchema,
    traits.PriceSelectingSchema,
):
    staged = fields.Bool(required=False, missing=False)


class _ProductProjectionSearchSchema(
    traits.SortableSchema,
    traits.PagingSchema,
    traits.PriceSelectingSchema,
    traits.ExpandableSchema,
):
    fuzzy = fields.Bool(required=False, missing=False)
    fuzzy_level = fields.Int(data_key="fuzzyLevel", required=False)
    mark_matching_variants = fields.Bool(data_key="markMatchingVariants", missing=False)
    staged = fields.Bool(required=False, missing=False)
    filter = OptionalList(fields.String(), required=False)
    filter_facets = OptionalList(
        fields.String(), data_key="filter.facets", required=False
    )
    filter_query = OptionalList(
        fields.String(), data_key="filter.query", required=False
    )
    facet = OptionalList(fields.String(), required=False)
    text = fields.Dict()

    @marshmallow.post_dump
    def _text_post_dump(self, data, **kwrags):
        values = data.pop("text")
        if not values:
            return data
        for key, val in values.items():
            data[f"text.{key}"] = val
        return data

    @marshmallow.pre_load
    def _text_post_load(self, data, **kwrags):
        items = {}
        for key in list(data.keys()):
            if key.startswith("text."):
                items[key[5:]] = data[key]
                del data[key]
        data["text"] = items
        return data


class _ProductProjectionSuggestSchema(traits.SortableSchema, traits.PagingSchema):
    fuzzy = fields.Bool(required=False, missing=False)
    staged = fields.Bool(required=False, missing=False)
    search_keywords = fields.Dict()

    @marshmallow.post_dump
    def _search_keywords_post_dump(self, data, **kwrags):
        values = data.pop("search_keywords")
        if not values:
            return data
        for key, val in values.items():
            data[f"searchKeywords.{key}"] = val
        return data

    @marshmallow.pre_load
    def _search_keywords_post_load(self, data, **kwrags):
        items = {}
        for key in list(data.keys()):
            if key.startswith("searchKeywords."):
                items[key[15:]] = data[key]
                del data[key]
        data["search_keywords"] = items
        return data


class ProductProjectionService(abstract.AbstractService):
    """A projected representation of a product shows the product with its current
    or staged data.

    The current or staged representation of a product in a catalog is called a
    product projection.
    """

    def get_by_id(
        self,
        id: str,
        *,
        expand: OptionalListStr = None,
        price_currency: OptionalListStr = None,
        price_country: OptionalListStr = None,
        price_customer_group: OptionalListStr = None,
        price_channel: OptionalListStr = None,
        locale_projection: OptionalListStr = None,
        store_projection: OptionalListStr = None,
        staged: bool = None,
    ) -> ProductProjection:
        """Gets the current or staged representation of a product in a catalog by
        ID.

        When used with an API client that has the
        view_published_products:{projectKey} scope, this endpoint only returns
        published (current) product projections.
        """
        params = self._serialize_params(
            {
                "expand": expand,
                "price_currency": price_currency,
                "price_country": price_country,
                "price_customer_group": price_customer_group,
                "price_channel": price_channel,
                "locale_projection": locale_projection,
                "store_projection": store_projection,
                "staged": staged,
            },
            _ProductProjectionGetSchema,
        )
        return self._client._get(
            endpoint=f"product-projections/{id}",
            params=params,
            response_class=ProductProjection,
        )

    def get_by_key(
        self,
        key: str,
        *,
        expand: OptionalListStr = None,
        price_currency: OptionalListStr = None,
        price_country: OptionalListStr = None,
        price_customer_group: OptionalListStr = None,
        price_channel: OptionalListStr = None,
        locale_projection: OptionalListStr = None,
        store_projection: OptionalListStr = None,
        staged: bool = None,
    ) -> ProductProjection:
        """Gets the current or staged representation of a product found by Key.

        When used with an API client that has the
        view_published_products:{projectKey} scope, this endpoint only returns
        published (current) product projections.
        """
        params = self._serialize_params(
            {
                "expand": expand,
                "price_currency": price_currency,
                "price_country": price_country,
                "price_customer_group": price_customer_group,
                "price_channel": price_channel,
                "locale_projection": locale_projection,
                "store_projection": store_projection,
                "staged": staged,
            },
            _ProductProjectionGetSchema,
        )
        return self._client._get(
            endpoint=f"product-projections/key={key}",
            params=params,
            response_class=ProductProjection,
        )

    def query(
        self,
        *,
        expand: OptionalListStr = None,
        sort: OptionalListStr = None,
        limit: int = None,
        offset: int = None,
        with_total: bool = None,
        where: OptionalListStr = None,
        predicate_var: typing.Dict[str, str] = None,
        price_currency: OptionalListStr = None,
        price_country: OptionalListStr = None,
        price_customer_group: OptionalListStr = None,
        price_channel: OptionalListStr = None,
        locale_projection: OptionalListStr = None,
        store_projection: OptionalListStr = None,
        staged: bool = None,
    ) -> ProductProjectionPagedQueryResponse:
        """You can use the product projections query endpoint to get the current
        or staged representations of Products.

        When used with an API client that has the
        view_published_products:{projectKey} scope, this endpoint only returns
        published (current) product projections.   A projected representation of
        a product shows the product with its current or staged data. The current
        or staged representation of a product in a catalog is called a product
        projection.
        """
        params = self._serialize_params(
            {
                "expand": expand,
                "sort": sort,
                "limit": limit,
                "offset": offset,
                "with_total": with_total,
                "where": where,
                "predicate_var": predicate_var,
                "price_currency": price_currency,
                "price_country": price_country,
                "price_customer_group": price_customer_group,
                "price_channel": price_channel,
                "locale_projection": locale_projection,
                "store_projection": store_projection,
                "staged": staged,
            },
            _ProductProjectionQuerySchema,
        )
        return self._client._get(
            endpoint="product-projections",
            params=params,
            response_class=ProductProjectionPagedQueryResponse,
        )

    def search(
        self,
        mark_matching_variants: bool,
        *,
        sort: OptionalListStr = None,
        limit: int = None,
        offset: int = None,
        with_total: bool = None,
        price_currency: OptionalListStr = None,
        price_country: OptionalListStr = None,
        price_customer_group: OptionalListStr = None,
        price_channel: OptionalListStr = None,
        locale_projection: OptionalListStr = None,
        store_projection: OptionalListStr = None,
        expand: OptionalListStr = None,
        fuzzy: bool = None,
        fuzzy_level: int = None,
        staged: bool = None,
        filter: str = None,
        filter_facets: str = None,
        filter_query: str = None,
        facet: str = None,
        text: typing.Dict[str, str] = None,
    ) -> ProductProjectionPagedSearchResponse:
        """Search Product Projection

        This endpoint provides high performance search queries over
        ProductProjections. The query result contains the ProductProjections for
        which at least one ProductVariant matches the search query. This means
        that variants can be included in the result also for which the search
        query does not match. To determine which ProductVariants match the search
        query, the returned ProductProjections include the additional field
        isMatchingVariant.
        """
        params = self._serialize_params(
            {
                "sort": sort,
                "limit": limit,
                "offset": offset,
                "with_total": with_total,
                "price_currency": price_currency,
                "price_country": price_country,
                "price_customer_group": price_customer_group,
                "price_channel": price_channel,
                "locale_projection": locale_projection,
                "store_projection": store_projection,
                "expand": expand,
                "fuzzy": fuzzy,
                "fuzzy_level": fuzzy_level,
                "mark_matching_variants": mark_matching_variants,
                "staged": staged,
                "filter": filter,
                "filter_facets": filter_facets,
                "filter_query": filter_query,
                "facet": facet,
                "text": text,
            },
            _ProductProjectionSearchSchema,
        )
        return self._client._get(
            endpoint="product-projections/search",
            params=params,
            response_class=ProductProjectionPagedSearchResponse,
        )

    def suggest(
        self,
        *,
        sort: OptionalListStr = None,
        limit: int = None,
        offset: int = None,
        with_total: bool = None,
        fuzzy: bool = None,
        staged: bool = None,
        search_keywords: typing.Dict[str, str] = None,
    ) -> ProductProjection:
        """The source of data for suggestions is the searchKeyword field in a
        product
        """
        params = self._serialize_params(
            {
                "sort": sort,
                "limit": limit,
                "offset": offset,
                "with_total": with_total,
                "fuzzy": fuzzy,
                "staged": staged,
                "search_keywords": search_keywords,
            },
            _ProductProjectionSuggestSchema,
        )
        return self._client._get(
            endpoint="product-projections/suggest",
            params=params,
            response_class=ProductProjection,
        )
