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

# pylint: disable=R0911,R0912

# Imports for creating embedded transaction builders
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EmbeddedAccountAddressRestrictionTransactionBuilder import EmbeddedAccountAddressRestrictionTransactionBuilder
from .EmbeddedAccountKeyLinkTransactionBuilder import EmbeddedAccountKeyLinkTransactionBuilder
from .EmbeddedAccountMetadataTransactionBuilder import EmbeddedAccountMetadataTransactionBuilder
from .EmbeddedAccountMosaicRestrictionTransactionBuilder import EmbeddedAccountMosaicRestrictionTransactionBuilder
from .EmbeddedAccountOperationRestrictionTransactionBuilder import EmbeddedAccountOperationRestrictionTransactionBuilder
from .EmbeddedAddressAliasTransactionBuilder import EmbeddedAddressAliasTransactionBuilder
from .EmbeddedHashLockTransactionBuilder import EmbeddedHashLockTransactionBuilder
from .EmbeddedMosaicAddressRestrictionTransactionBuilder import EmbeddedMosaicAddressRestrictionTransactionBuilder
from .EmbeddedMosaicAliasTransactionBuilder import EmbeddedMosaicAliasTransactionBuilder
from .EmbeddedMosaicDefinitionTransactionBuilder import EmbeddedMosaicDefinitionTransactionBuilder
from .EmbeddedMosaicGlobalRestrictionTransactionBuilder import EmbeddedMosaicGlobalRestrictionTransactionBuilder
from .EmbeddedMosaicMetadataTransactionBuilder import EmbeddedMosaicMetadataTransactionBuilder
from .EmbeddedMosaicSupplyChangeTransactionBuilder import EmbeddedMosaicSupplyChangeTransactionBuilder
from .EmbeddedMultisigAccountModificationTransactionBuilder import EmbeddedMultisigAccountModificationTransactionBuilder
from .EmbeddedNamespaceMetadataTransactionBuilder import EmbeddedNamespaceMetadataTransactionBuilder
from .EmbeddedNamespaceRegistrationTransactionBuilder import EmbeddedNamespaceRegistrationTransactionBuilder
from .EmbeddedNodeKeyLinkTransactionBuilder import EmbeddedNodeKeyLinkTransactionBuilder
from .EmbeddedSecretLockTransactionBuilder import EmbeddedSecretLockTransactionBuilder
from .EmbeddedSecretProofTransactionBuilder import EmbeddedSecretProofTransactionBuilder
from .EmbeddedTransferTransactionBuilder import EmbeddedTransferTransactionBuilder
from .EmbeddedVotingKeyLinkTransactionBuilder import EmbeddedVotingKeyLinkTransactionBuilder
from .EmbeddedVrfKeyLinkTransactionBuilder import EmbeddedVrfKeyLinkTransactionBuilder

class EmbeddedTransactionBuilderFactory:
    """Factory in charge of creating the specific embedded transaction builder from the binary payload.
    """

    @classmethod
    def createBuilder(cls, payload) -> EmbeddedTransactionBuilder:
        """
        It creates the specific embedded transaction builder from the payload bytes.
        Args:
            payload: bytes
        Returns:
            the EmbeddedTransactionBuilder subclass
        """
        headerBuilder = EmbeddedTransactionBuilder.loadFromBinary(payload)
        entityType = headerBuilder.getType().value
        entityTypeVersion = headerBuilder.getVersion()
        if entityType == 16716 and entityTypeVersion == 1:
            return EmbeddedAccountKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 16972 and entityTypeVersion == 1:
            return EmbeddedNodeKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 16707 and entityTypeVersion == 1:
            return EmbeddedVotingKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 16963 and entityTypeVersion == 1:
            return EmbeddedVrfKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 16712 and entityTypeVersion == 1:
            return EmbeddedHashLockTransactionBuilder.loadFromBinary(payload)
        if entityType == 16722 and entityTypeVersion == 1:
            return EmbeddedSecretLockTransactionBuilder.loadFromBinary(payload)
        if entityType == 16978 and entityTypeVersion == 1:
            return EmbeddedSecretProofTransactionBuilder.loadFromBinary(payload)
        if entityType == 16708 and entityTypeVersion == 1:
            return EmbeddedAccountMetadataTransactionBuilder.loadFromBinary(payload)
        if entityType == 16964 and entityTypeVersion == 1:
            return EmbeddedMosaicMetadataTransactionBuilder.loadFromBinary(payload)
        if entityType == 17220 and entityTypeVersion == 1:
            return EmbeddedNamespaceMetadataTransactionBuilder.loadFromBinary(payload)
        if entityType == 16717 and entityTypeVersion == 1:
            return EmbeddedMosaicDefinitionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16973 and entityTypeVersion == 1:
            return EmbeddedMosaicSupplyChangeTransactionBuilder.loadFromBinary(payload)
        if entityType == 16725 and entityTypeVersion == 1:
            return EmbeddedMultisigAccountModificationTransactionBuilder.loadFromBinary(payload)
        if entityType == 16974 and entityTypeVersion == 1:
            return EmbeddedAddressAliasTransactionBuilder.loadFromBinary(payload)
        if entityType == 17230 and entityTypeVersion == 1:
            return EmbeddedMosaicAliasTransactionBuilder.loadFromBinary(payload)
        if entityType == 16718 and entityTypeVersion == 1:
            return EmbeddedNamespaceRegistrationTransactionBuilder.loadFromBinary(payload)
        if entityType == 16720 and entityTypeVersion == 1:
            return EmbeddedAccountAddressRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16976 and entityTypeVersion == 1:
            return EmbeddedAccountMosaicRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 17232 and entityTypeVersion == 1:
            return EmbeddedAccountOperationRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16977 and entityTypeVersion == 1:
            return EmbeddedMosaicAddressRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16721 and entityTypeVersion == 1:
            return EmbeddedMosaicGlobalRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16724 and entityTypeVersion == 1:
            return EmbeddedTransferTransactionBuilder.loadFromBinary(payload)
        return headerBuilder
