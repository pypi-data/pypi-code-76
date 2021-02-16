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
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .Hash256Dto import Hash256Dto
from .HashLockTransactionBodyBuilder import HashLockTransactionBodyBuilder
from .KeyDto import KeyDto
from .NetworkTypeDto import NetworkTypeDto
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder

class EmbeddedHashLockTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded hash lock transaction.

    Attributes:
        hashLockTransactionBody: Hash lock transaction body.
    """

    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type: EntityTypeDto, mosaic: UnresolvedMosaicBuilder, duration: BlockDurationDto, hash: Hash256Dto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
            mosaic: Lock mosaic.
            duration: Number of blocks for which a lock should be valid.
            hash: Lock hash.
        """
        super().__init__(signerPublicKey, version, network, type)
        self.hashLockTransactionBody = HashLockTransactionBodyBuilder(mosaic, duration, hash)


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedHashLockTransactionBuilder:
        """Creates an instance of EmbeddedHashLockTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedHashLockTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        hashLockTransactionBody = HashLockTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[hashLockTransactionBody.getSize():]
        return EmbeddedHashLockTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type, hashLockTransactionBody.mosaic, hashLockTransactionBody.duration, hashLockTransactionBody.hash)

    def getMosaic(self) -> UnresolvedMosaicBuilder:
        """Gets lock mosaic.
        Returns:
            Lock mosaic.
        """
        return self.hashLockTransactionBody.getMosaic()

    def getDuration(self) -> BlockDurationDto:
        """Gets number of blocks for which a lock should be valid.
        Returns:
            Number of blocks for which a lock should be valid.
        """
        return self.hashLockTransactionBody.getDuration()

    def getHash(self) -> Hash256Dto:
        """Gets lock hash.
        Returns:
            Lock hash.
        """
        return self.hashLockTransactionBody.getHash()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.hashLockTransactionBody.getSize()
        return size

    def getBody(self) -> HashLockTransactionBodyBuilder:
        """Gets the body builder of the object.
        Returns:
            Body builder.
        """
        return self.hashLockTransactionBody

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.hashLockTransactionBody.serialize())  # kind:CUSTOM
        return bytes_
