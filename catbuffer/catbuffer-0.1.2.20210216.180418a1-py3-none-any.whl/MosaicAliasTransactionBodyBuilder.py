#!/usr/bin/python
"""
    Copyright (c) 2016-2019, Jaguar0625, gimre, BloodyRookie, Tech Bureau, Corp.
    Copyright (c) 2020-present, Jaguar0625, gimre, BloodyRookie.

    This file is part of Catapult.

    Catapult is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Catapult is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Catapult. If not, see <http://www.gnu.org/licenses/>.
"""

# pylint: disable=W0622,W0612,C0301,R0904

from __future__ import annotations
from .GeneratorUtils import GeneratorUtils
from .AliasActionDto import AliasActionDto
from .MosaicIdDto import MosaicIdDto
from .NamespaceIdDto import NamespaceIdDto

class MosaicAliasTransactionBodyBuilder:
    """Binary layout for an mosaic alias transaction.

    Attributes:
        namespaceId: Identifier of the namespace that will become an alias.
        mosaicId: Aliased mosaic identifier.
        aliasAction: Alias action.
    """

    def __init__(self, namespaceId: NamespaceIdDto, mosaicId: MosaicIdDto, aliasAction: AliasActionDto):
        """Constructor.
        Args:
            namespaceId: Identifier of the namespace that will become an alias.
            mosaicId: Aliased mosaic identifier.
            aliasAction: Alias action.
        """
        self.namespaceId = namespaceId
        self.mosaicId = mosaicId
        self.aliasAction = aliasAction


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicAliasTransactionBodyBuilder:
        """Creates an instance of MosaicAliasTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicAliasTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        namespaceId = NamespaceIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[namespaceId.getSize():]
        mosaicId = MosaicIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[mosaicId.getSize():]
        aliasAction = AliasActionDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[aliasAction.getSize():]
        return MosaicAliasTransactionBodyBuilder(namespaceId, mosaicId, aliasAction)

    def getNamespaceId(self) -> NamespaceIdDto:
        """Gets identifier of the namespace that will become an alias.
        Returns:
            Identifier of the namespace that will become an alias.
        """
        return self.namespaceId

    def getMosaicId(self) -> MosaicIdDto:
        """Gets aliased mosaic identifier.
        Returns:
            Aliased mosaic identifier.
        """
        return self.mosaicId

    def getAliasAction(self) -> AliasActionDto:
        """Gets alias action.
        Returns:
            Alias action.
        """
        return self.aliasAction

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.namespaceId.getSize()
        size += self.mosaicId.getSize()
        size += self.aliasAction.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.namespaceId.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.mosaicId.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.aliasAction.serialize())  # kind:CUSTOM
        return bytes_
