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
from .FinalizationEpochDto import FinalizationEpochDto
from .LinkActionDto import LinkActionDto
from .VotingKeyDto import VotingKeyDto

class VotingKeyLinkTransactionBodyBuilder:
    """Binary layout for a voting key link transaction.

    Attributes:
        linkedPublicKey: Linked public key.
        startEpoch: Start finalization epoch.
        endEpoch: End finalization epoch.
        linkAction: Link action.
    """

    def __init__(self, linkedPublicKey: VotingKeyDto, startEpoch: FinalizationEpochDto, endEpoch: FinalizationEpochDto, linkAction: LinkActionDto):
        """Constructor.
        Args:
            linkedPublicKey: Linked public key.
            startEpoch: Start finalization epoch.
            endEpoch: End finalization epoch.
            linkAction: Link action.
        """
        self.linkedPublicKey = linkedPublicKey
        self.startEpoch = startEpoch
        self.endEpoch = endEpoch
        self.linkAction = linkAction


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> VotingKeyLinkTransactionBodyBuilder:
        """Creates an instance of VotingKeyLinkTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of VotingKeyLinkTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        linkedPublicKey = VotingKeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[linkedPublicKey.getSize():]
        startEpoch = FinalizationEpochDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[startEpoch.getSize():]
        endEpoch = FinalizationEpochDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[endEpoch.getSize():]
        linkAction = LinkActionDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[linkAction.getSize():]
        return VotingKeyLinkTransactionBodyBuilder(linkedPublicKey, startEpoch, endEpoch, linkAction)

    def getLinkedPublicKey(self) -> VotingKeyDto:
        """Gets linked public key.
        Returns:
            Linked public key.
        """
        return self.linkedPublicKey

    def getStartEpoch(self) -> FinalizationEpochDto:
        """Gets start finalization epoch.
        Returns:
            Start finalization epoch.
        """
        return self.startEpoch

    def getEndEpoch(self) -> FinalizationEpochDto:
        """Gets end finalization epoch.
        Returns:
            End finalization epoch.
        """
        return self.endEpoch

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
        size += self.startEpoch.getSize()
        size += self.endEpoch.getSize()
        size += self.linkAction.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.linkedPublicKey.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.startEpoch.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.endEpoch.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.linkAction.serialize())  # kind:CUSTOM
        return bytes_
