"""The endpoints for tenant objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Dict, Mapping, Sequence, Union

import cg_request_args as rqa

from ..models.base_error import BaseError
from ..models.create_tenant_data import CreateTenantData
from ..models.extended_tenant import ExtendedTenant
from ..models.patch_tenant_data import PatchTenantData
from ..models.tenant_statistics import TenantStatistics
from ..parsers import JsonResponseParser, ParserFor, ResponsePropertyParser
from ..utils import (
    get_error,
    log_warnings,
    response_code_matches,
    to_dict,
    to_multipart,
)

if TYPE_CHECKING:
    from ..client import AuthenticatedClient, Client


def get_all(
    *,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "Client",
) -> Sequence[ExtendedTenant]:
    """Get all tenants of an instance.

    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: All the tenants of this instance.
    """
    url = "/api/v1/tenants/"
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            rqa.List(ParserFor.make(ExtendedTenant))
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def create(
    multipart_data: CreateTenantData,
    *,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> ExtendedTenant:
    """Create a new tenant.

    :param multipart_data: The data that should form the body of the request.
        See :model:`.CreateTenantData` for information about the possible
        fields.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The newly created tenant.
    """
    url = "/api/v1/tenants/"
    params = extra_parameters or {}

    response = client.http.post(
        url=url, files=to_multipart(to_dict(multipart_data)), params=params
    )
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(ParserFor.make(ExtendedTenant)).try_parse(
            response
        )
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get_stats(
    *,
    tenant_id: "str",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> TenantStatistics:
    """Get the statistics of a tenant.

    :param tenant_id: The id of the tenant for which you want to get the
        statistics.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The statistics of the specified tenant.
    """
    url = "/api/v1/tenants/{tenantId}/statistics/".format(tenantId=tenant_id)
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(ParserFor.make(TenantStatistics)).try_parse(
            response
        )
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get_logo(
    *,
    tenant_id: "str",
    dark: "bool" = False,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "Client",
) -> bytes:
    """Get the logo of a tenant.

    :param tenant_id: The id of the tenant for which you want to get the logo.
    :param dark: If truhty the retrieved logo will be suited for the dark
        theme.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The logo of the tenant.
    """
    url = "/api/v1/tenants/{tenantId}/logo".format(tenantId=tenant_id)
    params: Dict[str, Any] = {
        **(extra_parameters or {}),
        "dark": to_dict(dark),
    }

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return ResponsePropertyParser("content", bytes).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get(
    *,
    tenant_id: "str",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "Client",
) -> ExtendedTenant:
    """Get a tenant by id.

    :param tenant_id: The id of the tenant you want to retrieve.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The tenant with the given id.
    """
    url = "/api/v1/tenants/{tenantId}".format(tenantId=tenant_id)
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(ParserFor.make(ExtendedTenant)).try_parse(
            response
        )
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def patch(
    json_body: PatchTenantData,
    *,
    tenant_id: "str",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> ExtendedTenant:
    """Update a tenant by id.

    :param json_body: The body of the request. See :model:`.PatchTenantData`
        for information about the possible fields. You can provide this data as
        a :model:`.PatchTenantData` or as a dictionary.
    :param tenant_id: The id of the tenant you want to update.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The updated tenant.
    """
    url = "/api/v1/tenants/{tenantId}".format(tenantId=tenant_id)
    params = extra_parameters or {}

    response = client.http.patch(
        url=url, json=to_dict(json_body), params=params
    )
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(ParserFor.make(ExtendedTenant)).try_parse(
            response
        )
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
