""" Tools for reading, manipulating, and writing alias files """


import xml.etree.ElementTree as ET
import re


__all__ = ["AliasCommands", "load", "loads"]


class AliasCommands:
    """ Store/manipulate alias commands """

    def __init__(self):
        self.aliases = {}

    def __repr__(self):
        return f"AliasCommands({self.aliases})"

    def __setitem__(self, command, action):
        # Regex match
        new_command = str(command).strip()
        match = re.fullmatch(r"\.?([^\s;\.]+)", new_command)
        if not match:
            # Raise if `command` is invalid
            raise ValueError("invalid alias command " + repr(new_command))
        self.aliases["."+match.group(1)] = str(action)

    def __getitem__(self, command):
        try:
            return self.aliases[command]
        except KeyError:
            raise KeyError(repr(command) + " is not an existing or valid alias command")

    def __delitem__(self, command):
        try:
            del self.aliases[command]
        except KeyError:
            raise KeyError(repr(command) + " is not an existing or valid alias command")

    def items(self):
        return self.aliases.items()

    def keys(self):
        return self.aliases.keys()

    def values(self):
        return self.aliases.values()

    def dump(self, file_obj, client):
        """ Writes AliasCommands to passed-in file-like object """
        file_obj.write(self.dumps(client))

    def dumps(self, client):
        """ Returns a string in either the VRC txt or vSTARS/vERAM xml format """
        if client.lower() == "vrc":
            # Write to '.txt' format (VRC)
            output = ""
            for cmd, act in self.aliases.items():
                output += f"{cmd} {act}\n"
            return output
        elif client.lower() in ("vstars", "veram"):
            # Write to '.xml' format (vSTARS & vERAM)
            root = self._dumpxml()
            # (ET.indent only works in Python 3.9+)
            try:
                ET.indent(root)
            except:
                pass
            return ET.tostring(root, encoding="unicode")
        else:
            raise ValueError("unknown client " + repr(client))

    def _dumpxml(self):
        """ Returns an xml.etree.ElementTree Element object """
        root = ET.Element("CommandAliases")
        for cmd, act in self.aliases.items():
            ET.SubElement(root, "CommandAlias", attrib={"Command":cmd,"ReplaceWith":act})
        return root


def load(file_obj):
    """ Makes AliasCommands from an open file-like object """
    return loads(file_obj.read())

def loads(text):
    """ Makes AliasCommands from a string """
    if text.strip().startswith("<"):
        # load xml
        root = ET.fromstring(text)
        ac = AliasCommands()
        for node in root.findall("CommandAlias"):
            try:
                # Use `attrib[...]` instead of `get(...)` to catch errors
                ac[node.attrib["Command"]] = node.attrib["ReplaceWith"]
            except KeyError as e:
                raise ET.ParseError(f"{e} attrib not found")
        return ac
    else:
        # load txt (VRC)
        ac = AliasCommands()
        matches = re.finditer(r"^\.(\w+) ([^;\n]+)", text, flags=re.MULTILINE)
        # Check if none were found
        if not matches:
            raise ValueError("no alias commands were found")
        for match in matches:
            ac[match.group(1)] = match.group(2)
        return ac
