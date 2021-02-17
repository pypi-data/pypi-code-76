import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s
import numpy as np
import re

from .UuidUtil import UuidUtil

class IdentifierUtil(object):

    def __init__(self, node = None, client_obj = None):
        if node is None:
            self._node = RRN
        else:
            self._node = node
        self._client_obj = client_obj

        self._identifier = node.GetStructureType("com.robotraconteur.identifier.Identifier", self._client_obj)
        self._uuid_dt = node.GetNamedArrayDType("com.robotraconteur.uuid.UUID", self._client_obj)

        self._uuid_util = UuidUtil(node,client_obj)

    def IsIdentifierAnyUuid(self,identifier):
        if identifier is None or identifier.uuid is None:
            return True
        return np.all(identifier.uuid["uuid_bytes"] == 0)

    def IsIdentifierAnyName(self,identifier):
        if identifier is None or identifier.name is None:
            return True
        return len(identifier.name) == 0

    def IsIdentifierAny(self,identifier):
        if identifier is None:
            return True
        if not self.IsIdentifierAnyUuid(identifier):
            return False
        if not self.IsIdentifierAnyName(identifier):
            return False
        return True

    def IsIdentifierMatch(self, expected, test):
        if self.IsIdentifierAny(expected) or self.IsIdentifierAny(test):
            return True
        
        name_match = False
        uuid_match = False

        if self.IsIdentifierAnyName(expected) or self.IsIdentifierAnyName(test):
            name_match = True
        else:
            if expected.name == test.name:
                name_match = True

        if self.IsIdentifierAnyUuid(expected) or self.IsIdentifierAnyUuid(test):
            uuid_match = True
        else:
            if np.all(expected.uuid["uuid_bytes"] == test.uuid["uuid_bytes"]):
                uuid_match = True

        return name_match and uuid_match

    def CreateIdentifier(self,name,uuid):
        ret = self._identifier()        
        ret.name = name if name is not None else ""
        if uuid is not None:
            ret.uuid = self._uuid_util.ParseUuid(uuid)
        else:
            ret.uuid = np.zeros((1,),dtype=self._uuid_dt)
        return ret

    def CreateIdentifierFromName(self,name):
        assert name is not None
        ret = self._identifier()        
        ret.name = name        
        ret.uuid = np.zeros((1,),dtype=self._uuid_dt)
        return ret

    def IdentifierToString(self,identifier):
        if identifier is None:
            return ""
        if not self.IsIdentifierAnyName(identifier) and not self.IsIdentifierAnyUuid(identifier):
            return identifier.name + "|" + self._uuid_util.UuidToString(identifier.uuid)
        if not self.IsIdentifierAny(identifier):
            return identifier.name
        if not self.IsIdentifierAnyUuid(identifier):
            return identifier.uuid
        return ""

    def StringToIdentifier(self, string_id):
        name_regex_str = "(?:[a-zA-Z](?:[a-zA-Z0-9_]*[a-zA-Z0-9])?)(?:\\.[a-zA-Z](?:[a-zA-Z0-9_]*[a-zA-Z0-9])?)*"
        uuid_regex_str = "\\{?[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}\\}?"
        identifier_regex = "(?:(" + name_regex_str + ")\\|(" + uuid_regex_str + "))|(" + name_regex_str + ")|(" + uuid_regex_str + ")"

        r_res = re.match(identifier_regex, string_id)
        if r_res is None:
            raise RR.InvalidArgumentException("Invalid identifier string")

        if r_res.group(1) is not None and r_res.group(2) is not None:
            return self.CreateIdentifier(r_res.group(1), r_res.group(2))
        
        if r_res.group(3) is not None:
            return self.CreateIdentifierFromName(r_res.group(3))

        if r_res.group(4) is not None:
            return self.CreateIdentifier("", r_res.group(4))

        raise RR.InvalidArgumentException("Invalid identifier string")




        

        