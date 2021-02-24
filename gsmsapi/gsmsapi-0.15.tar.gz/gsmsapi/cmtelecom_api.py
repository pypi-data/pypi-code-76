# -*- python -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Cygnus Networks GmbH
# License: MIT

import json
import requests

#: characters allowed in GSM 03.38
GSM0338_CHARS = '@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæÉ !"#¤%&\'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§abcdefghijklmnopqrstuvwxyzäöñüà' + chr(27)

#: characters allowed in GSM 03.38 that occupy two octets
GSM0338_TWO_OCTET_CHARS = '€' + chr(12) + r'[\]^{|}~'

VALID_RESPONSE_CODE = [200, 400]

MESSAGE_TYPE_UNICODE = 'unicode'


class CMTelecomError(Exception):
	"""
	Custom exception type.

	"""
	pass


class CMTelecomAPI(object):  # pylint:disable=R0902,R0921
	"""
	Abstraction of the `cmtelecom.com <http://cmtelecom.com>`_ http(s) mail sending
	API.

	"""
	def __init__(self, producttoken, sender, debug=False, reports=False, concat=False, charset='ascii', messagetype=None):  # pylint: disable=R0913
		"""
		Initialize a new CMTelecom instance.

		"""
		self.reference = None
		self.senddate = None

		self.messagetype = messagetype
		self.producttoken = producttoken

		self.url = "https://gw.cmtelecom.com/v1.0/message"
		self.debug = debug
		self.cost = True
		self.message_id = True
		self.count = True
		self.reports = reports
		self.concat = concat
		self.charset = charset
		self.sender = sender

	def _handle_response(self, response):
		"""
		Handle parsing of response body.

		:param str body:
			response body
		"""
		retval = {}
		try:
			body = json.loads(response.text)
			if self.debug:
				print("DEBUG response body is %s" % repr(body))
		except ValueError:
			raise CMTelecomError('malformed response - no valid json body')

		if "details" not in body:
			raise CMTelecomError("Missing details object in response body")

		if response.status_code == 200:
			if "messages" in body:
				for message in body["messages"]:
					if "to" in message and "status" in message:
						retval[message['to']] = {"status": message["status"]}
					else:
						raise CMTelecomError("Missing field in response message object")
			else:
				raise CMTelecomError("Missing messages object in response body")
		elif response.status_code == 400:
			raise CMTelecomError(body["details"])
		else:
			response.raise_for_status()
		return retval

	def _build_request_parameters(self, recipients, content):
		"""
		Build the request parameter dictionary based on fields in this
		CMTelecomAPI instance.

		:param str recipient:
			recipient calling number

		"""
		to = list()
		for recipient in recipients:
			to.append({'number': recipient})

		msg = {
			"from": self.sender,
			"to": to,
			"body": {
				"content": content
			}
		}

		if self.concat:
			msg["minimumNumberOfMessageParts"] = 1
			msg["maximumNumberOfMessageParts"] = 8

		if self.messagetype == MESSAGE_TYPE_UNICODE:
			msg["dcs"] = 8

		request_params = {
			"messages": {
				"authentication": {
					"producttoken": self.producttoken
				},
				"msg": [msg]
			}
		}

		return request_params

	def _send_normal_message(self, recipients, text):
		"""
		Send a normal SMS message to the given recipient.

		:param list recipients:
			list of recipient calling number

		:param unicode text:
			unicode SMS message text

		"""
		request_params = self._build_request_parameters(recipients, text)
		response = requests.post(self.url, json=request_params)

		if response.status_code not in VALID_RESPONSE_CODE:
			response.raise_for_status()
		return self._handle_response(response)

	def _send_unicode_message(self, recipients, text):
		"""
		Send a unicode SMS message to the given recipient.

		:param list recipients:
			recipient calling number

		:param unicode text:
			unicode SMS message text

		"""
		request_params = self._build_request_parameters(recipients, text)

		response = requests.post(self.url, json=request_params)
		if response.status_code not in VALID_RESPONSE_CODE:
			response.raise_for_status()
		return self._handle_response(response)

	def _send_message(self, recipients, text):
		"""
		Send an SMS to a single recipient.

		:param list recipients:
			list of recipient calling number

		:param str text:
			SMS message text

		"""
		if self.messagetype is None:
			return self._send_normal_message(recipients, text)
		elif self.messagetype == MESSAGE_TYPE_UNICODE:
			return self._send_unicode_message(recipients, text)
		else:
			raise CMTelecomError("unknown message type %s" % self.messagetype)

	@staticmethod
	def _gsm0338_length(text):
		charcount = 0
		for char in text:
			if char in GSM0338_CHARS:
				charcount += 1
			elif char in GSM0338_TWO_OCTET_CHARS:
				charcount += 2
			else:
				raise CMTelecomError("character %s is not allowed in GSM messages." % char)
		return charcount

	def _check_normal_message(self, text):
		"""
		Perform a plausibility check on the given message text.

		:param str text:
			the message to check

		"""
		charcount = self._gsm0338_length(text)
		if (self.concat and charcount > 1530) or (not self.concat and charcount > 160):
			message = "too many characters in message"
			if not self.concat and charcount <= 1530:
				message += ", you may try to use concat"
			raise CMTelecomError(message)
		try:
			text.encode(self.charset)
		except ValueError:
			raise CMTelecomError("The message can not be encoded with the chosen character set %s" % self.charset)

	@staticmethod
	def _check_unicode_message(text):
		"""
		Perform a plausibility check on the given unicode message text.

		:param str text:
			the message to check

		"""
		for char in text:
			code = ord(char)
			if (0xd800 <= code <= 0xdfff) or (code > 0xffff):
				raise CMTelecomError("the message can not be represented in UCS2")
		if len(text) > 70:
			raise CMTelecomError("too many characters in message, unicode SMS may contain up to 70 characters")

	def _check_message(self, text):
		if self.messagetype is None:
			self._check_normal_message(text)
		elif self.messagetype == MESSAGE_TYPE_UNICODE:
			self._check_unicode_message(text)
		else:
			raise CMTelecomError("message type %s is unknown" % self.messagetype)

	def send_sms(self, to, text):
		"""
		Send an SMS to recipients in the to parameter.

		:param list to:
			list of recipient calling numbers

		:param str text:
			SMS message text

		:param dict kwargs:
			keyword arguments that override values in the configuration files

		"""
		if isinstance(to, str):
			to = [to]

		self._check_message(text)
		retval = self._send_message(to, text)
		return retval

	def get_balance(self):
		raise NotImplementedError("Balance check is not supported")
