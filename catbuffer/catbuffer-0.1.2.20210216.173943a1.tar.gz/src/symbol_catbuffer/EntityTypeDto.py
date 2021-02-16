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
from enum import Enum
from .GeneratorUtils import GeneratorUtils


class EntityTypeDto(Enum):
    """Enumeration of entity types

    Attributes:
        RESERVED: reserved entity type.
        NEMESIS_BLOCK_HEADER: Nemesis block header.
        NORMAL_BLOCK_HEADER: Normal block header.
        IMPORTANCE_BLOCK_HEADER: Importance block header.
        ACCOUNT_KEY_LINK_TRANSACTION: Account key link transaction.
        NODE_KEY_LINK_TRANSACTION: Node key link transaction.
        AGGREGATE_COMPLETE_TRANSACTION: Aggregate complete transaction.
        AGGREGATE_BONDED_TRANSACTION: Aggregate bonded transaction.
        VOTING_KEY_LINK_TRANSACTION: Voting key link transaction.
        VRF_KEY_LINK_TRANSACTION: Vrf key link transaction.
        HASH_LOCK_TRANSACTION: Hash lock transaction.
        SECRET_LOCK_TRANSACTION: Secret lock transaction.
        SECRET_PROOF_TRANSACTION: Secret proof transaction.
        ACCOUNT_METADATA_TRANSACTION: Account metadata transaction.
        MOSAIC_METADATA_TRANSACTION: Mosaic metadata transaction.
        NAMESPACE_METADATA_TRANSACTION: Namespace metadata transaction.
        MOSAIC_DEFINITION_TRANSACTION: Mosaic definition transaction.
        MOSAIC_SUPPLY_CHANGE_TRANSACTION: Mosaic supply change transaction.
        MULTISIG_ACCOUNT_MODIFICATION_TRANSACTION: Multisig account modification transaction.
        ADDRESS_ALIAS_TRANSACTION: Address alias transaction.
        MOSAIC_ALIAS_TRANSACTION: Mosaic alias transaction.
        NAMESPACE_REGISTRATION_TRANSACTION: Namespace registration transaction.
        ACCOUNT_ADDRESS_RESTRICTION_TRANSACTION: Account address restriction transaction.
        ACCOUNT_MOSAIC_RESTRICTION_TRANSACTION: Account mosaic restriction transaction.
        ACCOUNT_OPERATION_RESTRICTION_TRANSACTION: Account operation restriction transaction.
        MOSAIC_ADDRESS_RESTRICTION_TRANSACTION: Mosaic address restriction transaction.
        MOSAIC_GLOBAL_RESTRICTION_TRANSACTION: Mosaic global restriction transaction.
        TRANSFER_TRANSACTION: Transfer transaction.
    """

    RESERVED = 0
    NEMESIS_BLOCK_HEADER = 32835
    NORMAL_BLOCK_HEADER = 33091
    IMPORTANCE_BLOCK_HEADER = 33347
    ACCOUNT_KEY_LINK_TRANSACTION = 16716
    NODE_KEY_LINK_TRANSACTION = 16972
    AGGREGATE_COMPLETE_TRANSACTION = 16705
    AGGREGATE_BONDED_TRANSACTION = 16961
    VOTING_KEY_LINK_TRANSACTION = 16707
    VRF_KEY_LINK_TRANSACTION = 16963
    HASH_LOCK_TRANSACTION = 16712
    SECRET_LOCK_TRANSACTION = 16722
    SECRET_PROOF_TRANSACTION = 16978
    ACCOUNT_METADATA_TRANSACTION = 16708
    MOSAIC_METADATA_TRANSACTION = 16964
    NAMESPACE_METADATA_TRANSACTION = 17220
    MOSAIC_DEFINITION_TRANSACTION = 16717
    MOSAIC_SUPPLY_CHANGE_TRANSACTION = 16973
    MULTISIG_ACCOUNT_MODIFICATION_TRANSACTION = 16725
    ADDRESS_ALIAS_TRANSACTION = 16974
    MOSAIC_ALIAS_TRANSACTION = 17230
    NAMESPACE_REGISTRATION_TRANSACTION = 16718
    ACCOUNT_ADDRESS_RESTRICTION_TRANSACTION = 16720
    ACCOUNT_MOSAIC_RESTRICTION_TRANSACTION = 16976
    ACCOUNT_OPERATION_RESTRICTION_TRANSACTION = 17232
    MOSAIC_ADDRESS_RESTRICTION_TRANSACTION = 16977
    MOSAIC_GLOBAL_RESTRICTION_TRANSACTION = 16721
    TRANSFER_TRANSACTION = 16724

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EntityTypeDto:
        """Creates an instance of EntityTypeDto from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EntityTypeDto.
        """
        value: int = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes(payload), 2))
        return EntityTypeDto(value)

    @classmethod
    def getSize(cls) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        return 2

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.value, 2))
        return bytes_
