import socket
from pythonping import ping
import os

def ip(ipuser, port):
	socket.gethostbyname(socket.gethostname())
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((ipuser,port))
	print(s.getsockname()[0])
	s.close()

def ping(pingip):
	hostname = pingip
	response = os.system("ping -c 1 " + hostname)

	if response == 0:
	  print(hostname, 'is up!')
	else:
	  print(hostname, 'is down!')

def help():
	print("To get an ip address, you need to register one line of code:\ngetip.ip(site.address, port)")
	print("My github: tikotstudio. Repository this project: https://github.com/tikotstudio/getip")
	print("For ping ip or url you need to use ping(ip or url) function.")