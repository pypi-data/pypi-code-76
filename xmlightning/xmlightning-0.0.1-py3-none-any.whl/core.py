import xml.etree.ElementTree as ElementTree
from io import TextIOWrapper
from typing import *
from collections.abc import Callable

""" xmlightning! """


class Lightning(object):
    
    """ read the damn docs that took me time to write"""

    def __init__(self):
        self.__routes: Dict[str, function] = {}

    def route(self, path: AnyStr) -> None:
        """ Creates a route for the provided path """
        def inner(function_: Callable):
            self.__routes[path] = function_
            def wrapper(element):
                pass
            return wrapper
        return inner

    def parse(self, xml_like_document: Union[AnyStr, TextIOWrapper]) -> None:
        xml_document_root = ElementTree.parse(xml_like_document).getroot()
        print(self.__routes)
        for path_as_string, function_ in self.__routes.items():
            for element in xml_document_root.findall(path_as_string):
                function_(element)
