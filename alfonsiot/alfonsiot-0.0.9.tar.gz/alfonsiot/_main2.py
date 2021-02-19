import socket
import json
import os
import string
import random
import time
import sys
import argparse
import paho.mqtt.client
import yaml
import inspect

LOCAL_USE = True

projectPath = ""
config = {"uninitialized": True}
data = {}
mqtt = paho.mqtt.client.Client()

def _getIP():
	ip = getConfig("ip")
	if ip: return ip

	discoverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	discoverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	discoverSocket.settimeout(1)

	msg = None

	startSearchTime = time.time()

	while not msg:
		discoverSocket.sendto(b"discover", ("255.255.255.255", 27369))

		try:
			msg = discoverSocket.recv(1024)
		except socket.timeout:
			if startSearchTime + 30 < time.time(): raise socket.timeout()

	discoverData = json.loads(msg.decode("utf-8"))
	newIP = discoverData["domain"] if "domain" in discoverData else discoverData["ext_ip"] if "ext_ip" in discoverData and not LOCAL_USE else discoverData["ip"]
	config["ip"] = newIP
	return newIP

def _getID():
	return getConfig("id")

def getConfig(key):
	if key in config:
		return config[key]

	if key in data:
		return data[key]

	return None

def setup(configPath=None):
	global config

	if configPath == None:
		frm = inspect.stack()[-1]
		mod = inspect.getmodule(frm[0])
		configPath = os.path.dirname(os.path.realpath(mod.__file__)) + "/iot-config.yaml"

	with open(configPath) as f:
		config = yaml.safe_load(f)



def __console():
	parser = argparse.ArgumentParser("alfonsiot")
	parser.add_argument("config", default=os.getcwd() + "/iot-config.yaml", nargs="?", help="the config file, defaults to [cwd]/iot-config.yaml")
	args = parser.parse_args()

	setup(args.config)

if __name__ == "__main__":
	print("21")
	__console()
