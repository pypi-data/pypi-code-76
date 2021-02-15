"""Responses."""

from __future__ import annotations

import zlib
from typing import List, Optional, Type, TypeVar

from pydantic import Field

from kelvin.icd import Message
from kelvin.icd.model import CoreHeader, CoreModel

S = TypeVar("S", bound="Response", covariant=True)


class Header(CoreHeader):
    """Header Interface."""

    type: Optional[str] = Field(None, title="Request type.", description="Request type.")
    hash: Optional[str] = Field(None, title="Request Hash", description="Request hash.")


class Response(CoreModel[Header]):
    """Server response."""

    messages: List[Message]

    @classmethod
    def decode(cls: Type[S], data: bytes, compress: bool = False) -> S:
        """Decode model."""

        if compress:
            try:
                data = zlib.decompress(data)
            except zlib.error as e:
                raise ValueError(f"Unable to decompress data: {e}")

        return super().decode(data)

    def encode(self, compress: bool = False) -> bytes:
        """Encode model."""

        data = super().encode()

        if compress:
            data = zlib.compress(data)

        return data
