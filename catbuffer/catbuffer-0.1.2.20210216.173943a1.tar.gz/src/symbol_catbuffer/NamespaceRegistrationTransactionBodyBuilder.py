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
from .NamespaceIdDto import NamespaceIdDto
from .NamespaceRegistrationTypeDto import NamespaceRegistrationTypeDto

class NamespaceRegistrationTransactionBodyBuilder:
    """Binary layout for a namespace registration transaction.

    Attributes:
        duration: Namespace duration.
        parentId: Parent namespace identifier.
        id: Namespace identifier.
        registrationType: Namespace registration type.
        name: Namespace name.
    """

    def __init__(self, duration: BlockDurationDto, parentId: NamespaceIdDto, id: NamespaceIdDto, registrationType: NamespaceRegistrationTypeDto, name: bytes):
        """Constructor.
        Args:
            duration: Namespace duration.
            parentId: Parent namespace identifier.
            id: Namespace identifier.
            registrationType: Namespace registration type.
            name: Namespace name.
        """
        self.duration = duration
        self.parentId = parentId
        self.id = id
        self.registrationType = registrationType
        self.name = name


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> NamespaceRegistrationTransactionBodyBuilder:
        """Creates an instance of NamespaceRegistrationTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of NamespaceRegistrationTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        registrationTypeCondition = bytes_[0:8]
        bytes_ = bytes_[8:]

        id = NamespaceIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[id.getSize():]
        registrationType = NamespaceRegistrationTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[registrationType.getSize():]
        nameSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        name = GeneratorUtils.getBytes(bytes_, nameSize)  # kind:BUFFER
        bytes_ = bytes_[nameSize:]
        duration = None
        if registrationType == NamespaceRegistrationTypeDto.ROOT:
            duration = BlockDurationDto.loadFromBinary(registrationTypeCondition)  # kind:CUSTOM3
        parentId = None
        if registrationType == NamespaceRegistrationTypeDto.CHILD:
            parentId = NamespaceIdDto.loadFromBinary(registrationTypeCondition)  # kind:CUSTOM3
        return NamespaceRegistrationTransactionBodyBuilder(duration, parentId, id, registrationType, name)

    def getDuration(self) -> BlockDurationDto:
        """Gets namespace duration.
        Returns:
            Namespace duration.
        """
        if not self.registrationType == NamespaceRegistrationTypeDto.ROOT:
            raise Exception('registrationType is not set to ROOT.')
        return self.duration

    def getParentId(self) -> NamespaceIdDto:
        """Gets parent namespace identifier.
        Returns:
            Parent namespace identifier.
        """
        if not self.registrationType == NamespaceRegistrationTypeDto.CHILD:
            raise Exception('registrationType is not set to CHILD.')
        return self.parentId

    def getId(self) -> NamespaceIdDto:
        """Gets namespace identifier.
        Returns:
            Namespace identifier.
        """
        return self.id

    def getRegistrationType(self) -> NamespaceRegistrationTypeDto:
        """Gets namespace registration type.
        Returns:
            Namespace registration type.
        """
        return self.registrationType

    def getName(self) -> bytes:
        """Gets namespace name.
        Returns:
            Namespace name.
        """
        return self.name

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        if self.registrationType == NamespaceRegistrationTypeDto.ROOT:
            size += self.duration.getSize()
        if self.registrationType == NamespaceRegistrationTypeDto.CHILD:
            size += self.parentId.getSize()
        size += self.id.getSize()
        size += self.registrationType.getSize()
        size += 1  # nameSize
        size += len(self.name)
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        if self.registrationType == NamespaceRegistrationTypeDto.ROOT:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.duration.serialize())  # kind:CUSTOM
        if self.registrationType == NamespaceRegistrationTypeDto.CHILD:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.parentId.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.id.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.registrationType.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getName()), 1))  # kind:SIZE_FIELD
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.name)  # kind:BUFFER
        return bytes_
