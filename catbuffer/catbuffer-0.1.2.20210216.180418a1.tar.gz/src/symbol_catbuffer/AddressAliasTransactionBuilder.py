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
from .AddressAliasTransactionBodyBuilder import AddressAliasTransactionBodyBuilder
from .AddressDto import AddressDto
from .AliasActionDto import AliasActionDto
from .AmountDto import AmountDto
from .EntityTypeDto import EntityTypeDto
from .KeyDto import KeyDto
from .NamespaceIdDto import NamespaceIdDto
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder

class AddressAliasTransactionBuilder(TransactionBuilder):
    """Binary layout for a non-embedded address alias transaction.

    Attributes:
        addressAliasTransactionBody: Address alias transaction body.
    """

    def __init__(self, signature: SignatureDto, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type: EntityTypeDto, fee: AmountDto, deadline: TimestampDto, namespaceId: NamespaceIdDto, address: AddressDto, aliasAction: AliasActionDto):
        """Constructor.
        Args:
            signature: Entity signature.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
            fee: Transaction fee.
            deadline: Transaction deadline.
            namespaceId: Identifier of the namespace that will become an alias.
            address: Aliased address.
            aliasAction: Alias action.
        """
        super().__init__(signature, signerPublicKey, version, network, type, fee, deadline)
        self.addressAliasTransactionBody = AddressAliasTransactionBodyBuilder(namespaceId, address, aliasAction)


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AddressAliasTransactionBuilder:
        """Creates an instance of AddressAliasTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AddressAliasTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        addressAliasTransactionBody = AddressAliasTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[addressAliasTransactionBody.getSize():]
        return AddressAliasTransactionBuilder(superObject.signature, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type, superObject.fee, superObject.deadline, addressAliasTransactionBody.namespaceId, addressAliasTransactionBody.address, addressAliasTransactionBody.aliasAction)

    def getNamespaceId(self) -> NamespaceIdDto:
        """Gets identifier of the namespace that will become an alias.
        Returns:
            Identifier of the namespace that will become an alias.
        """
        return self.addressAliasTransactionBody.getNamespaceId()

    def getAddress(self) -> AddressDto:
        """Gets aliased address.
        Returns:
            Aliased address.
        """
        return self.addressAliasTransactionBody.getAddress()

    def getAliasAction(self) -> AliasActionDto:
        """Gets alias action.
        Returns:
            Alias action.
        """
        return self.addressAliasTransactionBody.getAliasAction()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.addressAliasTransactionBody.getSize()
        return size

    def getBody(self) -> AddressAliasTransactionBodyBuilder:
        """Gets the body builder of the object.
        Returns:
            Body builder.
        """
        return self.addressAliasTransactionBody

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.addressAliasTransactionBody.serialize())  # kind:CUSTOM
        return bytes_
