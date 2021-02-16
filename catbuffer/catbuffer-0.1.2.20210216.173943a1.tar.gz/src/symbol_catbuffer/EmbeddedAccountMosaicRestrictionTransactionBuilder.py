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
from .AccountMosaicRestrictionTransactionBodyBuilder import AccountMosaicRestrictionTransactionBodyBuilder
from .AccountRestrictionFlagsDto import AccountRestrictionFlagsDto
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .KeyDto import KeyDto
from .NetworkTypeDto import NetworkTypeDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto

class EmbeddedAccountMosaicRestrictionTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded account mosaic restriction transaction.

    Attributes:
        accountMosaicRestrictionTransactionBody: Account mosaic restriction transaction body.
    """

    def __init__(self, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type: EntityTypeDto, restrictionFlags: List[AccountRestrictionFlagsDto], restrictionAdditions: List[UnresolvedMosaicIdDto], restrictionDeletions: List[UnresolvedMosaicIdDto]):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
            restrictionFlags: Account restriction flags.
            restrictionAdditions: Account restriction additions.
            restrictionDeletions: Account restriction deletions.
        """
        super().__init__(signerPublicKey, version, network, type)
        self.accountMosaicRestrictionTransactionBody = AccountMosaicRestrictionTransactionBodyBuilder(restrictionFlags, restrictionAdditions, restrictionDeletions)


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedAccountMosaicRestrictionTransactionBuilder:
        """Creates an instance of EmbeddedAccountMosaicRestrictionTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedAccountMosaicRestrictionTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        accountMosaicRestrictionTransactionBody = AccountMosaicRestrictionTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[accountMosaicRestrictionTransactionBody.getSize():]
        return EmbeddedAccountMosaicRestrictionTransactionBuilder(superObject.signerPublicKey, superObject.version, superObject.network, superObject.type, accountMosaicRestrictionTransactionBody.restrictionFlags, accountMosaicRestrictionTransactionBody.restrictionAdditions, accountMosaicRestrictionTransactionBody.restrictionDeletions)

    def getRestrictionFlags(self) -> List[AccountRestrictionFlagsDto]:
        """Gets account restriction flags.
        Returns:
            Account restriction flags.
        """
        return self.accountMosaicRestrictionTransactionBody.getRestrictionFlags()

    def getRestrictionAdditions(self) -> List[UnresolvedMosaicIdDto]:
        """Gets account restriction additions.
        Returns:
            Account restriction additions.
        """
        return self.accountMosaicRestrictionTransactionBody.getRestrictionAdditions()

    def getRestrictionDeletions(self) -> List[UnresolvedMosaicIdDto]:
        """Gets account restriction deletions.
        Returns:
            Account restriction deletions.
        """
        return self.accountMosaicRestrictionTransactionBody.getRestrictionDeletions()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.accountMosaicRestrictionTransactionBody.getSize()
        return size

    def getBody(self) -> AccountMosaicRestrictionTransactionBodyBuilder:
        """Gets the body builder of the object.
        Returns:
            Body builder.
        """
        return self.accountMosaicRestrictionTransactionBody

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.accountMosaicRestrictionTransactionBody.serialize())  # kind:CUSTOM
        return bytes_
