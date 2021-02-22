#!/usr/bin/env python

PURPLE = "\033[95m"
CYAN = "\033[96m"
DARKCYAN = "\033[36m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END = "\033[0m"

def purple(string, callback = None):
	if callback:
		string = callback[0](string, callback = [x for x in callback if x != callback[0]])
	return "{}{}{}".format(PURPLE, string, END)

def cyan(string, callback = None):
	if callback:
		string = callback[0](string, callback = [x for x in callback if x != callback[0]])
	return "{}{}{}".format(CYAN, string, END)

def darkcyan(string, callback = None):
	if callback:
		string = callback[0](string, callback = [x for x in callback if x != callback[0]])
	return "{}{}{}".format(DARKCYAN, string, END)

def blue(string, callback = None):
	if callback:
		string = callback[0](string, callback = [x for x in callback if x != callback[0]])
	return "{}{}{}".format(BLUE, string, END)

def green(string, callback = None):
	if callback:
		string = callback[0](string, callback = [x for x in callback if x != callback[0]])
	return "{}{}{}".format(GREEN, string, END)

def yellow(string, callback = None):
	if callback:
		string = callback[0](string, callback = [x for x in callback if x != callback[0]])
	return "{}{}{}".format(YELLOW, string, END)

def red(string, callback = None):
	if callback:
		string = callback[0](string, callback = [x for x in callback if x != callback[0]])
	return "{}{}{}".format(RED, string, END)

def bold(string, callback = None):
	if callback:
		string = callback[0](string, callback = [x for x in callback if x != callback[0]])
	return "{}{}{}".format(BOLD, string, END)

def underline(string, callback = None):
	if callback:
		string = callback[0](string, callback = [x for x in callback if x != callback[0]])
	return "{}{}{}".format(UNDERLINE, string, END)

def output(string, *args):
	if args:
		string = args[0](string, callback = [x for x in args if x != args[0]])
	return string
