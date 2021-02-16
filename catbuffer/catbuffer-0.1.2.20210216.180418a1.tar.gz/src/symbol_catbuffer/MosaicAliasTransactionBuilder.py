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
from .AmountDto import AmountDto
from .EntityTypeDto import EntityTypeDto
from .KeyDto import KeyDto
from .MosaicAliasTransactionBodyBuilder import MosaicAliasTransactionBodyBuilder
from .MosaicIdDto import MosaicIdDto
from .NamespaceIdDto import NamespaceIdDto
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder

class MosaicAliasTransactionBuilder(TransactionBuilder):
    """Binary layout for a non-embedded mosaic alias transaction.

    Attributes:
        mosaicAliasTransactionBody: Mosaic alias transaction body.
    """

    def __init__(self, signature: SignatureDto, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type: EntityTypeDto, fee: AmountDto, deadline: TimestampDto, namespaceId: NamespaceIdDto, mosaicId: MosaicIdDto, aliasAction: AliasActionDto):
        """Constructor.
        Args:
            signature: Entity signature.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
            fee: Transaction fee.
            deadline: Transaction deadline.
            namespaceId: Identifier of the namespace that will become an alias.
            mosaicId: Aliased mosaic identifier.
            aliasAction: Alias action.
        """
        super().__init__(signature, signerPublicKey, version, network, type, fee, deadline)
        self.mosaicAliasTransactionBody = MosaicAliasTransactionBodyBuilder(namespaceId, mosaicId, aliasAction)


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicAliasTransactionBuilder:
        """Creates an instance of MosaicAliasTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicAliasTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        mosaicAliasTransactionBody = MosaicAliasTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[mosaicAliasTransactionBody.getSize():]
        return MosaicAliasTransactionBuilder(superObject.signature, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type, superObject.fee, superObject.deadline, mosaicAliasTransactionBody.namespaceId, mosaicAliasTransactionBody.mosaicId, mosaicAliasTransactionBody.aliasAction)

    def getNamespaceId(self) -> NamespaceIdDto:
        """Gets identifier of the namespace that will become an alias.
        Returns:
            Identifier of the namespace that will become an alias.
        """
        return self.mosaicAliasTransactionBody.getNamespaceId()

    def getMosaicId(self) -> MosaicIdDto:
        """Gets aliased mosaic identifier.
        Returns:
            Aliased mosaic identifier.
        """
        return self.mosaicAliasTransactionBody.getMosaicId()

    def getAliasAction(self) -> AliasActionDto:
        """Gets alias action.
        Returns:
            Alias action.
        """
        return self.mosaicAliasTransactionBody.getAliasAction()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.mosaicAliasTransactionBody.getSize()
        return size

    def getBody(self) -> MosaicAliasTransactionBodyBuilder:
        """Gets the body builder of the object.
        Returns:
            Body builder.
        """
        return self.mosaicAliasTransactionBody

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.mosaicAliasTransactionBody.serialize())  # kind:CUSTOM
        return bytes_
