"""The endpoints for tenant objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Dict, Sequence

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.base_error import BaseError
    from ..models.create_tenant_data import CreateTenantData
    from ..models.extended_tenant import ExtendedTenant
    from ..models.patch_tenant_data import PatchTenantData
    from ..models.tenant_statistics import TenantStatistics
    from ..parsers import JsonResponseParser, ParserFor, ResponsePropertyParser
    from ..utils import to_multipart

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class TenantService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get_all(
        self,
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[ExtendedTenant]":
        """Get all tenants of an instance.

        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: All the tenants of this instance.
        """
        from typing import Sequence

        from ..models.base_error import BaseError
        from ..models.extended_tenant import ExtendedTenant
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/tenants/"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(ExtendedTenant))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def create(
        self: "TenantService[AuthenticatedClient]",
        multipart_data: Union[dict, list, "CreateTenantData"],
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ExtendedTenant":
        """Create a new tenant.

        :param multipart_data: The data that should form the body of the
            request. See :model:`.CreateTenantData` for information about the
            possible fields.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The newly created tenant.
        """
        from ..models.base_error import BaseError
        from ..models.create_tenant_data import CreateTenantData
        from ..models.extended_tenant import ExtendedTenant
        from ..parsers import JsonResponseParser, ParserFor
        from ..utils import to_multipart

        url = "/api/v1/tenants/"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(
                url=url,
                files=to_multipart(to_dict(multipart_data)),
                params=params,
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ExtendedTenant)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_stats(
        self: "TenantService[AuthenticatedClient]",
        *,
        tenant_id: "str",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "TenantStatistics":
        """Get the statistics of a tenant.

        :param tenant_id: The id of the tenant for which you want to get the
            statistics.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The statistics of the specified tenant.
        """
        from ..models.base_error import BaseError
        from ..models.tenant_statistics import TenantStatistics
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/tenants/{tenantId}/statistics/".format(
            tenantId=tenant_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(TenantStatistics)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_logo(
        self,
        *,
        tenant_id: "str",
        dark: "bool" = False,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "bytes":
        """Get the logo of a tenant.

        :param tenant_id: The id of the tenant for which you want to get the
            logo.
        :param dark: If truhty the retrieved logo will be suited for the dark
            theme.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The logo of the tenant.
        """
        from typing import Dict

        from ..models.base_error import BaseError
        from ..parsers import (
            JsonResponseParser,
            ParserFor,
            ResponsePropertyParser,
        )

        url = "/api/v1/tenants/{tenantId}/logo".format(tenantId=tenant_id)
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "dark": to_dict(dark),
        }

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return ResponsePropertyParser("content", bytes).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get(
        self,
        *,
        tenant_id: "str",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ExtendedTenant":
        """Get a tenant by id.

        :param tenant_id: The id of the tenant you want to retrieve.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The tenant with the given id.
        """
        from ..models.base_error import BaseError
        from ..models.extended_tenant import ExtendedTenant
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/tenants/{tenantId}".format(tenantId=tenant_id)
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ExtendedTenant)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def patch(
        self: "TenantService[AuthenticatedClient]",
        json_body: Union[dict, list, "PatchTenantData"],
        *,
        tenant_id: "str",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ExtendedTenant":
        """Update a tenant by id.

        :param json_body: The body of the request. See
            :model:`.PatchTenantData` for information about the possible
            fields. You can provide this data as a :model:`.PatchTenantData` or
            as a dictionary.
        :param tenant_id: The id of the tenant you want to update.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated tenant.
        """
        from ..models.base_error import BaseError
        from ..models.extended_tenant import ExtendedTenant
        from ..models.patch_tenant_data import PatchTenantData
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/tenants/{tenantId}".format(tenantId=tenant_id)
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ExtendedTenant)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
