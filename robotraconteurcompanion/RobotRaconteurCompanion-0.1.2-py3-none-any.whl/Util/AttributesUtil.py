import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s
import numpy as np

from .IdentifierUtil import IdentifierUtil

class AttributesUtil(object):

    def __init__(self, node = None, client_obj = None):
        if node is None:
            self._node = RRN
        else:
            self._node = node
        self._client_obj = client_obj

        self._ident_util = IdentifierUtil(self._node, self._client_obj)

    def _try_add_identifier(self, o, name, id_):
        if not self._ident_util.IsIdentifierAny(id_):
            o[name] =  RR.VarValue(self._ident_util.IdentifierToString(id_),"string")
            return True
        return False

    def _try_add_string(self, o, name, str_):
        if str_ is not None and len(str_) > 0:
            o[name] = RR.VarValue(str_,"string")
            return True
        return False        
        
    def GetDefaultServiceAttributesFromDeviceInfo(self, device_info):
        o = dict()
        self._try_add_identifier(o,"device", device_info.device)
        self._try_add_identifier(o,"parent_device", device_info.parent_device)
        self._try_add_identifier(o,"manufacturer", device_info.manufacturer)
        self._try_add_identifier(o,"model", device_info.model)
        self._try_add_string(o,"serial_number",device_info.serial_number)
        self._try_add_string(o,"user_description",device_info.user_description)
        return o