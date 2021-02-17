#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2021 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

import json
import unittest

from tgsdk import Update, Message, CallbackQuery
# TODO:

def test__update__init():
	_ = Chat(
		id=123,
		type=Chat.CHAT_GROUP,
		title="title"
	)

	assert _.id == 123
	assert _.type == "group"
	assert _.title == "title"
	assert _.username is None
	assert _.first_name is None
	assert _.last_name is None
	assert _.photo is None
	assert _.description is None
	assert _.invite_link is None
	assert _.pinned_message is None
	assert _.permissions is None
	assert _.slow_mode_delay is None
	assert _.bio is None
	assert _.linked_chat_id is None
	assert _.location is None


def test__chat__to_dict():
	_ = Update(
		id=123,
		type=Chat.CHAT_GROUP,
		title="title"
	)

	unittest.TestCase().assertDictEqual(
		_.to_dict(),
		{
			"id": 123,
			"type": "group",
			"title": "title"
		}
	)


def test__chat__to_json():
	_ = Update(
		id=123,
		type=Chat.CHAT_GROUP,
		title="title"
	)

	unittest.TestCase().assertDictEqual(
		json.loads(_.to_json()),
		{
			"id": 123,
			"type": "group",
			"title": "title"
		}
	)


def test__chat__de_json():
	data = {
		"id": 123,
		"type": "group",
		"title": "title"
	}

	_ = Update.de_json(data)

	assert isinstance(_, Update) is True
	assert _.id == 123
	assert _.type == "group"
	assert _.title == "title"
	assert _.username is None
	assert _.first_name is None
	assert _.last_name is None
	assert _.photo is None
	assert _.description is None
	assert _.invite_link is None
	assert _.pinned_message is None
	assert _.permissions is None
	assert _.slow_mode_delay is None
	assert _.bio is None
	assert _.linked_chat_id is None
	assert _.location is None


def test__chat__de_json__data_is_none():
	data = None

	_ = Update.de_json(data)

	assert _ is None
