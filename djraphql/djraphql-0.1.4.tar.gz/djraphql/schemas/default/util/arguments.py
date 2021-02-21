from graphene import Int, List, Argument
from six import iteritems
from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Lower
from functools import reduce

SCHEMA_BUILDER_SETTINGS = getattr(settings, "SCHEMA_BUILDER", {})
# default number of records retrieved for list query if no limit specified
DEFAULT_MAXIMUM_RESULTS = SCHEMA_BUILDER_SETTINGS.get("DEFAULT_MAXIMUM_RESULTS", 50)
# maximum number of records a list query can retrieve
ABSOLUTE_MAXIMUM_RESULTS = SCHEMA_BUILDER_SETTINGS.get("ABSOLUTE_MAXIMUM_RESULTS", 500)


def create_query_arguments(where_type, order_by_type):
    return {
        "where": Argument(where_type),
        "order_by": Argument(List(order_by_type)),
        "limit": Argument(Int),
        "offset": Argument(Int),
    }


def update_queryset_based_on_arguments(queryset, args, take_slice=True):
    if "where" in args:
        annotations = dict()
        q = filter_from_where_args(args["where"], annotations)
        queryset = queryset.annotate(**annotations).filter(q)

    if "order_by" in args:
        sort_order = []
        for sort_entry in args["order_by"]:
            sort_keys = list(sort_entry.keys())
            assert len(sort_keys) == 1, "order_by items can only have 1 key."
            sort_key = sort_keys[0]
            sort_values = list(sort_entry.values())
            sort_direction = sort_values[0]
            dash = "" if sort_direction == "ascending" else "-"
            sort_order.append("{}{}".format(dash, sort_key))
        queryset = queryset.order_by(*sort_order)

    if take_slice:
        limit = min(
            args.get("limit", DEFAULT_MAXIMUM_RESULTS), ABSOLUTE_MAXIMUM_RESULTS
        )
        offset = args.get("offset", 0)
        queryset = queryset[offset: offset + limit]

    return queryset


def filter_from_where_args(where_args, annotations, _and=True):
    combined_qs = []
    for key, value in iteritems(where_args):
        # Conjunction operations
        if key in ("_and", "_or"):
            joined = reduce(
                lambda result, q: q & result if key == "_and" else q | result,
                [filter_from_where_args(item, annotations) for item in value],
            )
            combined_qs.append(joined)

        # Negation operation
        if key == "_not":
            combined_qs.append(~filter_from_where_args(value, annotations))

        # Predicate operations
        if "_eq" in value:
            combined_qs.append(Q(**{key: value["_eq"]}))
        if "_neq" in value:
            combined_qs.append(~Q(**{key: value["_neq"]}))
        if "_gt" in value:
            combined_qs.append(Q(**{"{}__gt".format(key): value["_gt"]}))
        if "_gte" in value:
            combined_qs.append(Q(**{"{}__gte".format(key): value["_gte"]}))
        if "_lt" in value:
            combined_qs.append(Q(**{"{}__lt".format(key): value["_lt"]}))
        if "_lte" in value:
            combined_qs.append(Q(**{"{}__lte".format(key): value["_lte"]}))
        if "_in" in value:
            combined_qs.append(Q(**{"{}__in".format(key): value["_in"]}))
        if "_nin" in value:
            combined_qs.append(~Q(**{"{}__in".format(key): value["_nin"]}))
        if "_is_null" in value:
            combined_qs.append(Q(**{"{}__isnull".format(key): value["_is_null"]}))
        if "_like" in value:
            combined_qs.append(Q(**{"{}__contains".format(key): value["_like"]}))
        if "_ilike" in value:
            annotations["{}_lower".format(key)] = Lower(key)
            combined_qs.append(
                Q(**{"{}_lower__icontains".format(key): value["_ilike"].lower()})
            )

    if not combined_qs:
        # If we're here, the where clause contains a nested join, e.g.
        # albums(where: { artist: { label: { name: {_eq: "Record Co."}}}})
        # which means we need to generate Q(artist__label__name='Record Co.')
        for next_key, next_value in iteritems(value):
            nested_key = "{}__{}".format(key, next_key)
            combined_qs.append(
                filter_from_where_args({nested_key: next_value}, annotations)
            )

    if not combined_qs:
        print("Warning: combined_qs should never be empty at this point.")

    # Join them all together using ANDs or ORs.
    return reduce(lambda result, q: q & result if _and else q | result, combined_qs)
