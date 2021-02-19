import os
import zipfile
import logging
from xml.etree import cElementTree as ET
from mcutk.exceptions import CmsisPackIssue

LOGGER = logging.getLogger(__name__)

class CMSISPack(object):
    """This class represent a CMSIS DFP pack object.
    """
    def __init__(self, filepath):
        self._name = None
        self._pack_type = None
        self._version = None
        self._vendor = None
        self._devices = None
        self._boardname = ""
        self.path = filepath
        self._type = None
        self._pack_file = zipfile.ZipFile(filepath, mode='r')
        self._parse_pdsc(self._pack_file)

    def _parse_pdsc(self, packfile):
        files = packfile.namelist()
        pdsc = None
        for item in files:
            if item.endswith(".pdsc"):
                pdsc = item
                break

        if pdsc is None:
            raise CmsisPackIssue("fatal error: could not found .pdsc file in pack!")

        tree = ET.fromstring(packfile.read(pdsc))
        self._name = tree.find("name").text
        self._vendor = tree.find("vendor").text
        self._version = tree.find("releases/release").attrib["version"]
        self._type == "DFP" if "DFP" in self._name.upper() else "BSP"
        if self._type == 'DFP':
            self._dfp(tree)
        else:
            self._bsp(tree)

    def _dfp(self, tree):
        device_xpath = 'devices/family/device'
        linker_xpath = "components/component/files/file[@category='linkerScript']"

        # Device Definition Reference:
        # https://www.keil.com/pack/doc/CMSIS/Pack/html/pdsc_family_pg.html#element_memory

        devices = dict()
        for device_node in tree.findall(device_xpath):
            device_name = device_node.attrib["Dname"]
            device = {
                "name": device_name,
                "memory": list(),
                "algorithm": list(),
                "linker": list(),
                "partnumbers": list()
            }

            for mem_node in device_node.findall("memory"):
                device["memory"].append(mem_node.attrib)

            for algo_node in device_node.findall("algorithm"):
                algoinfo = algo_node.attrib
                device["algorithm"].append(algoinfo)

                # RAMstart & RAMsize: If not specified, require a RAM memory with default=1 attribute.
                if "RAMstart" not in algoinfo:
                    algoinfo["RAMstart_from_memory"] = "1"
                    for mem in device["memory"]:
                        if mem.get("default") == "1" and mem["access"] != "rx":
                            algoinfo["RAMstart"] = mem['start']
                            algoinfo["RAMsize"] = mem['size']
                            break

            for var_node in device_node.findall("variant"):
                device["partnumbers"].append(var_node.attrib["Dvariant"])

            for linker_node in tree.findall(linker_xpath):
                device["linker"].append(linker_node.attrib)

            devices[device_name] = device

        self._devices = devices

    def _bsp(self, tree):
        components = "components/component[@Cclass='Board Support']"
        node = tree.find(components)
        if node:
            self._boardname = node.attrib['Cvariant']

    @property
    def name(self):
        return self._name

    @property
    def vendor(self):
        return self._vendor

    @property
    def is_dfp(self):
        return "DFP" in self.name

    @property
    def version(self):
        return self._version

    @property
    def devicelist(self):
        return self._devices.keys()

    @property
    def boardname(self):
        return self._boardname

    @property
    def partnumbers(self):
        parts = list()
        for deviceinfo in self._devices.itervalues():
            parts.extend(deviceinfo["partnumbers"])
        return parts

    def has_partnumbers(self, name):
        for deviceinfo in self._devices.itervalues():
            if name in deviceinfo["partnumbers"]:
                return True
        return False

    def get_device_info_by_name(self, name):
        if not self.is_dfp:
            return None

        for deviceinfo in self._devices.itervalues():
            if name in deviceinfo["partnumbers"] or deviceinfo["name"] == name or  deviceinfo["name"] in name:
                return deviceinfo
        return None

    def validate_algorithm(self):
        if "DFP" not in self.name:
            return
        for device in self._devices.itervalues():
            if not device["algorithm"]:
                raise CmsisPackIssue("no algorithm found")

            for info in device["algorithm"]:
                name = info.get("name")
                if name not in self._pack_file.namelist():
                    raise CmsisPackIssue("Critical: Missing flash algorithm \"{0}\" in pack!".format(name))

    def validate_linker(self):
        if "DFP" not in self.name:
            return
        for device in self._devices.itervalues():
            if not device["linker"]:
                raise CmsisPackIssue("no linker information found")

            for info in device["linker"]:
                name = info.get("name")
                if name not in self._pack_file.namelist():
                    raise CmsisPackIssue("Critical: Missing linker script \"{0}\" in pack!".format(name))
