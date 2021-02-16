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
from .Hash256Dto import Hash256Dto
from .LockHashAlgorithmDto import LockHashAlgorithmDto
from .UnresolvedAddressDto import UnresolvedAddressDto

class SecretProofTransactionBodyBuilder:
    """Binary layout for a secret proof transaction.

    Attributes:
        recipientAddress: Locked mosaic recipient address.
        secret: Secret.
        hashAlgorithm: Hash algorithm.
        proof: Proof data.
    """

    def __init__(self, recipientAddress: UnresolvedAddressDto, secret: Hash256Dto, hashAlgorithm: LockHashAlgorithmDto, proof: bytes):
        """Constructor.
        Args:
            recipientAddress: Locked mosaic recipient address.
            secret: Secret.
            hashAlgorithm: Hash algorithm.
            proof: Proof data.
        """
        self.recipientAddress = recipientAddress
        self.secret = secret
        self.hashAlgorithm = hashAlgorithm
        self.proof = proof


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> SecretProofTransactionBodyBuilder:
        """Creates an instance of SecretProofTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of SecretProofTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        recipientAddress = UnresolvedAddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[recipientAddress.getSize():]
        secret = Hash256Dto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[secret.getSize():]
        proofSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))  # kind:SIZE_FIELD
        bytes_ = bytes_[2:]
        hashAlgorithm = LockHashAlgorithmDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[hashAlgorithm.getSize():]
        proof = GeneratorUtils.getBytes(bytes_, proofSize)  # kind:BUFFER
        bytes_ = bytes_[proofSize:]
        return SecretProofTransactionBodyBuilder(recipientAddress, secret, hashAlgorithm, proof)

    def getRecipientAddress(self) -> UnresolvedAddressDto:
        """Gets locked mosaic recipient address.
        Returns:
            Locked mosaic recipient address.
        """
        return self.recipientAddress

    def getSecret(self) -> Hash256Dto:
        """Gets secret.
        Returns:
            Secret.
        """
        return self.secret

    def getHashAlgorithm(self) -> LockHashAlgorithmDto:
        """Gets hash algorithm.
        Returns:
            Hash algorithm.
        """
        return self.hashAlgorithm

    def getProof(self) -> bytes:
        """Gets proof data.
        Returns:
            Proof data.
        """
        return self.proof

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.recipientAddress.getSize()
        size += self.secret.getSize()
        size += 2  # proofSize
        size += self.hashAlgorithm.getSize()
        size += len(self.proof)
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.recipientAddress.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.secret.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getProof()), 2))  # kind:SIZE_FIELD
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.hashAlgorithm.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.proof)  # kind:BUFFER
        return bytes_
