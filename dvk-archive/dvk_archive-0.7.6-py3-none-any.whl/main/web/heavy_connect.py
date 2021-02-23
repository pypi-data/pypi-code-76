#!/usr/bin/env python3

from bs4 import BeautifulSoup
from json import loads
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FO
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def print_driver_instructions():
    """
    Print instructions for installing Selenium drivers.
    """
    print("This program uses Selenium to process JavaScript.")
    print("To run, you must install Selenium web drivers.")
    print("Download the drivers for your preferred browser:")
    print("")
    print("Firefox:")
    print("https://github.com/mozilla/geckodriver/releases")
    print("")
    print("Copy Selenium driver(s) to your PATH directory.")
    print("(On Windows, find PATH with command \"echo %PATH%\" )")
    print("(On Mac/Linux, find PATH with command \"echo $PATH\" )")

class HeavyConnect:

    def __init__(self, headless:bool=True):
        """
        Initialize the HeavyConnect class.
        """
        self.initialize_driver(headless)

    def initialize_driver(self, headless:bool=True):
        """
        Starts the Selenium driver.

        :param headless: Whether to run in headless mode, defaults to True
        :type headless: bool, optional
        """
        try:
            # TRY FIREFOX DRIVER
            options = FO()
            options.headless = headless
            options.page_load_strategy = "none"
            profile = webdriver.FirefoxProfile()
            self.driver = webdriver.Firefox(options=options, firefox_profile=profile)
        except WebDriverException:
            # PRINTS INSTRUCTIONS FOR GETTING SELENIUM DRIVER
            self.driver = None
            print_driver_instructions()

    def get_page(self, url:str=None, element:str=None) -> BeautifulSoup:
        """
        Connects to a URL and returns a BeautifulSoup object.
        Capable of loading JavaScript, AJAX, etc.

        :param url: URL to retrieve, defaults to None
        :type url: str, optional
        :param element: XPATH Element to wait for, defaults to None
        :type element: str, optional
        :return: BeautifulSoup object for the web page
        :rtype: BeautifulSoup
        """
        # RETURN NONE IF URL OR LOADED DRIVER IS INVALID
        if url is None or url == "" or self.driver is None:
            return None
        # ATTEMPT LOADING WEB PAGE
        try:
            self.driver.get(url)
            # WAIT FOR ELEMENT TO LOAD, IF SPECIFIED
            if element is not None and not element == "":
                WebDriverWait(self.driver, 10).until(
                     EC.presence_of_all_elements_located((By.XPATH, element)))
            bs = BeautifulSoup(self.driver.page_source, "lxml")
            return bs
        except:
            return None
        return None

    def get_json(self, url:str=None) -> dict:
        bs = self.get_page(url, "//div[@id='json']")
        try:
            element = bs.find("div", {"id": "json"})
            html = element.get_text()
            # CONVERT TO JSON
            json = loads(html)
            return json
        except:
            return None

    def get_driver(self) -> webdriver:
        """
        Returns the current Selenium Web Driver

        :return: Selenium Web Driver
        :rtype: webdriver
        """
        return self.driver

    def close_driver(self):
        """
        Closes the Selenium driver if possible.
        """
        if self.driver is not None:
            self.driver.close()
