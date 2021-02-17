#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2021 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

import time
import pytest
from tgsdk import Bot, Location, Contact
from tgsdk.network.request import Request
from tgsdk import InputMediaPhoto, ChatAction
from .constants import TestValues


def test__bot__init():
	_ = Bot(token=TestValues.BOT_API_TOKEN)

	assert _.token == TestValues.BOT_API_TOKEN
	assert _.base_url == "https://api.telegram.org/bot%s" % TestValues.BOT_API_TOKEN
	assert _.base_file_url == "https://api.telegram.org/file/bot%s" % TestValues.BOT_API_TOKEN
	assert _._me is None

	assert isinstance(_.request, Request)

	# TODO:
	assert _._me.id == TestValues.BOT_ID
	assert _._me.first_name == TestValues.BOT_FIRST_NAME
	assert _._me.username == TestValues.BOT_USERNAME
	assert _.link == "https://t.me/%s" % TestValues.BOT_USERNAME
	assert _.tg_link == "tg://resolve?domain=%s" % TestValues.BOT_USERNAME

	assert _.to_dict() == {"id": TestValues.BOT_ID, "username": TestValues.BOT_USERNAME, "first_name": TestValues.BOT_FIRST_NAME}


def test__bot__init__with_urls():
	_ = Bot(
		token=TestValues.BOT_API_TOKEN,
		base_url="https://api.telegram.org/bot",
		base_file_url="https://api.telegram.org/file/bot"
	)

	assert _.token == TestValues.BOT_API_TOKEN
	assert _.base_url == "https://api.telegram.org/bot%s" % TestValues.BOT_API_TOKEN
	assert _.base_file_url == "https://api.telegram.org/file/bot%s" % TestValues.BOT_API_TOKEN
	assert _._me is None

	assert isinstance(_.request, Request)

	# TODO:
	assert _._me.id == TestValues.BOT_ID
	assert _._me.first_name == TestValues.BOT_FIRST_NAME
	assert _._me.username == TestValues.BOT_USERNAME
	assert _.link == "https://t.me/%s" % TestValues.BOT_USERNAME
	assert _.tg_link == "tg://resolve?domain=%s" % TestValues.BOT_USERNAME

	assert _.to_dict() == {"id": TestValues.BOT_ID, "username": TestValues.BOT_USERNAME, "first_name": TestValues.BOT_FIRST_NAME}


def test__bot__get_me():
	_ = Bot(token=TestValues.BOT_API_TOKEN)

	result = _.get_me()

	assert result.is_bot is True
	assert result.id == TestValues.BOT_ID
	assert result.first_name == TestValues.BOT_FIRST_NAME
	assert result.username == TestValues.BOT_USERNAME


def test__bot__build_chat_id__int_above_zero():
	chat_id = Bot.build_chat_id(chat_id=123)

	assert chat_id == -123


def test__bot__build_chat_id__int_below_zero():
	chat_id = Bot.build_chat_id(chat_id=-123)

	assert chat_id == -123


def test__bot__build_chat_id__username_without_at():
	chat_id = Bot.build_chat_id(chat_id="username")

	assert chat_id == "@username"


def test__bot__build_chat_id__username_with_at():
	chat_id = Bot.build_chat_id(chat_id="@username")

	assert chat_id == "@username"


def test__bot__webhook():
	_ = Bot(token=TestValues.BOT_API_TOKEN)

	result = _.set_webhook(
		url="https://telegram.org",
		max_connections=100
	)
	assert result is True

	result = _.get_webhook_info()
	assert result.url == "https://telegram.org"
	assert result.max_connections == 100
	assert result.allowed_updates == ["message", "callback_query"]
	assert result.has_custom_certificate is False
	assert result.pending_update_count == 0
	assert result.ip_address is not None
	assert result.ip_address == "149.154.167.99"  # TODO:
	assert result.last_error_date is None
	assert result.last_error_message is None

	result = _.delete_webhook()
	assert result is True

	result = _.get_webhook_info()
	assert result.url == ""
	assert result.max_connections is None
	assert result.allowed_updates == ["message", "callback_query"]
	assert result.has_custom_certificate is False
	assert result.pending_update_count == 0
	assert result.ip_address is None
	assert result.last_error_date is None
	assert result.last_error_message is None

	time.sleep(2)

	result = _.set_webhook(
		url="https://telegram.org",
		allowed_updates=["message"],
		ip_address="149.154.167.99",
		drop_pending_updates=True
	)
	assert result is True

	result = _.get_webhook_info()
	assert result.url == "https://telegram.org"
	assert result.max_connections == 50
	assert result.allowed_updates == ["message"]
	assert result.has_custom_certificate is False
	assert result.pending_update_count == 0
	assert result.ip_address == "149.154.167.99"
	assert result.last_error_date is None
	assert result.last_error_message is None


	result = _.delete_webhook()
	assert result is True


#

# result = bot.send_media_group(
# 	chat_id=1031684366,
# 	media=[
# 		InputMediaPhoto(
# 			media="https://images.unsplash.com/photo-1541185933-ef5d8ed016c2?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MjZ8fHNwYWNleHxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&w=1000&q=80",
# 			caption="MEDIA URL"
# 		)
# 	]
# )
# print(result)


# result = bot.send_media_group(
# 	chat_id=1031684366,
# 	media=[
# 		InputMediaPhoto(
# 			media="AgACAgQAAxkDAAEO841gFJBqYq5E0xS8-iuSTKNwj4768QACyKsxG9-VrVAAAQPEWh2UBDA0I9knXQADAQADAgADeQADz7sEAAEeBA",
# 			caption="MEDIA FILE ID"
# 		)
# 	]
# )
# print(result)


# file = open("../data/img.jpeg", "rb")
# result = bot.send_media_group(
# 	chat_id=1031684366,
# 	media=[
# 		InputMediaPhoto(
# 			media=file,
# 			caption="MEDIA LOCAL FILE"
# 		)
# 	]
# )
# print(result)


# result = bot.get_file(file_id="AgACAgQAAxkDAAEO841gFJBqYq5E0xS8-iuSTKNwj4768QACyKsxG9-VrVAAAQPEWh2UBDA0I9knXQADAQADAgADeQADz7sEAAEeBA")
# print(result)



# result = bot.get_my_commands()
# print(result)


# result = bot.send_chat_action(
# 	chat_id=1031684366,
# 	action=ChatAction.TYPING
# )
# print(result)


# result = bot.send_photo(
# 	chat_id=1031684366,
# 	photo="https://c.files.bbci.co.uk/D810/production/_112421355_ifat-with-metadata-1.jpg",
# 	caption="PHOTO URL"
# )
# print(result)


# result = bot.send_photo(
# 	chat_id=1031684366,
# 	photo="AgACAgQAAxkDAAEO841gFJBqYq5E0xS8-iuSTKNwj4768QACyKsxG9-VrVAAAQPEWh2UBDA0I9knXQADAQADAgADeQADz7sEAAEeBA",
# 	caption="PHOTO FILE ID"
# )
# print(result)


# file = open("../data/img2.jpg", "rb")
# result = bot.send_photo(
# 	chat_id=1031684366,
# 	photo=file,
# 	caption="PHOTO LOCAL FILE"
# )
# print(result)


# result = bot.set_my_commands(
# 	commands=[
# 		(
# 			"/start",
# 			"Перезапуск бота"
# 		)
# 	]
# )
# print(result)


# result = bot.send_contact(
# 	chat_id="1031684366",
# 	phone_number="76665554433",
# 	first_name="First Name"
# )
# print(result)


# result = bot.send_contact(
# 	chat_id="1031684366",
# 	contact=Contact(
# 		phone_number="+76665554433",
# 		first_name="First Name Contact"
# 	)
# )
# print(result)


# result = bot.send_location(
# 	chat_id=1031684366,
# 	latitude=50,
# 	longitude=30
# )
# print(result)


# result = bot.send_location(
# 	chat_id=1031684366,
# 	location=Location(
# 		latitude=50,
# 		longitude=30
# 	)
# )
# print(result)


# result = bot.send_document(
# 	chat_id=1031684366,
# 	document="https://planetpdf.com/planetpdf/pdfs/pdf_tmpl.pdf",
# 	caption="DOCUMENT URL"
# )
# print(result)


# result = bot.send_document(
# 	chat_id=1031684366,
# 	document="BQACAgQAAxkDAAEO86NgFRyoLqB0yTfKMsoUcz0aMHETsAAChAIAAvGwrFD57OPd7lDGLx4E",
# 	caption="DOCUMENT FILE ID"
# )
# print(result)


# file = open("../data/pdf.pdf", "rb")
# result = bot.send_document(
# 	chat_id=1031684366,
# 	document=file,
# 	caption="DOCUMENT LOCAL FILE"
# )
# print(result)


# result = bot.send_audio(
# 	chat_id=1031684366,
# 	audio="https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3",
# 	caption="AUDIO URL"
# )
# print(result)


# result = bot.send_audio(
# 	chat_id=1031684366,
# 	audio="CQACAgQAAxkDAAEO86ZgFR2mP2z3vjVy5rdB-IJD9gr8swACXwIAAltDRFBVXDhbwMwrwR4E",
# 	caption="AUDIO FILE ID"
# )
# print(result)


# file = open("../data/mp3.mp3", "rb")
# result = bot.send_audio(
# 	chat_id=1031684366,
# 	audio=file,
# 	caption="AUDIO LOCAL FILE"
# )
# print(result)


# result = bot.send_video(
# 	chat_id=1031684366,
# 	video="https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4",
# 	caption="VIDEO URL"
# )
# print(result)


# result = bot.send_video(
# 	chat_id=1031684366,
# 	video="BAACAgQAAxkDAAEO86pgFR6mFN7s8zraoRrgmHatC-c3xQACTQIAAknVLFPQKja5jtZtnB4E",
# 	caption="VIDEO FILE ID"
# )
# print(result)


# file = open("../data/mp4.mp4", "rb")
# result = bot.send_video(
# 	chat_id=1031684366,
# 	video=file,
# 	caption="VIDEO LOCAL FILE"
# )
# print(result)


# result = bot.send_voice(
# 	chat_id=1031684366,
# 	voice="https://file-examples-com.github.io/uploads/2017/11/file_example_OOG_1MG.ogg",
# 	caption="VOICE URL"
# )
# print(result)


# result = bot.send_voice(
# 	chat_id=1031684366,
# 	voice="AwACAgIAAxkDAAEO869gFR9i8Hl5plwzlZ5SNYxLaXimEgACagwAAkTvqEgzjfWu0U6AyR4E",
# 	caption="VOICE FILE ID"
# )
# print(result)


# file = open("../data/ogg.ogg", "rb")
# result = bot.send_voice(
# 	chat_id=1031684366,
# 	voice=file,
# 	caption="VOICE LOCAL FILE"
# )
# print(result)


# # KEYBOARDS
# from tgsdk import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, LoginUrl

# bot.send_message(
# 	chat_id=1031684366,
# 	text="ReplyMarkup",
# 	reply_markup=ReplyKeyboardMarkup(keyboard=[
# 		[
# 			"Top 1.1", "Top 1.2"
# 		],
# 		[
# 			"Bottom 1.1"
# 		],
# 	], resize_keyboard=True)
# )


# result = bot.send_message(
# 	chat_id=1031684366,
# 	text="Inline Keyboard",
# 	reply_markup=InlineKeyboardMarkup(
# 		inline_keyboard=[
# 			[
# 				InlineKeyboardButton(
# 					text="Callback",
# 					callback_data="callback"
# 				)
# 			],
# 			[
# 				InlineKeyboardButton(
# 					text="URL",
# 					url="https://google.com"
# 				)
# 			],
# 			[
# 				InlineKeyboardButton(
# 					text="Login URL",
# 					login_url=LoginUrl(
# 						url="https://app.botmaker.co/login"
# 					)
# 				)
# 			],
# 			[
# 				InlineKeyboardButton(
# 					text="Switch",
# 					switch_inline_query="Switch inline"
# 				)
# 			],
# 			[
# 				InlineKeyboardButton(
# 					text="Switch current Chat",
# 					switch_inline_query_current_chat="Switch Current Chat"
# 				)
# 			]
# 		]
# 	)
# )
# print(result)


# result = bot.copy_message(
# 	chat_id="1031684366",
# 	from_chat_id="1031684366",
# 	message_id=979907
# )
# print(result)


# result = bot.get_chat(
# 	chat_id="1001193605030"
# )
# print(result)


# result = bot.get_chat(
# 	chat_id="-1001193605030"
# )
# print(result)


# result = bot.get_chat(
# 	chat_id="@test_chats_1"
# )
# print(result)


# result = bot.get_chat(
# 	chat_id="test_chats_1"
# )
# print(result)


# result = bot.get_chat_member(
# 	chat_id="test_chats_1",
# 	user_id="1031684366"
# )
# print(result)


# result = bot.get_chat_administrators(
# 	chat_id="test_chats_1",
# )
# print(result)


# result = bot.get_chat_members_count(
# 	chat_id="test_chats_1",
# )
# print(result)


# result = bot.set_chat_title(
# 	chat_id="test_chats_1",
# 	title="Channel Subscription"
# )
# print(result)


# result = bot.set_chat_description(
# 	chat_id="test_chats_1",
# 	description="Channel Subscription 1"
# )
# print(result)


# result = bot.export_chat_invite_link(
# 	chat_id="test_chats_1",
# )
# print(result)
