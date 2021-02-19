import alfonsiot
import sys
import time
import logging
import argparse
import os
import threading

CONFIG_PATH = os.path.expanduser("~/.alfons-cli/")

def readProfile(name):
	keys = ["server", "user", "password", "topic", "message"]

	def _parseProfile(lines):
		for line in lines:
			if not "=" in line:
				continue

			l = line.strip().split("=", 1)

			if len(l) < 2:
				continue

			key = l[0]
			value = l[1]

			if len(key) < 1 and len(value) < 1:
				continue

			if key not in keys:
				continue

			yield (key, value)

	# Make sure the profiles directory exists - make it if it doesn't
	if not os.path.exists(os.path.join(CONFIG_PATH, "profiles")):
		os.makedirs(os.path.join(CONFIG_PATH, "profiles"))
	
	profilePath = os.path.join(CONFIG_PATH, "profiles", name + ".conf")
	
	if os.path.exists(profilePath):
		with open(profilePath) as f:
			return {k:v for k,v in _parseProfile(f.readlines())}
	else:
		return {}

def main():
	parser = argparse.ArgumentParser()
	
	parser.add_argument("-p", "--profile", default="default")
	parser.add_argument("-s", "--server", nargs="?")
	parser.add_argument("-u", "--user", nargs="?")
	parser.add_argument("-pw", "--password", nargs="?")
	parser.add_argument("-t", "--topic", nargs="?")
	parser.add_argument("-m", "--message", nargs="?")
	parser.add_argument("-c", "--continuous", action="store_true")

	parserArgs = vars(parser.parse_args())
	
	arguments = readProfile(parserArgs["profile"])
	del parserArgs["profile"]
	
	requiredArgs = ["server", "topic"]

	for a in parserArgs:
		if parserArgs[a] != None or a not in arguments:
			arguments[a] = parserArgs[a]

		if a in requiredArgs and arguments[a] == None:
			print("Argument '" + a + "' is set neither as an argument or in the selected profile")
			return 1

	host, port = arguments["server"].split(":", 1)
	username = arguments["user"]
	password = arguments["password"]
	topic = arguments["topic"]
	message = arguments["message"]
	
	if arguments["continuous"]:
		print("In continuous mode... quit with KeyboardInterrupt")

	logging.info("Connecting...")
	iot = alfonsiot.start(host=host, port=port, username=username, password=password)
	
	def _onConnect(iot):
		print("Connected! ", end="")

		def _onSubMessage(payload):
			print("Received message on the topic:\n\t", payload)
			
			if not arguments["continuous"]:
				lock.release()
		
		iot.subscribe(topic, _onSubMessage)
		
		if message != None:
			print("Publishing...")
			iot.publish(topic, message)
		else:
			print("No message, just subscribing...")

	iot.onConnect = _onConnect

	try:
		lock = threading.Lock()
		lock.acquire()
		lock.acquire()
	except KeyboardInterrupt:
		pass

