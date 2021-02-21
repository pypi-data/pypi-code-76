import re


class Object(object):
    @staticmethod
    def is_name_valid(name):  # verilog rules
        return re.match(r'(^[a-zA-Z_][a-zA-Z0-9_$]{0,1023}$|^\\\S* $)', name)

    def __init__(self, name):
        # verilog rules
        if not self.is_name_valid(name):
            raise Exception('name "' + name + '" should be as verilog syntax format')
        self.__name = name
        self.__properties = {}

    def get_object_name(self):
        return self.__name

    def set_object_name(self, name):
        if not self.is_name_valid(name):
            raise Exception('name "' + name + '" should be as verilog syntax format')
        self.__name = name

    def get_property(self, property):
        return self.__properties.get(property)

    def set_property(self, property, value):
        self.__properties[property] = value
        return self

    def get_properties(self, filter=None, name_regex=None):
        return self.filter_objects(self.__properties, name_regex=name_regex, filter=filter)

    @staticmethod
    def filter_objects(objects, name_regex=None, filter=None):
        # filter pins/nets/busses with regex or/with lambda filter(using their properties for example)
        if filter is None and name_regex is None:
            return objects
        if name_regex:  # get all objects that matches regex
            if filter is None:
                filter = lambda x: True
            return [obj for obj in objects if filter(obj) and re.match(name_regex, obj.get_object_name())]
        return [obj for obj in objects if filter(obj)]  # get all objects that pass filter

    def __str__(self):
        return self.__name

