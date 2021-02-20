# -*- coding: utf-8 -*-

import os
import shutil
import json

from lxml import etree
from quick_data_clean.quick_algo import DataAlgo


class File(object):

    line_write_to_file = ""
    is_end_to_write = False
    read_binary_size = 0

    @classmethod
    def traversal_file_current_path(cls, path, file_suffix="*"):
        dirs = os.listdir(path)
        for file in dirs:
            if file_suffix != "*":
                if file.endswith(file_suffix):
                    yield file
            else:
                yield file

    @classmethod
    def traversal_file(cls, path, file_suffix="*"):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file_suffix == "*":
                    yield file
                else:
                    if file.endswith(file_suffix):
                        yield file

    @classmethod
    def traversal_file_path(cls, path, file_suffix="*"):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file_suffix == "*":
                    yield root + "\\" + file
                else:
                    if file.endswith(file_suffix):
                        yield root + "\\" + file

    @classmethod
    def copy_file(cls, file_path_source, file_path_dst):
        shutil.copy(file_path_source, file_path_dst)

    @classmethod
    def copy_dir(cls, path_source, path_dst):
        shutil.copytree(path_source, path_dst)

    @classmethod
    def create_dir(cls, path):
        if not cls.is_path_exists(path):
            os.makedirs(path)

    @classmethod
    def is_path_exists(cls, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                return False
            else:
                return True
        else:
            return False

    @classmethod
    def is_file_exists(cls, file_path):
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def read_binary(cls, file_path, read_size=1024):
        cls.read_binary_size = read_size
        with open(file_path, "rb") as f:
            while True:
                strb = f.read(cls.read_binary_size)
                if len(strb) == 0:
                    break
                yield strb

    @classmethod
    def read_text(cls, file_path, cueeent_encoding="utf-8"):
        with open(file_path, "r", encoding=cueeent_encoding) as f:
            while True:
                text_line = f.readline()

                if not text_line:
                    break

                text_line = text_line.replace("\n", "")
                yield text_line


class WriteTextFile(object):

    def __init__(self, file_path_, mode_="w", encoding_="utf-8"):
        self.file_path = file_path_
        self.mode = mode_
        self.encoding = encoding_
        self.file_obj = None

    def __enter__(self):
        self.file_obj = open(self.file_path, self.mode, encoding=self.encoding)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_obj is not None:
            self.file_obj.close()

    def __del__(self):
        pass

    def write(self, line):
        self.file_obj.write(line)

    def writelines(self, lines):
        self.file_obj.writelines(lines)


class WriteBinaryFile(object):

    def __init__(self, file_path_, mode_="wb"):
        self.file_path = file_path_
        self.file_obj = None
        self.mode = mode_

    def __enter__(self):
        self.file_obj = open(self.file_path, self.mode)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_obj is not None:
            self.file_obj.close()

    def __del__(self):
        pass

    def write(self, byte_data):
        self.file_obj.write(byte_data)


class Json(object):

    @classmethod
    def encode(cls, dict_data):
        return json.dumps(dict_data)

    @classmethod
    def decode(cls, json_str):
        return json.loads(json_str)


class ReadXml(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def walkData(self, root_node, level):
        temp_list = [level, root_node.tag, root_node.attrib, root_node.text]
        yield temp_list

        children_node = root_node.getchildren()
        if len(children_node) == 0:
            return
        for child in children_node:
            for item in self.walkData(child, level + 1):
                yield item

        return

    def get_xml_data(self):
        level = 1
        root = etree.parse(self.file_path).getroot()
        for x in self.walkData(root, level):
            yield x

    def get_xml_info(self, xml):
        return xml.docinfo.encoding, xml.docinfo.xml_version

    def get_node_by_xpath(self, xpath_sql):
        xml = etree.parse(self.file_path)
        root = xml.getroot()
        for node in root.xpath(xpath_sql):
            yield node


class WriteXml(object):
    def __init__(self):
        pass

    def add_root_element(self, element_name):
        self.root = etree.Element(element_name)
        return self.root

    def add_sub_element(self, parrent_element, element_name, value=""):
        child = etree.SubElement(parrent_element, element_name)
        child.text = value
        return child

    def save_as(self, file_path, encoding='utf-8'):
        tree = etree.ElementTree(self.root)
        tree.write(file_path, pretty_print=True,
                   xml_declaration=True,
                   encoding='utf-8')


if __name__ == '__main__':

    for file in File.traversal_file_path(r"C:\1234", "txt"):
        print(file)

    with open(r"测试_副件.jpg", mode="wb")as myself_copy:
        for data in File.read_binary(r"测试.jpg"):
            # print(File.un_pack(data))
            myself_copy.write(data)

    with open(r"test_binary.bin", mode="wb")as myself_copy:
        str_write = "12345678"
        myself_copy.write(DataAlgo.pack(str_write))

    for line in File.read_text(r"测试_gbk编码.txt", "gbk"):
        print(line)

    for line in File.read_text(r"测试_utf-8编码.txt"):
        print(line)

    index_count = 0
    for line in File.write_text(r"测试写文本_utf-8.txt"):
        # 处理写入行
        File.line_write_to_file = "1234"
        File.line_write_to_file = "\n"

        # 控制是否写入完毕
        index_count = index_count + 1
        if index_count > 4:
            File.is_end_to_write = True
