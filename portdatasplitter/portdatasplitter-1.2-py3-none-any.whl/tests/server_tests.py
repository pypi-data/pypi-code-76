from portdataspitter.portdatasplitter import PortDataSplitter


server = PortDataSplitter('0.0.0.0', 2290, port_name='/dev/ttyUSB0')
ports = server.get_all_connected_devices()

for port in ports:
    server = PortDataSplitter('0.0.0.0', 2290, port_name=port)
    server.start()