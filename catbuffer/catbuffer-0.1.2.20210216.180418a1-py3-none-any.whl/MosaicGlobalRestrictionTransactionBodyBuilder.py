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
from .MosaicRestrictionTypeDto import MosaicRestrictionTypeDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto

class MosaicGlobalRestrictionTransactionBodyBuilder:
    """Binary layout for a mosaic global restriction transaction.

    Attributes:
        mosaicId: Identifier of the mosaic being restricted.
        referenceMosaicId: Identifier of the mosaic providing the restriction key.
        restrictionKey: Restriction key relative to the reference mosaic identifier.
        previousRestrictionValue: Previous restriction value.
        newRestrictionValue: New restriction value.
        previousRestrictionType: Previous restriction type.
        newRestrictionType: New restriction type.
    """

    def __init__(self, mosaicId: UnresolvedMosaicIdDto, referenceMosaicId: UnresolvedMosaicIdDto, restrictionKey: int, previousRestrictionValue: int, newRestrictionValue: int, previousRestrictionType: MosaicRestrictionTypeDto, newRestrictionType: MosaicRestrictionTypeDto):
        """Constructor.
        Args:
            mosaicId: Identifier of the mosaic being restricted.
            referenceMosaicId: Identifier of the mosaic providing the restriction key.
            restrictionKey: Restriction key relative to the reference mosaic identifier.
            previousRestrictionValue: Previous restriction value.
            newRestrictionValue: New restriction value.
            previousRestrictionType: Previous restriction type.
            newRestrictionType: New restriction type.
        """
        self.mosaicId = mosaicId
        self.referenceMosaicId = referenceMosaicId
        self.restrictionKey = restrictionKey
        self.previousRestrictionValue = previousRestrictionValue
        self.newRestrictionValue = newRestrictionValue
        self.previousRestrictionType = previousRestrictionType
        self.newRestrictionType = newRestrictionType


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicGlobalRestrictionTransactionBodyBuilder:
        """Creates an instance of MosaicGlobalRestrictionTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicGlobalRestrictionTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        mosaicId = UnresolvedMosaicIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[mosaicId.getSize():]
        referenceMosaicId = UnresolvedMosaicIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[referenceMosaicId.getSize():]
        restrictionKey = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        previousRestrictionValue = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        newRestrictionValue = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        previousRestrictionType = MosaicRestrictionTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[previousRestrictionType.getSize():]
        newRestrictionType = MosaicRestrictionTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[newRestrictionType.getSize():]
        return MosaicGlobalRestrictionTransactionBodyBuilder(mosaicId, referenceMosaicId, restrictionKey, previousRestrictionValue, newRestrictionValue, previousRestrictionType, newRestrictionType)

    def getMosaicId(self) -> UnresolvedMosaicIdDto:
        """Gets identifier of the mosaic being restricted.
        Returns:
            Identifier of the mosaic being restricted.
        """
        return self.mosaicId

    def getReferenceMosaicId(self) -> UnresolvedMosaicIdDto:
        """Gets identifier of the mosaic providing the restriction key.
        Returns:
            Identifier of the mosaic providing the restriction key.
        """
        return self.referenceMosaicId

    def getRestrictionKey(self) -> int:
        """Gets restriction key relative to the reference mosaic identifier.
        Returns:
            Restriction key relative to the reference mosaic identifier.
        """
        return self.restrictionKey

    def getPreviousRestrictionValue(self) -> int:
        """Gets previous restriction value.
        Returns:
            Previous restriction value.
        """
        return self.previousRestrictionValue

    def getNewRestrictionValue(self) -> int:
        """Gets new restriction value.
        Returns:
            New restriction value.
        """
        return self.newRestrictionValue

    def getPreviousRestrictionType(self) -> MosaicRestrictionTypeDto:
        """Gets previous restriction type.
        Returns:
            Previous restriction type.
        """
        return self.previousRestrictionType

    def getNewRestrictionType(self) -> MosaicRestrictionTypeDto:
        """Gets new restriction type.
        Returns:
            New restriction type.
        """
        return self.newRestrictionType

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.mosaicId.getSize()
        size += self.referenceMosaicId.getSize()
        size += 8  # restrictionKey
        size += 8  # previousRestrictionValue
        size += 8  # newRestrictionValue
        size += self.previousRestrictionType.getSize()
        size += self.newRestrictionType.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.mosaicId.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.referenceMosaicId.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getRestrictionKey(), 8))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getPreviousRestrictionValue(), 8))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getNewRestrictionValue(), 8))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.previousRestrictionType.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.newRestrictionType.serialize())  # kind:CUSTOM
        return bytes_
