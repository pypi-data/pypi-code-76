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
from .AmountDto import AmountDto
from .EntityTypeDto import EntityTypeDto
from .KeyDto import KeyDto
from .MosaicGlobalRestrictionTransactionBodyBuilder import MosaicGlobalRestrictionTransactionBodyBuilder
from .MosaicRestrictionTypeDto import MosaicRestrictionTypeDto
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto

class MosaicGlobalRestrictionTransactionBuilder(TransactionBuilder):
    """Binary layout for a non-embedded mosaic global restriction transaction.

    Attributes:
        mosaicGlobalRestrictionTransactionBody: Mosaic global restriction transaction body.
    """

    def __init__(self, signature: SignatureDto, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type: EntityTypeDto, fee: AmountDto, deadline: TimestampDto, mosaicId: UnresolvedMosaicIdDto, referenceMosaicId: UnresolvedMosaicIdDto, restrictionKey: int, previousRestrictionValue: int, newRestrictionValue: int, previousRestrictionType: MosaicRestrictionTypeDto, newRestrictionType: MosaicRestrictionTypeDto):
        """Constructor.
        Args:
            signature: Entity signature.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
            fee: Transaction fee.
            deadline: Transaction deadline.
            mosaicId: Identifier of the mosaic being restricted.
            referenceMosaicId: Identifier of the mosaic providing the restriction key.
            restrictionKey: Restriction key relative to the reference mosaic identifier.
            previousRestrictionValue: Previous restriction value.
            newRestrictionValue: New restriction value.
            previousRestrictionType: Previous restriction type.
            newRestrictionType: New restriction type.
        """
        super().__init__(signature, signerPublicKey, version, network, type, fee, deadline)
        self.mosaicGlobalRestrictionTransactionBody = MosaicGlobalRestrictionTransactionBodyBuilder(mosaicId, referenceMosaicId, restrictionKey, previousRestrictionValue, newRestrictionValue, previousRestrictionType, newRestrictionType)


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicGlobalRestrictionTransactionBuilder:
        """Creates an instance of MosaicGlobalRestrictionTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicGlobalRestrictionTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        mosaicGlobalRestrictionTransactionBody = MosaicGlobalRestrictionTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[mosaicGlobalRestrictionTransactionBody.getSize():]
        return MosaicGlobalRestrictionTransactionBuilder(superObject.signature, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type, superObject.fee, superObject.deadline, mosaicGlobalRestrictionTransactionBody.mosaicId, mosaicGlobalRestrictionTransactionBody.referenceMosaicId, mosaicGlobalRestrictionTransactionBody.restrictionKey, mosaicGlobalRestrictionTransactionBody.previousRestrictionValue, mosaicGlobalRestrictionTransactionBody.newRestrictionValue, mosaicGlobalRestrictionTransactionBody.previousRestrictionType, mosaicGlobalRestrictionTransactionBody.newRestrictionType)

    def getMosaicId(self) -> UnresolvedMosaicIdDto:
        """Gets identifier of the mosaic being restricted.
        Returns:
            Identifier of the mosaic being restricted.
        """
        return self.mosaicGlobalRestrictionTransactionBody.getMosaicId()

    def getReferenceMosaicId(self) -> UnresolvedMosaicIdDto:
        """Gets identifier of the mosaic providing the restriction key.
        Returns:
            Identifier of the mosaic providing the restriction key.
        """
        return self.mosaicGlobalRestrictionTransactionBody.getReferenceMosaicId()

    def getRestrictionKey(self) -> int:
        """Gets restriction key relative to the reference mosaic identifier.
        Returns:
            Restriction key relative to the reference mosaic identifier.
        """
        return self.mosaicGlobalRestrictionTransactionBody.getRestrictionKey()

    def getPreviousRestrictionValue(self) -> int:
        """Gets previous restriction value.
        Returns:
            Previous restriction value.
        """
        return self.mosaicGlobalRestrictionTransactionBody.getPreviousRestrictionValue()

    def getNewRestrictionValue(self) -> int:
        """Gets new restriction value.
        Returns:
            New restriction value.
        """
        return self.mosaicGlobalRestrictionTransactionBody.getNewRestrictionValue()

    def getPreviousRestrictionType(self) -> MosaicRestrictionTypeDto:
        """Gets previous restriction type.
        Returns:
            Previous restriction type.
        """
        return self.mosaicGlobalRestrictionTransactionBody.getPreviousRestrictionType()

    def getNewRestrictionType(self) -> MosaicRestrictionTypeDto:
        """Gets new restriction type.
        Returns:
            New restriction type.
        """
        return self.mosaicGlobalRestrictionTransactionBody.getNewRestrictionType()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.mosaicGlobalRestrictionTransactionBody.getSize()
        return size

    def getBody(self) -> MosaicGlobalRestrictionTransactionBodyBuilder:
        """Gets the body builder of the object.
        Returns:
            Body builder.
        """
        return self.mosaicGlobalRestrictionTransactionBody

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.mosaicGlobalRestrictionTransactionBody.serialize())  # kind:CUSTOM
        return bytes_
