import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s
import numpy as np
import re

from .LocalIdentifiersManager import LocalIdentifiersManager
from .IdentifierUtil import IdentifierUtil
from ..InfoParser import InfoParser

class InfoFileLoader(object):

    def __init__(self, node = None, client_obj = None):
        if node is None:
            self._node = RRN
        else:
            self._node = node
        self._client_obj = client_obj

        self._info_parser = InfoParser(self._node,self._client_obj)
        self._id_manager = LocalIdentifiersManager(self._node,self._client_obj)
        self._id_util = IdentifierUtil(self._node,self._client_obj)

    def _load_device_identifier(self, info_file, category):
        
        if hasattr(info_file,"device_info"):
            if info_file is not None and info_file.device_info is not None and info_file.device_info.device is not None \
                and not self._id_util.IsIdentifierAnyName(info_file.device_info.device) and \
                self._id_util.IsIdentifierAnyUuid(info_file.device_info.device):

                dev_id, lock_fd = self._id_manager.GetIdentifierForNameAndLock(category, info_file.device_info.device.name)
                info_file.device_info.device = dev_id
                return True, dev_id,lock_fd
            return False, None, None
        elif hasattr(info_file,"device"):
            if info_file is not None and info_file.device \
                and not self._id_util.IsIdentifierAnyName(info_file.device) and \
                self._id_util.IsIdentifierAnyUuid(info_file.device):

                dev_id, lock_fd = self._id_manager.GetIdentifierForNameAndLock(category, info_file.device.name)
                info_file.device = dev_id
                return True, dev_id,lock_fd
            return False, None, None
        return False, None, None

    def LoadInfoFileFromString(self, info_text, info_type_name, category = "unspecified"):
        info = self._info_parser.ParseInfoString(info_text, info_type_name)
        _, _, fds = self._load_device_identifier(info,category)
        return info, fds

    def LoadInfoFile(self, file_name, info_type_name, category = "unspecified"):
        info = self._info_parser.ParseInfoFile(file_name, info_type_name)
        _, _, fds = self._load_device_identifier(info,category)
        return info, fds