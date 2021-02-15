"""The module that defines the ``NonFinalizedLTI1p3Provider`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Mapping, Optional, Type

import cg_request_args as rqa
from typing_extensions import Literal

from ..utils import to_dict
from .base_lti1p3_provider import BaseLTI1p3Provider


@dataclass
class NonFinalizedLTI1p3Provider(BaseLTI1p3Provider):
    """A non finalized LTI 1.3 provider as JSON."""

    #: This is a non finalized provider.
    finalized: "Literal[False]"
    #: The auth login url, if already configured.
    auth_login_url: "Optional[str]"
    #: The auth token url, if already configured.
    auth_token_url: "Optional[str]"
    #: The client id, if already configured.
    client_id: "Optional[str]"
    #: The url where we can download the keyset of the LMS, if already
    #: configured.
    key_set_url: "Optional[str]"
    #: The auth audience, if already configured.
    auth_audience: "Optional[str]"
    #: Custom fields that the LMS should provide when launching.
    custom_fields: "Mapping[str, str]"
    #: The public JWK for this provider, this should be provided to the LMS.
    public_jwk: "Mapping[str, str]"
    #: The public key for this provider, this should be provided to the LMS.
    public_key: "str"
    #: If you have the permission to edit this provider this will be a key with
    #: which you can do that.
    edit_secret: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: BaseLTI1p3Provider.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "finalized",
                    rqa.LiteralBoolean(False),
                    doc="This is a non finalized provider.",
                ),
                rqa.RequiredArgument(
                    "auth_login_url",
                    rqa.Nullable(rqa.SimpleValue.str),
                    doc="The auth login url, if already configured.",
                ),
                rqa.RequiredArgument(
                    "auth_token_url",
                    rqa.Nullable(rqa.SimpleValue.str),
                    doc="The auth token url, if already configured.",
                ),
                rqa.RequiredArgument(
                    "client_id",
                    rqa.Nullable(rqa.SimpleValue.str),
                    doc="The client id, if already configured.",
                ),
                rqa.RequiredArgument(
                    "key_set_url",
                    rqa.Nullable(rqa.SimpleValue.str),
                    doc=(
                        "The url where we can download the keyset of the LMS,"
                        " if already configured."
                    ),
                ),
                rqa.RequiredArgument(
                    "auth_audience",
                    rqa.Nullable(rqa.SimpleValue.str),
                    doc="The auth audience, if already configured.",
                ),
                rqa.RequiredArgument(
                    "custom_fields",
                    rqa.LookupMapping(rqa.SimpleValue.str),
                    doc=(
                        "Custom fields that the LMS should provide when"
                        " launching."
                    ),
                ),
                rqa.RequiredArgument(
                    "public_jwk",
                    rqa.LookupMapping(rqa.SimpleValue.str),
                    doc=(
                        "The public JWK for this provider, this should be"
                        " provided to the LMS."
                    ),
                ),
                rqa.RequiredArgument(
                    "public_key",
                    rqa.SimpleValue.str,
                    doc=(
                        "The public key for this provider, this should be"
                        " provided to the LMS."
                    ),
                ),
                rqa.RequiredArgument(
                    "edit_secret",
                    rqa.Nullable(rqa.SimpleValue.str),
                    doc=(
                        "If you have the permission to edit this provider this"
                        " will be a key with which you can do that."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["finalized"] = to_dict(self.finalized)
        res["auth_login_url"] = to_dict(self.auth_login_url)
        res["auth_token_url"] = to_dict(self.auth_token_url)
        res["client_id"] = to_dict(self.client_id)
        res["key_set_url"] = to_dict(self.key_set_url)
        res["auth_audience"] = to_dict(self.auth_audience)
        res["custom_fields"] = to_dict(self.custom_fields)
        res["public_jwk"] = to_dict(self.public_jwk)
        res["public_key"] = to_dict(self.public_key)
        res["edit_secret"] = to_dict(self.edit_secret)
        res["capabilities"] = to_dict(self.capabilities)
        res["version"] = to_dict(self.version)
        res["iss"] = to_dict(self.iss)
        res["id"] = to_dict(self.id)
        res["lms"] = to_dict(self.lms)
        res["created_at"] = to_dict(self.created_at)
        res["intended_use"] = to_dict(self.intended_use)
        res["tenant_id"] = to_dict(self.tenant_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["NonFinalizedLTI1p3Provider"], d: Dict[str, Any]
    ) -> "NonFinalizedLTI1p3Provider":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            finalized=parsed.finalized,
            auth_login_url=parsed.auth_login_url,
            auth_token_url=parsed.auth_token_url,
            client_id=parsed.client_id,
            key_set_url=parsed.key_set_url,
            auth_audience=parsed.auth_audience,
            custom_fields=parsed.custom_fields,
            public_jwk=parsed.public_jwk,
            public_key=parsed.public_key,
            edit_secret=parsed.edit_secret,
            capabilities=parsed.capabilities,
            version=parsed.version,
            iss=parsed.iss,
            id=parsed.id,
            lms=parsed.lms,
            created_at=parsed.created_at,
            intended_use=parsed.intended_use,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res
