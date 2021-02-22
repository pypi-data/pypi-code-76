#!/usr/bin/env python
import logging
import typing
from eupy.native import shell
from eupy.hermes import client

NOTSET = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

"""
Wrapper class over logging.Logger to automate formatting and other jobs
"""
class _Logger:

	def __init__(self,
							 name   : str,
							 level  : int,
							 client : typing.Tuple[client.gmail, int],
							 colorize   : bool,
							 step  		  : bool,
							 self_debug : bool):
		self._mail_client, self._mail_level = client
		self._colorize    = colorize
		self._step        = step
		self._self_debug  = self_debug
		self._configLogger(name, level)
		if self.self_debug:
			self.debug("Logger initialized")
		return

	def _configLogger(self, name, level):
		# create logger
		logging.root.handlers = []
		self._logger = logging.getLogger(name)
		self._logger.setLevel(level)

		# create console handler and set level to debug
		ch = logging.StreamHandler()
		ch.setLevel(level)

		# create formatter
		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

		# add formatter to ch
		ch.setFormatter(formatter)

		# add ch to logger
		if not self._logger.handlers:
			self._logger.addHandler(ch)
			self._logger.propagate = False
		if self.self_debug:
			self.debug("logger._Logger._configLogger()")
		self.info("Logger has been initialized")
		return

	@property
	def handlers(self):
		return self._logger.handlers

	@property
	def logger(self):
		return self._logger
	
	@property
	def level(self):
		return logging.getLevelName(self._logger.level)

	@level.setter
	def level(self, lvl):
		self.logger.setLevel(lvl)
		self.handlers[0].setLevel(lvl)
		return

	@property
	def self_debug(self):
		return self._self_debug

	@property
	def enable_step(self):
		self._step = True

	@property
	def disable_step(self):
		self._step = False

	"""
	Main logging functions
	"""
	def debug(self, message, mail_level = 6, step = False):
		if self._colorize:
			message = shell.output(message, shell.bold, shell.green)
		if mail_level >= self._mail_level:
			self._mail_client.send_message("Logger", message)
		self._logger.debug(message)
		if self._logger.level == DEBUG and (self._step or step):
			try:
				input()
			except EOFError as e:
				self.warning(e)

	def info(self, message, mail_level = 6):
		if self._colorize:
			message = shell.output(message, shell.bold, shell.cyan)
		if mail_level >= self._mail_level:
			self._mail_client.send_message("Logger", message)
		self._logger.info(message)

	def warning(self, message, mail_level = 6):
		if self._colorize:
			message = shell.output(message, shell.bold, shell.yellow)
		if mail_level >= self._mail_level:
			self._mail_client.send_message("Logger", message)
		self._logger.warning(message)

	def warn(self, message, mail_level = 6):
		if self._colorize:
			message = shell.output(message, shell.bold, shell.yellow)
		if mail_level >= self._mail_level:
			self._mail_client.send_message("Logger", message)
		self._logger.warn(message)

	def error(self, message, mail_level = 6):
		if self._colorize:
			message = shell.output(message, shell.bold, shell.red)
		if mail_level >= self._mail_level:
			self._mail_client.send_message("Logger", message)
		self._logger.error(message)
	
	def critical(self, message, mail_level = 6):
		if self._colorize:
			message = shell.output(message, shell.bold, shell.underline, shell.red)
		if mail_level >= self._mail_level:
			self._mail_client.send_message("Logger", message)
		self._logger.critical(message)

	def shutdown(self):
		if self.self_debug:
			self.debug("eupy.native.logger._Logger.shutdown()")
		logging.shutdown()
		return

_logger = None

def initLogger(name, lvl = INFO, mail: client = None, colorize = False, step = False, self_debug = False):
	global _logger
	_logger = _Logger(name, lvl, client, colorize, step, self_debug)
	if _logger.self_debug:
		_logger.debug("eupy.native.logger.initLogger()")
	return _logger

def getLogger():
	global _logger
	if _logger == None:
		raise NameError("Logger has not been initialized!")
	else:
		if _logger.self_debug:
			_logger.debug("eupy.native.logger.getLogger()")
		return _logger

def initOrGetLogger(name = "", lvl = INFO, mail: client = None, colorize = False, step = False, self_debug = False):
	global _logger
	if _logger == None:
		logging.warning("Logger has not been explicitly initialized")
		_logger = _Logger(name, lvl, client, colorize, step, self_debug)
		if _logger.self_debug:
			_logger.debug("eupy.native.logger.initOrGetLogger()")
		return _logger
	else:
		if _logger.self_debug:
			_logger.debug("eupy.native.logger.initOrGetLogger()")
		return _logger
