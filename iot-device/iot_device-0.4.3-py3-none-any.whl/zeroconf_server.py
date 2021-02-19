from zeroconf import ServiceInfo, Zeroconf
import socket

deviceUID  = "12:ad:93"
deviceName = "myesp32"
deviceDesc = { 
    "uid": deviceUID, 
    "deviceName": deviceName }
deviceType = "_repl"
deviceIP = "192.168.1.55"
devicePort = 50123

print(socket.inet_aton(deviceIP))

info = ServiceInfo(
    type_=deviceType + "._tcp.local.",
    name=deviceName + "." + deviceType +"._tcp.local.",
    port=devicePort, 
    weight=0, 
    priority=0,
    properties=deviceDesc, 
    server=deviceName + ".local.",
    addresses=[socket.inet_aton(deviceIP)])

zeroconf = Zeroconf()

import time
for i in range(1000):
    zeroconf.register_service(info)
    time.sleep(5)
    zeroconf.unregister_service(info)
    time.sleep(3)

print("DONE")