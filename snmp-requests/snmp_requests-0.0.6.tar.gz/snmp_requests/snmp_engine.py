
from subprocess import run, PIPE
import re




class snmp_engine():

    def __init__(self, version, security, ip_addr, port):

        # Version
        self.options = ["-v", version, "-Oben"]

        # Security settings
        if (version == '1') or (version == '2c') :
            self.options = self.options + ["-c", security]

        elif (version == '3'):

            try:
                self.options = self.options + ["-c", security['username'], "-l", security['level']]

                if (security['level'] == 'authNoPriv') or (security['level'] == 'authPriv'):
                    self.options = self.options + ["-A", security['authKey']]

                    if 'authAlg' in security.keys():
                        self.options = self.options + ["-a", security['authAlg']]

                if (security['level'] == 'authPriv'):
                    self.options = self.options + ["-X", security['privKey']]

                    if 'privAlg' in security.keys():
                        self.options = self.options + ["-x", security['privAlg']]

            except:
                print("Error en la configuracion de la seguridad en SNMPv3")


        # Add host
        self.options = self.options + [ip_addr + ":" + str(port) ]


    def procesa_resp(self, aux):

        aux = aux.split(" = ")
        oid = aux[0]
        type = ''
        val = ''

        if 'No Such Instance' in aux[1]:
            type = 'NoSuchInstance'
        elif 'No Such Object' in aux[1]:
            type = 'NoSuchObject'
        elif 'No more variables left in this MIB View' in aux[1]:
            type = 'EndOfMib'
        else:
            aux = aux[1].split(": ")
            type = aux[0]

            if type == "STRING":
                aux2 = aux[1].split("\"")
                val = aux2[1]
            elif type == "Timeticks":
                aux2 = aux[1].split("(")[1]
                val = aux2.split(")")[0]
            else:
                val = aux[1]

        return oid, type, val


    def snmpget(self, varBinds):

        cmd = ["snmpget"] + self.options
        for varBind in varBinds:
            cmd = cmd + [str(varBind[0])]

        resp = run(cmd, stdout=PIPE, stderr=PIPE)

        v = []
        for varBind in resp.stdout.decode('utf-8').split('\n')[:-1]:
            oid_resp, type2_resp, val_resp = self.procesa_resp(varBind)
            v.append([oid_resp, (type2_resp, val_resp)])
        return v



    def snmpgetnext(self, varBinds):

        cmd = ["snmpgetnext"] + self.options
        for varBind in varBinds:
            cmd = cmd + [str(varBind[0])]

        resp = run(cmd, stdout=PIPE, stderr=PIPE)

        v = []
        for varBind in resp.stdout.decode('utf-8').split('\n')[:-1]:
            oid_resp, type2_resp, val_resp = self.procesa_resp(varBind)
            v.append([oid_resp, (type2_resp, val_resp)])
        return v


    def snmpset(self, varBinds):

        cmd = ["snmpset"] + self.options
        for varBind in varBinds:
            if varBind[1][0] == 'INTEGER':
                cmd = cmd + [str(varBind[0]), 'i', str(varBind[1][1])]
            elif varBind[1][0] == 'hexValue':
                cmd = cmd + [str(varBind[0]), 'x', str(varBind[1][1])]
            elif varBind[1][0] == 'STRING':
                cmd = cmd + [str(varBind[0]), 's', str(varBind[1][1])]
            elif varBind[1][0] == 'OID':
                cmd = cmd + [str(varBind[0]), 'o', str(varBind[1][1])]
            else:
                print("Unknown data type")

        resp = run(cmd, stdout=PIPE, stderr=PIPE)

        v = []
        for varBind in resp.stdout.decode('utf-8').split('\n')[:-1]:
            oid_resp, type2_resp, val_resp = self.procesa_resp(varBind)
            v.append([oid_resp, (type2_resp, val_resp)])
        return v


    def snmpbulk(self, nonRepeaters, maxRepetitions, varBinds):

        cmd = ["snmpbulkget", "-B", nonRepeaters, maxRepetitions] + self.options
        for varBind in varBinds:
            cmd = cmd + [str(varBind[0])]

        resp = run(cmd, stdout=PIPE, stderr=PIPE)

        v = []
        for varBind in resp.stdout.decode('utf-8').split('\n')[:-1]:
            oid_resp, type2_resp, val_resp = self.procesa_resp(varBind)
            v.append([oid_resp, (type2_resp, val_resp)])
        return v


    def snmpwalk(self, oid):

        cmd = ["snmpwalk"] + self.options
        cmd = cmd + [oid]

        resp = run(cmd, stdout=PIPE, stderr=PIPE)

        v = []
        for varBind in resp.stdout.decode('utf-8').split('\n')[:-1]:
            oid_resp, type2_resp, val_resp = self.procesa_resp(varBind)
            v.append([oid_resp, (type2_resp, val_resp)])
        return v


class tools():

    def var_type(self, var):
        s = str(type(var))
        ss = re.findall(r"'(.*?)'",s)[0]
        if '.' not in ss:
            return ss
        else:
            return ss.rsplit('.', 1)[-1]

