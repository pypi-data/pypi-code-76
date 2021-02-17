#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2021 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

from typing import TYPE_CHECKING

from tgsdk import (
	ChatPhoto,
	TelegramEntity,
)
from tgsdk.utils import constants
from .chatlocation import ChatLocation
from .chatpermissions import ChatPermissions

if TYPE_CHECKING:
	from tgsdk import Message


class Chat(TelegramEntity):
	"""
	https://core.telegram.org/bots/api#chat

	"""
	__slots__ = (
		"id", "type", "title", "username", "first_name", "last_name", "photo", "description", "invite_link",
		"pinned_message", "permissions", "slow_mode_delay", "bio", "linked_chat_id", "location"
	)

	PRIVATE = constants.CHAT_PRIVATE  # type: str
	CHAT_CHANNEL = constants.CHAT_CHANNEL  # type: str
	CHAT_GROUP = constants.CHAT_GROUP  # type: str
	CHAT_SUPERGROUP = constants.CHAT_SUPERGROUP  # type: str

	def __init__(
		self,
		id: int,
		type: str,
		title: str = None,
		username: str = None,
		first_name: str = None,
		last_name: str = None,
		photo: ChatPhoto = None,
		description: str = None,
		invite_link: str = None,
		pinned_message: "Message" = None,
		permissions: ChatPermissions = None,
		slow_mode_delay: int = None,
		bio: str = None,
		linked_chat_id: int = None,
		location: ChatLocation = None
	):
		self.id = id
		self.type = type
		self.title = title
		self.username = username
		self.first_name = first_name
		self.last_name = last_name
		self.photo = photo
		self.description = description
		self.invite_link = invite_link
		self.pinned_message = pinned_message
		self.permissions = permissions
		self.slow_mode_delay = slow_mode_delay
		self.bio = bio
		self.linked_chat_id = linked_chat_id
		self.location = location

	def is_private(self) -> bool:
		return self.type == self.PRIVATE

	def is_channel(self) -> bool:
		return self.type == self.CHAT_CHANNEL

	def is_group(self) -> bool:
		return self.type == self.CHAT_GROUP

	def is_supergroup(self) -> bool:
		return self.type == self.CHAT_SUPERGROUP
