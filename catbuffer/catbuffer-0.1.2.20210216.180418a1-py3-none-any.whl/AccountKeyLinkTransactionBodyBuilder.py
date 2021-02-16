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
from .KeyDto import KeyDto
from .LinkActionDto import LinkActionDto

class AccountKeyLinkTransactionBodyBuilder:
    """Binary layout for an account key link transaction.

    Attributes:
        linkedPublicKey: Linked public key.
        linkAction: Link action.
    """

    def __init__(self, linkedPublicKey: KeyDto, linkAction: LinkActionDto):
        """Constructor.
        Args:
            linkedPublicKey: Linked public key.
            linkAction: Link action.
        """
        self.linkedPublicKey = linkedPublicKey
        self.linkAction = linkAction


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountKeyLinkTransactionBodyBuilder:
        """Creates an instance of AccountKeyLinkTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountKeyLinkTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        linkedPublicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[linkedPublicKey.getSize():]
        linkAction = LinkActionDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[linkAction.getSize():]
        return AccountKeyLinkTransactionBodyBuilder(linkedPublicKey, linkAction)

    def getLinkedPublicKey(self) -> KeyDto:
        """Gets linked public key.
        Returns:
            Linked public key.
        """
        return self.linkedPublicKey

    def getLinkAction(self) -> LinkActionDto:
        """Gets link action.
        Returns:
            Link action.
        """
        return self.linkAction

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.linkedPublicKey.getSize()
        size += self.linkAction.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.linkedPublicKey.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.linkAction.serialize())  # kind:CUSTOM
        return bytes_
