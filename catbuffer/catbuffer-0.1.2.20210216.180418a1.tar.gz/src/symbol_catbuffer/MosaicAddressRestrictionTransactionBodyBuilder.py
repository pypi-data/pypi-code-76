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
from .UnresolvedAddressDto import UnresolvedAddressDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto

class MosaicAddressRestrictionTransactionBodyBuilder:
    """Binary layout for a mosaic address restriction transaction.

    Attributes:
        mosaicId: Identifier of the mosaic to which the restriction applies.
        restrictionKey: Restriction key.
        previousRestrictionValue: Previous restriction value.
        newRestrictionValue: New restriction value.
        targetAddress: Address being restricted.
    """

    def __init__(self, mosaicId: UnresolvedMosaicIdDto, restrictionKey: int, previousRestrictionValue: int, newRestrictionValue: int, targetAddress: UnresolvedAddressDto):
        """Constructor.
        Args:
            mosaicId: Identifier of the mosaic to which the restriction applies.
            restrictionKey: Restriction key.
            previousRestrictionValue: Previous restriction value.
            newRestrictionValue: New restriction value.
            targetAddress: Address being restricted.
        """
        self.mosaicId = mosaicId
        self.restrictionKey = restrictionKey
        self.previousRestrictionValue = previousRestrictionValue
        self.newRestrictionValue = newRestrictionValue
        self.targetAddress = targetAddress


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicAddressRestrictionTransactionBodyBuilder:
        """Creates an instance of MosaicAddressRestrictionTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicAddressRestrictionTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        mosaicId = UnresolvedMosaicIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[mosaicId.getSize():]
        restrictionKey = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        previousRestrictionValue = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        newRestrictionValue = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        targetAddress = UnresolvedAddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[targetAddress.getSize():]
        return MosaicAddressRestrictionTransactionBodyBuilder(mosaicId, restrictionKey, previousRestrictionValue, newRestrictionValue, targetAddress)

    def getMosaicId(self) -> UnresolvedMosaicIdDto:
        """Gets identifier of the mosaic to which the restriction applies.
        Returns:
            Identifier of the mosaic to which the restriction applies.
        """
        return self.mosaicId

    def getRestrictionKey(self) -> int:
        """Gets restriction key.
        Returns:
            Restriction key.
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

    def getTargetAddress(self) -> UnresolvedAddressDto:
        """Gets address being restricted.
        Returns:
            Address being restricted.
        """
        return self.targetAddress

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.mosaicId.getSize()
        size += 8  # restrictionKey
        size += 8  # previousRestrictionValue
        size += 8  # newRestrictionValue
        size += self.targetAddress.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.mosaicId.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getRestrictionKey(), 8))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getPreviousRestrictionValue(), 8))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getNewRestrictionValue(), 8))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.targetAddress.serialize())  # kind:CUSTOM
        return bytes_
