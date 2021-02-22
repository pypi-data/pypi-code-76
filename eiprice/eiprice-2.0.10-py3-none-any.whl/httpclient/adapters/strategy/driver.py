from abc import ABC, abstractmethod
from functools import wraps

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver


def shield_from_no_such_element(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoSuchElementException:
            return None

    return decorated_view


class ContentFinderStrategy(ABC):
    @abstractmethod
    def execute(self, select, driver, first=True):
        pass


class FindByXpath(ContentFinderStrategy):
    @staticmethod
    @shield_from_no_such_element
    def execute(select: str, driver: WebDriver, first=True):
        if first:
            return driver.find_element_by_xpath(select)
        return driver.find_elements_by_xpath(select)


class FindById(ContentFinderStrategy):
    @staticmethod
    @shield_from_no_such_element
    def execute(select: str, driver: WebDriver, first=True):
        if first:
            return driver.find_element_by_id(select)
        return driver.find_elements_by_id(select)


class FindByCss(ContentFinderStrategy):
    @staticmethod
    @shield_from_no_such_element
    def execute(select: str, driver: WebDriver, first=True):
        if first:
            return driver.find_element_by_css_selector(select)
        return driver.find_elements_by_css_selector(select)


class FindByName(ContentFinderStrategy):
    @staticmethod
    @shield_from_no_such_element
    def execute(select: str, driver: WebDriver, first=True):
        if first:
            return driver.find_element_by_name(select)
        return driver.find_elements_by_name(select)


class FindByTagName(ContentFinderStrategy):
    @staticmethod
    @shield_from_no_such_element
    def execute(select: str, driver: WebDriver, first=True):
        if first:
            return driver.find_element_by_tag_name(select)
        return driver.find_elements_by_tag_name(select)


class FindByClassName(ContentFinderStrategy):
    @staticmethod
    @shield_from_no_such_element
    def execute(select: str, driver: WebDriver, first=True):
        if first:
            return driver.find_element_by_class_name(select)
        return driver.find_elements_by_class_name(select)
