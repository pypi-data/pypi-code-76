#!/usr/bin/env python
import logging
from eupy.native import shell

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

	def __init__(self, name, level, colorize, step, self_debug):
		self._colorize = colorize
		self._step = step
		self._self_debug = self_debug
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
	def debug(self, message, step = False):
		if self._colorize:
			message = shell.output(message, shell.bold, shell.green)
		self._logger.debug(message)
		if self._logger.level == DEBUG and (self._step or step):
			try:
				input()
			except EOFError as e:
				self.warning(e)

	def info(self, message):
		if self._colorize:
			message = shell.output(message, shell.bold, shell.cyan)
		self._logger.info(message)

	def warning(self, message):
		if self._colorize:
			message = shell.output(message, shell.bold, shell.yellow)
		self._logger.warning(message)

	def warn(self, message):
		if self._colorize:
			message = shell.output(message, shell.bold, shell.yellow)
		self._logger.warn(message)

	def error(self, message):
		if self._colorize:
			message = shell.output(message, shell.bold, shell.red)
		self._logger.error(message)
	
	def critical(self, message):
		if self._colorize:
			message = shell.output(message, shell.bold, shell.underline, shell.red)
		self._logger.critical(message)

	def shutdown(self):
		if self.self_debug:
			self.debug("eupy.native.logger._Logger.shutdown()")
		logging.shutdown()
		return

_logger = None

def initLogger(name, lvl = INFO, colorize = False, step = False, self_debug = False):
	global _logger
	_logger = _Logger(name, lvl, colorize, step, self_debug)
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

def initOrGetLogger(name = "", lvl = INFO, colorize = False, step = False, self_debug = False):
	global _logger
	if _logger == None:
		logging.warning("Logger has not been explicitly initialized")
		_logger = _Logger(name, lvl, colorize, step, self_debug)
		if _logger.self_debug:
			_logger.debug("eupy.native.logger.initOrGetLogger()")
		return _logger
	else:
		if _logger.self_debug:
			_logger.debug("eupy.native.logger.initOrGetLogger()")
		return _logger
