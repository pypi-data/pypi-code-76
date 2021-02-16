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
from .KeyDto import KeyDto
from .NamespaceIdDto import NamespaceIdDto
from .NamespaceRegistrationTransactionBodyBuilder import NamespaceRegistrationTransactionBodyBuilder
from .NamespaceRegistrationTypeDto import NamespaceRegistrationTypeDto
from .NetworkTypeDto import NetworkTypeDto

class EmbeddedNamespaceRegistrationTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded namespace registration transaction.

    Attributes:
        namespaceRegistrationTransactionBody: Namespace registration transaction body.
    """

    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type: EntityTypeDto, duration: BlockDurationDto, parentId: NamespaceIdDto, id: NamespaceIdDto, registrationType: NamespaceRegistrationTypeDto, name: bytes):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
            duration: Namespace duration.
            parentId: Parent namespace identifier.
            id: Namespace identifier.
            registrationType: Namespace registration type.
            name: Namespace name.
        """
        super().__init__(signerPublicKey, version, network, type)
        self.namespaceRegistrationTransactionBody = NamespaceRegistrationTransactionBodyBuilder(duration, parentId, id, registrationType, name)


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedNamespaceRegistrationTransactionBuilder:
        """Creates an instance of EmbeddedNamespaceRegistrationTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedNamespaceRegistrationTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        namespaceRegistrationTransactionBody = NamespaceRegistrationTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[namespaceRegistrationTransactionBody.getSize():]
        return EmbeddedNamespaceRegistrationTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type, namespaceRegistrationTransactionBody.duration, namespaceRegistrationTransactionBody.parentId, namespaceRegistrationTransactionBody.id, namespaceRegistrationTransactionBody.registrationType, namespaceRegistrationTransactionBody.name)

    def getDuration(self) -> BlockDurationDto:
        """Gets namespace duration.
        Returns:
            Namespace duration.
        """
        return self.namespaceRegistrationTransactionBody.getDuration()

    def getParentId(self) -> NamespaceIdDto:
        """Gets parent namespace identifier.
        Returns:
            Parent namespace identifier.
        """
        return self.namespaceRegistrationTransactionBody.getParentId()

    def getId(self) -> NamespaceIdDto:
        """Gets namespace identifier.
        Returns:
            Namespace identifier.
        """
        return self.namespaceRegistrationTransactionBody.getId()

    def getRegistrationType(self) -> NamespaceRegistrationTypeDto:
        """Gets namespace registration type.
        Returns:
            Namespace registration type.
        """
        return self.namespaceRegistrationTransactionBody.getRegistrationType()

    def getName(self) -> bytes:
        """Gets namespace name.
        Returns:
            Namespace name.
        """
        return self.namespaceRegistrationTransactionBody.getName()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.namespaceRegistrationTransactionBody.getSize()
        return size

    def getBody(self) -> NamespaceRegistrationTransactionBodyBuilder:
        """Gets the body builder of the object.
        Returns:
            Body builder.
        """
        return self.namespaceRegistrationTransactionBody

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.namespaceRegistrationTransactionBody.serialize())  # kind:CUSTOM
        return bytes_
