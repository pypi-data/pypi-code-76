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
from .BlockDurationDto import BlockDurationDto
from .Hash256Dto import Hash256Dto
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder

class HashLockTransactionBodyBuilder:
    """Binary layout for a hash lock transaction.

    Attributes:
        mosaic: Lock mosaic.
        duration: Number of blocks for which a lock should be valid.
        hash: Lock hash.
    """

    def __init__(self, mosaic: UnresolvedMosaicBuilder, duration: BlockDurationDto, hash: Hash256Dto):
        """Constructor.
        Args:
            mosaic: Lock mosaic.
            duration: Number of blocks for which a lock should be valid.
            hash: Lock hash.
        """
        self.mosaic = mosaic
        self.duration = duration
        self.hash = hash


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> HashLockTransactionBodyBuilder:
        """Creates an instance of HashLockTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of HashLockTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        mosaic = UnresolvedMosaicBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[mosaic.getSize():]
        duration = BlockDurationDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[duration.getSize():]
        hash = Hash256Dto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[hash.getSize():]
        return HashLockTransactionBodyBuilder(mosaic, duration, hash)

    def getMosaic(self) -> UnresolvedMosaicBuilder:
        """Gets lock mosaic.
        Returns:
            Lock mosaic.
        """
        return self.mosaic

    def getDuration(self) -> BlockDurationDto:
        """Gets number of blocks for which a lock should be valid.
        Returns:
            Number of blocks for which a lock should be valid.
        """
        return self.duration

    def getHash(self) -> Hash256Dto:
        """Gets lock hash.
        Returns:
            Lock hash.
        """
        return self.hash

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.mosaic.getSize()
        size += self.duration.getSize()
        size += self.hash.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.mosaic.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.duration.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.hash.serialize())  # kind:CUSTOM
        return bytes_
