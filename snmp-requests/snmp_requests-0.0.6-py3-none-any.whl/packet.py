
from pysnmp.hlapi import *
from pysnmp.smi import exval
import re


class response (object):

    def __init__(self, errorIndication, errorStatus, errorIndex, varBinds):
        self.errorIndication = errorIndication
        self.errorStatus = errorStatus
        self.errorIndex = errorIndex
        self.varBinds = varBinds

    def pretty_print(self):
        if self.errorIndication:
            print(self.errorIndication)
        elif self.errorStatus:
            print(self.errorStatus)
            print(self.errorIndex)
        else:
            for varBind in self.varBinds:
                print(tools().var_type(varBind[0]) + ' : ' + str(varBind[0]))
                print(tools().var_type(varBind[1]) + ' : ' + str(varBind[1]))


def get_alg(alg):

    # Available authentication protocols
    if alg == "usmHMACMD5AuthProtocol":
        return usmHMACMD5AuthProtocol
    elif alg == "usmHMACSHAAuthProtocol":
        return usmHMACSHAAuthProtocol
    elif alg == "usmHMAC128SHA224AuthProtocol":
        return usmHMAC128SHA224AuthProtocol
    elif alg == "usmHMAC192SHA256AuthProtocol":
        return usmHMAC192SHA256AuthProtocol
    elif alg == "usmHMAC256SHA384AuthProtocol":
        return usmHMAC256SHA384AuthProtocol
    elif alg == "usmHMAC384SHA512AuthProtocol":
        return usmHMAC384SHA512AuthProtocol
    elif alg == "usmNoAuthProtocol":
        return usmNoAuthProtocol



    #Available privacy protocols
    elif alg == "usmDESPrivProtocol":
        return usmDESPrivProtocol
    elif alg == "usm3DESEDEPrivProtocol":
        return usm3DESEDEPrivProtocol
    elif alg == "usmAesCfb128Protocol":
        return usmAesCfb128Protocol
    elif alg == "usmAesCfb192Protocol":
        return usmAesCfb192Protocol
    elif alg == "usmAesCfb256Protocol":
        return usmAesCfb256Protocol
    elif alg == "usmNoPrivProtocol":
        return usmNoPrivProtocol

    else:
        print("Unsupported algorithm")
        return None





class snmp_engine():

    def __init__(self, version, security, ip_addr, port):

        if (version == 'v1'):
            self.security = CommunityData(security, mpModel=0)

        elif (version == 'v2c'):
            self.security = CommunityData(security)

        elif (version == 'v3'):

            if not(False in [(key in security.keys()) for key in ['username', 'authKey', 'authAlg', 'privKey', 'privAlg']]):
                self.security = UsmUserData(security['username'], security['authKey'], security['privKey'],
                            authProtocol=get_alg(security['authAlg']),
                            privProtocol=get_alg(security['privAlg']))
            elif not(False in [(key in security.keys()) for key in ['username', 'authKey', 'authAlg', 'privKey']]):
                self.security = UsmUserData(security['username'], security['authKey'], security['privKey'],
                                            authProtocol=get_alg(security['authAlg']))
            elif not(False in [(key in security.keys()) for key in ['username', 'authKey', 'privKey', 'privAlg']]):
                self.security = UsmUserData(security['username'], security['authKey'], security['privKey'],
                                            privProtocol=get_alg(security['privAlg']))
            elif not(False in [(key in security.keys()) for key in ['username', 'authKey', 'authAlg']]):
                self.security = UsmUserData(security['username'], security['authKey'], security['privKey'])
            elif not(False in [(key in security.keys()) for key in ['username', 'authKey']]):
                self.security = UsmUserData(security['username'], security['authKey'])
            elif not(False in [(key in security.keys()) for key in ['username']]):
                self.security = UsmUserData(security['username'])
            else:
                print("not supported config")

        self.transport = UdpTransportTarget((ip_addr, port))


    def parse_varBinds(self, varBinds):

        v = []
        for varBind in varBinds:

            if varBind[1] == None:
                v.append(ObjectType(ObjectIdentity(varBind[0])))

            else:
                if varBind[1][0] == "INTEGER":
                    v.append((ObjectIdentifier(varBind[0]),
                                     Integer(int(varBind[1][1]))))
                elif varBind[1][0] == "Timeticks":
                    v.append((ObjectIdentifier(varBind[0]),
                                     TimeTicks(int(varBind[1][1]))))
                elif varBind[1][0] == "Counter32":
                    v.append((ObjectIdentifier(varBind[0]),
                                     Counter32(int(varBind[1][1]))))
                elif varBind[1][0] == "OctetString":
                    v.append((ObjectIdentifier(varBind[0]),
                                     OctetString(str(varBind[1][1]))))
                elif varBind[1][0] == "OID":
                    v.append((ObjectIdentifier(varBind[0]),
                                     ObjectIdentifier(str(varBind[1][1]))))
                elif varBind[1][0] == "hexValue":
                    v.append((ObjectIdentifier(varBind[0]),
                                     OctetString(hexValue=str(varBind[1][1]))))
                else:
                    v.append((ObjectIdentifier(varBind[0]),
                                     OctetString(str(varBind[1][1]))))
        return v


    def snmpget(self, varBinds):

        varBinds = self.parse_varBinds(varBinds)
        iterator = getCmd(SnmpEngine(), self.security, self.transport, ContextData(), *varBinds)
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        resp = response(errorIndication, errorStatus, errorIndex, varBinds)
        return resp


    def snmpgetnext(self, varBinds):

        varBinds = self.parse_varBinds(varBinds)
        iterator = nextCmd(SnmpEngine(), self.security, self.transport, ContextData(), *varBinds)
        try:
            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
            resp = response(errorIndication, errorStatus, errorIndex, varBinds)
        except StopIteration:
            varBinds = [(ObjectIdentifier(varBinds[0][0]), exval.endOfMibView)]
            resp = response(0, 0, 0, varBinds)
        return resp


    def snmpset(self, varBinds):

        varBinds = self.parse_varBinds(varBinds)
        iterator = setCmd(SnmpEngine(), self.security, self.transport, ContextData(), *varBinds)
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        resp = response(errorIndication, errorStatus, errorIndex, varBinds)
        return resp


    def snmpbulk(self, nonRepeaters, maxRepetitions, varBinds):

        varBinds = self.parse_varBinds(varBinds)
        iterator = bulkCmd(SnmpEngine(), self.security, self.transport, ContextData(), nonRepeaters, maxRepetitions *varBinds)
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        resp = response(errorIndication, errorStatus, errorIndex, varBinds)
        return resp


    def snmpwalk(self, oid):

        varBinds = [[oid, None]]
        varBinds = self.parse_varBinds(varBinds)
        iterator = nextCmd(SnmpEngine(), self.security, self.transport, ContextData(), *varBinds)

        r = []
        for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            r.append(varBinds[0])

        return r


class tools():

    def var_type(self, var):
        s = str(type(var))
        ss = re.findall(r"'(.*?)'",s)[0]
        if '.' not in ss:
            return ss
        else:
            return ss.rsplit('.', 1)[-1]

