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
from typing import List
from .GeneratorUtils import GeneratorUtils
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .KeyDto import KeyDto
from .NetworkTypeDto import NetworkTypeDto
from .TransferTransactionBodyBuilder import TransferTransactionBodyBuilder
from .UnresolvedAddressDto import UnresolvedAddressDto
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder

class EmbeddedTransferTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded transfer transaction.

    Attributes:
        transferTransactionBody: Transfer transaction body.
    """

    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type: EntityTypeDto, recipientAddress: UnresolvedAddressDto, mosaics: List[UnresolvedMosaicBuilder], message: bytes):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
            recipientAddress: Recipient address.
            mosaics: Attached mosaics.
            message: Attached message.
        """
        super().__init__(signerPublicKey, version, network, type)
        self.transferTransactionBody = TransferTransactionBodyBuilder(recipientAddress, mosaics, message)


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedTransferTransactionBuilder:
        """Creates an instance of EmbeddedTransferTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedTransferTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        transferTransactionBody = TransferTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[transferTransactionBody.getSize():]
        return EmbeddedTransferTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type, transferTransactionBody.recipientAddress, transferTransactionBody.mosaics, transferTransactionBody.message)

    def getRecipientAddress(self) -> UnresolvedAddressDto:
        """Gets recipient address.
        Returns:
            Recipient address.
        """
        return self.transferTransactionBody.getRecipientAddress()

    def getMosaics(self) -> List[UnresolvedMosaicBuilder]:
        """Gets attached mosaics.
        Returns:
            Attached mosaics.
        """
        return self.transferTransactionBody.getMosaics()

    def getMessage(self) -> bytes:
        """Gets attached message.
        Returns:
            Attached message.
        """
        return self.transferTransactionBody.getMessage()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.transferTransactionBody.getSize()
        return size

    def getBody(self) -> TransferTransactionBodyBuilder:
        """Gets the body builder of the object.
        Returns:
            Body builder.
        """
        return self.transferTransactionBody

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.transferTransactionBody.serialize())  # kind:CUSTOM
        return bytes_
