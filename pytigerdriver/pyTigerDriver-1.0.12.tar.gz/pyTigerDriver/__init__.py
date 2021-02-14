# -*- coding: utf-8 -*-

from .misc import ExceptionAuth
from .pyDriver import GSQL_Client, ExceptionRecursiveRet, ExceptionCodeRet, REST_Client, REST_ClientError


class Client():
    def __init__(self, server_ip="127.0.0.1", username="tigergraph", password="tigergraph",local=False, cacert=""
                 , version="3.0.5", commit="", restPort="9000", gsPort="14240", protocol="https"
                 , graph="MyGraph", token=""):
        sslCert = ""
        self.cacert = cacert
        if self.cacert == "":
            from os.path import expanduser
            self.cacert = expanduser("~") + "/tg.cer"
        if protocol == "https":
            try:
                import ssl
                sslhost = server_ip.split(":")[0]
                sslCert = ssl.get_server_certificate((sslhost, 443))
            except:
                raise Exception("Error getting the certificate !")
        cert = open(self.cacert, "w")
        cert.writelines(sslCert)
        cert.close()
        self.Rest = REST_Client(server_ip=server_ip, protocol=protocol, restPort=restPort, token=token
                                , username=username, password=password, cacert=self.cacert)
        self.Gsql = GSQL_Client(server_ip=server_ip, username=username, password=password,local=local, cacert=self.cacert
                                , version=version, commit=commit, graph=graph, gsPort=gsPort, protocol=protocol)

    def setToken(self,token=""):
        self.Gsql.setToken(token)
        self.Rest.setToken(token)
