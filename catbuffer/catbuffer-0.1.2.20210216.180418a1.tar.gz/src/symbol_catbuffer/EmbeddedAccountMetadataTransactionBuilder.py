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
from .AccountMetadataTransactionBodyBuilder import AccountMetadataTransactionBodyBuilder
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .KeyDto import KeyDto
from .NetworkTypeDto import NetworkTypeDto
from .UnresolvedAddressDto import UnresolvedAddressDto

class EmbeddedAccountMetadataTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded account metadata transaction.

    Attributes:
        accountMetadataTransactionBody: Account metadata transaction body.
    """

    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type: EntityTypeDto, targetAddress: UnresolvedAddressDto, scopedMetadataKey: int, valueSizeDelta: int, value: bytes):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
            targetAddress: Metadata target address.
            scopedMetadataKey: Metadata key scoped to source, target and type.
            valueSizeDelta: Change in value size in bytes.
            value: Difference between existing value and new value \note when there is no existing value, new value is same this value \note when there is an existing value, new value is calculated as xor(previous-value, value).
        """
        super().__init__(signerPublicKey, version, network, type)
        self.accountMetadataTransactionBody = AccountMetadataTransactionBodyBuilder(targetAddress, scopedMetadataKey, valueSizeDelta, value)


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedAccountMetadataTransactionBuilder:
        """Creates an instance of EmbeddedAccountMetadataTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedAccountMetadataTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        accountMetadataTransactionBody = AccountMetadataTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[accountMetadataTransactionBody.getSize():]
        return EmbeddedAccountMetadataTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type, accountMetadataTransactionBody.targetAddress, accountMetadataTransactionBody.scopedMetadataKey, accountMetadataTransactionBody.valueSizeDelta, accountMetadataTransactionBody.value)

    def getTargetAddress(self) -> UnresolvedAddressDto:
        """Gets metadata target address.
        Returns:
            Metadata target address.
        """
        return self.accountMetadataTransactionBody.getTargetAddress()

    def getScopedMetadataKey(self) -> int:
        """Gets metadata key scoped to source, target and type.
        Returns:
            Metadata key scoped to source, target and type.
        """
        return self.accountMetadataTransactionBody.getScopedMetadataKey()

    def getValueSizeDelta(self) -> int:
        """Gets change in value size in bytes.
        Returns:
            Change in value size in bytes.
        """
        return self.accountMetadataTransactionBody.getValueSizeDelta()

    def getValue(self) -> bytes:
        """Gets difference between existing value and new value \note when there is no existing value, new value is same this value \note when there is an existing value, new value is calculated as xor(previous-value, value).
        Returns:
            Difference between existing value and new value \note when there is no existing value, new value is same this value \note when there is an existing value, new value is calculated as xor(previous-value, value).
        """
        return self.accountMetadataTransactionBody.getValue()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.accountMetadataTransactionBody.getSize()
        return size

    def getBody(self) -> AccountMetadataTransactionBodyBuilder:
        """Gets the body builder of the object.
        Returns:
            Body builder.
        """
        return self.accountMetadataTransactionBody

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.accountMetadataTransactionBody.serialize())  # kind:CUSTOM
        return bytes_
