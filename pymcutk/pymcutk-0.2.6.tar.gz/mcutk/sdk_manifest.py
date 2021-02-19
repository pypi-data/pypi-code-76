import logging
import os
import glob
from xml.etree import ElementTree as ET
from distutils.version import LooseVersion


class SDKManifest(object):
    """NXP MCUXpresso SDK Manifest Parser."""

    @classmethod
    def find(cls, root_dir):
        manifestfilelist = glob.glob("{0}/*_manifest*.xml".format(root_dir))
        manifests = list()
        for per_file in manifestfilelist:
            manifest_obj = cls(per_file)
            if manifest_obj:
                manifests.append(manifest_obj)

        return manifests

    @classmethod
    def find_max_version(cls, root_dir):
        """Load latest version of manifest from directory."""
        manifests = SDKManifest.find(root_dir)
        if not manifests:
            return None
        return sorted(manifests, key=lambda m: LooseVersion(m.manifest_version))[-1]

    def __init__(self, filepath):
        self._filepath = filepath
        self._xmlroot = ET.parse(filepath).getroot()
        self._sdk_root = os.path.dirname(filepath)
        self._id = self._xmlroot.attrib['id']
        self._manifest_version = self._xmlroot.attrib['format_version']
        self._sdk_name = self._xmlroot.attrib["id"]
        self._sdk_version = self._xmlroot.find('./ksdk').attrib['version']

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    @property
    def filepath(self):
        return self._filepath

    @property
    def id(self):
        return self._id

    @property
    def sdk_version(self):
        return self._sdk_version

    @property
    def sdk_name(self):
        return self._sdk_name

    @property
    def format_version(self):
         return self._manifest_version

    @property
    def manifest_version(self):
        return self._manifest_version

    @property
    def sdk_root(self):
        return self._sdk_root

    @property
    def boards(self):
        xpath = './boards/board'
        nodes = self._xmlroot.findall(xpath)
        return [n.attrib['id'] for n in nodes]

    @property
    def toolchains(self):
        xpath = './toolchains/toolchain'
        nodes = self._xmlroot.findall(xpath)
        return [n.attrib['id'] for n in nodes]

    def find_example(self, example_id):
        """Return a dict which contain exmaple attributes.

        Keys:
            - id
            - name
            - toolchain
            - brief
            - category
            - path
        """
        xpath = './boards/board/examples/example[@id="{0}"]'.format(example_id)
        example_info = dict()
        node = self._xmlroot.find(xpath)
        if node is None:
            logging.debug("Cannot found example in manifest, id: %s", example_id)
            return

        example_info.update(node.attrib)
        xml_node = node.find('./external[@type="xml"]')
        xml_filename = xml_node.find('./files').attrib['mask']
        example_info['example.xml'] = xml_filename
        return example_info

    def dump_examples(self):
        """Return a list of examples.
        """
        xpath = './boards/board/examples/example'
        examples = list()
        for example_node in self._xmlroot.findall(xpath):
            examples.append({
                'toolchain': example_node.attrib['toolchain'].split(" "),
                'path': example_node.attrib['path'],
                'name': example_node.attrib['name']
            })
        return examples
