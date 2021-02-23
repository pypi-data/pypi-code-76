#!/usr/bin/env/ python3

from bs4 import BeautifulSoup
from dvk_archive.main.web.heavy_connect import HeavyConnect
from dvk_archive.test.temp_dir import get_test_dir
from os import stat
from os.path import abspath, join

def test_get_page():
    """
    Tests the get_page method.
    """
    # TEST LOADING ELEMENTS FROM A WEB PAGE
    connect = HeavyConnect()
    try:
        url = "http://pythonscraping.com/exercises/exercise1.html"
        page = connect.get_page(url)
        assert page is not None
        assert page.find("h1").get_text() == "An Interesting Title"
        assert page.find("title").get_text() == "A Useful Page"
        # TEST WAITING FOR ELEMENT
        url = "http://pythonscraping.com/pages/javascript/ajaxDemo.html"
        page = connect.get_page(url, "//button[@id='loadedButton']")
        assert page is not None
        element = page.find("button", {"id":"loadedButton"}).get_text()
        assert element  == "A button to click!"
        # TEST WAITING FOR NON-EXISTANT ELEMENT
        url = "http://pythonscraping.com/exercises/exercise1.html"
        page = connect.get_page(url, "//a[href='non-existant']")
        assert page is None
        # TEST LOADING WITH INVALID URL
        page = connect.get_page(None, None)
        assert page is None
        url = "qwertyuiopasdfghjkl"
        page = connect.get_page(url, None)
        assert page is None
        # CLOSE DRIVER
    finally:
        connect.close_driver()

def test_load_json():
    """
    Tests the load_json function.
    """
    connect = HeavyConnect()
    try:
        # TEST LOADING PAGE AS A JSON OBJECT
        json = connect.get_json("http://echo.jsontest.com/key/value/json/test")
        assert json["json"] == "test"
        assert json["key"] == "value"
        # TEST LOADING AN INVALID PAGE
        json = connect.get_json("asdfghjkl")
        assert json is None
        json = connect.get_json(None)
        assert json is None
    finally:
        connect.close_driver()

def all_tests():
    """
    Runs all tests for the heavy_connect module.
    """
    test_load_json()
    test_get_page()
