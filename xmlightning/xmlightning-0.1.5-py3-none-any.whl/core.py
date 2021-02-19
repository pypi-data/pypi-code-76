import xml.etree.ElementTree as ElementTree

from xml.etree.ElementTree import Element
from io import TextIOWrapper
from typing import *
from collections.abc import Callable

""" xmlightning! """


class _Lightning(object):
    @staticmethod
    def has_attribs(element: Element, desired_attribs={}) -> bool:
        return element.attrib == desired_attribs

    @staticmethod
    def has_number_of_children(element: Element, x: int = 0) -> bool:
        count = 0
        for child_element in element:
            if count > x:
                return False
            count += 1
        return count != x

    @staticmethod
    def check_text(text_to_check, check_with: Iterable) -> bool:
        return text_to_check not in check_with


class Lightning(_Lightning):

    """
    Takes in no parameters for __init__; however, __init__ is required
    """

    def __init__(self):
        self.__routes: Dict[str, Callable] = {}

    def get_routes(self) -> Dict[str, Callable]:
        return self.__routes

    def route(self, path: AnyStr) -> None:
        """ Creates a route for the provided path """
        def inner(function_: Callable):
            self.__routes[path] = function_

            def wrapper(element):
                pass
            return wrapper
        return inner

    def parse(self, xml_like_document: Union[AnyStr, TextIOWrapper]) -> None:
        """  """
        xml_document_root = ElementTree.parse(xml_like_document).getroot()
        for path_as_string, function_ in self.__routes.items():
            for element in xml_document_root.findall(path_as_string):
                function_(element)


class LightningAlternative(object):

    """
    Alternative declaration of the Lightning class
    """

    __routes: Dict[str, Callable] = {}

    @classmethod
    def get_routes(cls) -> Dict[str, Callable]:
        return cls.__routes

    @classmethod
    def route(cls, path: AnyStr) -> None:
        """ Creates a route for the provided path """

        def inner(function_: Callable):
            cls.__routes[path] = function_

            def wrapper(element):
                pass
            return wrapper
        return inner

    @classmethod
    def parse(cls, xml_like_document: Union[AnyStr, TextIOWrapper]) -> None:
        xml_document_root = ElementTree.parse(xml_like_document).getroot()
        for path_as_string, function_ in cls.__routes.items():
            for element in xml_document_root.findall(path_as_string):
                function_(None, element)
