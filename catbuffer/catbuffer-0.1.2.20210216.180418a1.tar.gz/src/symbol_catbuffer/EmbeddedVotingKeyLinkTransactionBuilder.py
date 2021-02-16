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
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .FinalizationEpochDto import FinalizationEpochDto
from .KeyDto import KeyDto
from .LinkActionDto import LinkActionDto
from .NetworkTypeDto import NetworkTypeDto
from .VotingKeyDto import VotingKeyDto
from .VotingKeyLinkTransactionBodyBuilder import VotingKeyLinkTransactionBodyBuilder

class EmbeddedVotingKeyLinkTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded voting key link transaction.

    Attributes:
        votingKeyLinkTransactionBody: Voting key link transaction body.
    """

    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type: EntityTypeDto, linkedPublicKey: VotingKeyDto, startEpoch: FinalizationEpochDto, endEpoch: FinalizationEpochDto, linkAction: LinkActionDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
            linkedPublicKey: Linked public key.
            startEpoch: Start finalization epoch.
            endEpoch: End finalization epoch.
            linkAction: Link action.
        """
        super().__init__(signerPublicKey, version, network, type)
        self.votingKeyLinkTransactionBody = VotingKeyLinkTransactionBodyBuilder(linkedPublicKey, startEpoch, endEpoch, linkAction)


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedVotingKeyLinkTransactionBuilder:
        """Creates an instance of EmbeddedVotingKeyLinkTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedVotingKeyLinkTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        votingKeyLinkTransactionBody = VotingKeyLinkTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[votingKeyLinkTransactionBody.getSize():]
        return EmbeddedVotingKeyLinkTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type, votingKeyLinkTransactionBody.linkedPublicKey, votingKeyLinkTransactionBody.startEpoch, votingKeyLinkTransactionBody.endEpoch, votingKeyLinkTransactionBody.linkAction)

    def getLinkedPublicKey(self) -> VotingKeyDto:
        """Gets linked public key.
        Returns:
            Linked public key.
        """
        return self.votingKeyLinkTransactionBody.getLinkedPublicKey()

    def getStartEpoch(self) -> FinalizationEpochDto:
        """Gets start finalization epoch.
        Returns:
            Start finalization epoch.
        """
        return self.votingKeyLinkTransactionBody.getStartEpoch()

    def getEndEpoch(self) -> FinalizationEpochDto:
        """Gets end finalization epoch.
        Returns:
            End finalization epoch.
        """
        return self.votingKeyLinkTransactionBody.getEndEpoch()

    def getLinkAction(self) -> LinkActionDto:
        """Gets link action.
        Returns:
            Link action.
        """
        return self.votingKeyLinkTransactionBody.getLinkAction()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.votingKeyLinkTransactionBody.getSize()
        return size

    def getBody(self) -> VotingKeyLinkTransactionBodyBuilder:
        """Gets the body builder of the object.
        Returns:
            Body builder.
        """
        return self.votingKeyLinkTransactionBody

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.votingKeyLinkTransactionBody.serialize())  # kind:CUSTOM
        return bytes_
