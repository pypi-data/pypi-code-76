from suds.client import Client
import json

name = "nc_dns"
class nc_client(object):
    endpoint = "https://www.servercontrolpanel.de:443/WSEndUser?wsdl"
    client = Client(endpoint)

    def getVServer(self):
        return json.dumps(self.client.service.getVServers(self.__customer, self.__api_password))
    
    def getVServerState(self, server):
        return json.dumps(self.client.service.getVServerState(self.__customer, self.__api_password, server))

    def getVServerNickname(self, server):
        return json.dumps(self.client.service.getVServerNickname(self.__customer, self.__api_password, server))
        
    def getVServerIPs(self, server):
        return json.dumps(self.client.service.getVServerIPs(self.__customer, self.__api_password, server))

    def getVServerUptime(self, server):
        return json.dumps(self.client.service.getVServerUptime(self.__customer, self.__api_password, server))

    def getVServerInformation(self, server):
        return (self.client.service.getVServerInformation(self.__customer, self.__api_password, server))      

    def __init__(self, customer, api_password):
        self.__customer = customer
        self.__api_password = api_password