"""
@package base

Base Page class implementation
It implements methods which are common to all the pages throughout the application

This class needs to be inherited by all the page classes
This should not be used by creating object instances

Example:
    Class LoginPage(BasePage)
"""
from selenium_driver import SeleniumDriver
from utilities.util import Util

class BasePage(SeleniumDriver):

    def __init__(self, driver):
        """
        Inits BasePage class
        Returns:
            None
        """
        super(BasePage, self).__init__(driver)
        self.driver = driver
        self.util = Util()