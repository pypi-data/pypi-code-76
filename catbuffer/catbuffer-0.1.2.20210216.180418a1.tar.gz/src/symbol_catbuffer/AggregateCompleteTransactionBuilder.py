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
from .AggregateTransactionBodyBuilder import AggregateTransactionBodyBuilder
from .AmountDto import AmountDto
from .CosignatureBuilder import CosignatureBuilder
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .Hash256Dto import Hash256Dto
from .KeyDto import KeyDto
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder

class AggregateCompleteTransactionBuilder(TransactionBuilder):
    """Binary layout for an aggregate complete transaction.

    Attributes:
        aggregateTransactionBody: Aggregate transaction body.
    """

    def __init__(self, signature: SignatureDto, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type: EntityTypeDto, fee: AmountDto, deadline: TimestampDto, transactionsHash: Hash256Dto, transactions: List[EmbeddedTransactionBuilder], cosignatures: List[CosignatureBuilder]):
        """Constructor.
        Args:
            signature: Entity signature.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
            fee: Transaction fee.
            deadline: Transaction deadline.
            transactionsHash: Aggregate hash of an aggregate's transactions.
            transactions: Sub-transaction data (transactions are variable sized and payload size is in bytes).
            cosignatures: Cosignatures data (fills remaining body space after transactions).
        """
        super().__init__(signature, signerPublicKey, version, network, type, fee, deadline)
        self.aggregateTransactionBody = AggregateTransactionBodyBuilder(transactionsHash, transactions, cosignatures)


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AggregateCompleteTransactionBuilder:
        """Creates an instance of AggregateCompleteTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AggregateCompleteTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        aggregateTransactionBody = AggregateTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[aggregateTransactionBody.getSize():]
        return AggregateCompleteTransactionBuilder(superObject.signature, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type, superObject.fee, superObject.deadline, aggregateTransactionBody.transactionsHash, aggregateTransactionBody.transactions, aggregateTransactionBody.cosignatures)

    def getTransactionsHash(self) -> Hash256Dto:
        """Gets aggregate hash of an aggregate's transactions.
        Returns:
            Aggregate hash of an aggregate's transactions.
        """
        return self.aggregateTransactionBody.getTransactionsHash()

    def getTransactions(self) -> List[EmbeddedTransactionBuilder]:
        """Gets sub-transaction data (transactions are variable sized and payload size is in bytes).
        Returns:
            Sub-transaction data (transactions are variable sized and payload size is in bytes).
        """
        return self.aggregateTransactionBody.getTransactions()

    def getCosignatures(self) -> List[CosignatureBuilder]:
        """Gets cosignatures data (fills remaining body space after transactions).
        Returns:
            Cosignatures data (fills remaining body space after transactions).
        """
        return self.aggregateTransactionBody.getCosignatures()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.aggregateTransactionBody.getSize()
        return size

    def getBody(self) -> AggregateTransactionBodyBuilder:
        """Gets the body builder of the object.
        Returns:
            Body builder.
        """
        return self.aggregateTransactionBody

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.aggregateTransactionBody.serialize())  # kind:CUSTOM
        return bytes_
