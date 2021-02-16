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
from .AccountRestrictionFlagsDto import AccountRestrictionFlagsDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto

class AccountMosaicRestrictionTransactionBodyBuilder:
    """Binary layout for an account mosaic restriction transaction.

    Attributes:
        restrictionFlags: Account restriction flags.
        restrictionAdditions: Account restriction additions.
        restrictionDeletions: Account restriction deletions.
    """

    def __init__(self, restrictionFlags: List[AccountRestrictionFlagsDto], restrictionAdditions: List[UnresolvedMosaicIdDto], restrictionDeletions: List[UnresolvedMosaicIdDto]):
        """Constructor.
        Args:
            restrictionFlags: Account restriction flags.
            restrictionAdditions: Account restriction additions.
            restrictionDeletions: Account restriction deletions.
        """
        self.restrictionFlags = restrictionFlags
        self.restrictionAdditions = restrictionAdditions
        self.restrictionDeletions = restrictionDeletions


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountMosaicRestrictionTransactionBodyBuilder:
        """Creates an instance of AccountMosaicRestrictionTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountMosaicRestrictionTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        restrictionFlags = AccountRestrictionFlagsDto.bytesToFlags(bytes_, 2)  # kind:FLAGS
        bytes_ = bytes_[2:]
        restrictionAdditionsCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        restrictionDeletionsCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        accountRestrictionTransactionBody_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        restrictionAdditions: List[UnresolvedMosaicIdDto] = []  # kind:ARRAY
        for _ in range(restrictionAdditionsCount):
            item = UnresolvedMosaicIdDto.loadFromBinary(bytes_)
            restrictionAdditions.append(item)
            bytes_ = bytes_[item.getSize():]
        restrictionDeletions: List[UnresolvedMosaicIdDto] = []  # kind:ARRAY
        for _ in range(restrictionDeletionsCount):
            item = UnresolvedMosaicIdDto.loadFromBinary(bytes_)
            restrictionDeletions.append(item)
            bytes_ = bytes_[item.getSize():]
        return AccountMosaicRestrictionTransactionBodyBuilder(restrictionFlags, restrictionAdditions, restrictionDeletions)

    def getRestrictionFlags(self) -> List[AccountRestrictionFlagsDto]:
        """Gets account restriction flags.
        Returns:
            Account restriction flags.
        """
        return self.restrictionFlags

    def getRestrictionAdditions(self) -> List[UnresolvedMosaicIdDto]:
        """Gets account restriction additions.
        Returns:
            Account restriction additions.
        """
        return self.restrictionAdditions

    def getRestrictionDeletions(self) -> List[UnresolvedMosaicIdDto]:
        """Gets account restriction deletions.
        Returns:
            Account restriction deletions.
        """
        return self.restrictionDeletions

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 2  # restrictionFlags
        size += 1  # restrictionAdditionsCount
        size += 1  # restrictionDeletionsCount
        size += 4  # accountRestrictionTransactionBody_Reserved1
        for _ in self.restrictionAdditions:
            size += _.getSize()
        for _ in self.restrictionDeletions:
            size += _.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(AccountRestrictionFlagsDto.flagsToInt(self.getRestrictionFlags()), 2))  # kind:FLAGS
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getRestrictionAdditions()), 1))  # kind:SIZE_FIELD
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getRestrictionDeletions()), 1))  # kind:SIZE_FIELD
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(0, 4))
        for _ in self.restrictionAdditions: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())
        for _ in self.restrictionDeletions: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())
        return bytes_
