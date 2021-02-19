from zeroconf import ServiceBrowser, Zeroconf
import socket

class MyListener:

    def __init__(self):
        self.names = set()

    def __show(self, action, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        short_name = name[:name.index('.')]
        ip = "1.1.1.1"
        try:
            ip = socket.inet_ntoa(info.addresses[0])
        except IndexError:
            pass
        uid = str(info.properties.get(b'uid', 'unknown:uid:'+short_name))
        self.names.add(short_name)
        print(f"{action:10} {short_name:8} {str(self.names):50} {ip:15} {uid}")

    def add_service(self, zeroconf, type, name):
        self.__show("Add", zeroconf, type, name)

    def update_service(self, zeroconf, type, name):
        self.__show("Update", zeroconf, type, name)

    def remove_service(self, zeroconf, type, name):
        short_name = name[:name.index('.')]
        self.names.remove(short_name)
        action = "Remove"
        print(f"{action:10} {short_name:8} {str(self.names):50}")


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, type_="_repl._tcp.local.", handlers=listener)

try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()