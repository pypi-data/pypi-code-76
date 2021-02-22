# encoding: utf-8
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
import logging
import os
import socket
import sys

dir_file = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

class CKWeb(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.1

    def __init__(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        logger = logging.getLogger(__name__)

    # Function Selenium
    @keyword('[W] Open Browser Url')
    def web_open_browser_url(self, URL, BrowserType):
        keyword_execute = 'Open Browser Url'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        BuiltIn().run_keyword(keyword_execute, URL, BrowserType)

    @keyword('[W] Wait Until Contains Message')
    def web_wait_until_contains_message(self, Element_text, Timeout=10):
        keyword_execute = 'Wait Until Contains Message'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        BuiltIn().run_keyword(keyword_execute, Element_text, Timeout)

    @keyword('[W] Click Element Message')
    def web_click_element_message(self, Element_text, Timeout=10):
        keyword_execute = 'Click Element Message'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        BuiltIn().run_keyword(keyword_execute, Element_text, Timeout)

    @keyword('[W] Input for Elements Text')
    def web_input_for_elements_text(self, Element_text, Index, Message):
        keyword_execute = 'Input for Elements Text'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        BuiltIn().run_keyword(keyword_execute, Element_text, Index, Message)

    @keyword('[W] Get Message Regular')
    def web_get_message_regular(self, Element_text, Pattern, Timeout=10):
        keyword_execute = 'Get Message Regular'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        data = BuiltIn().run_keyword(keyword_execute, Element_text, Pattern, Timeout)
        return data

    @keyword('[W] Click Image Index')
    def web_click_image_index(self, Index=1):
        keyword_execute = 'Click Image Index'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        BuiltIn().run_keyword(keyword_execute, Index)

    @keyword('[W] Press Enter')
    def web_press_enter(self, attributes, value, Keys='ENTER'):
        keyword_execute = 'Press Enter'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        BuiltIn().run_keyword(keyword_execute, attributes, value, Keys)

    @keyword('[W] Input for Elements')
    def web_input_for_elements(self, Index, Message):
        keyword_execute = 'Input for Elements'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        BuiltIn().run_keyword(keyword_execute, Index, Message)

    @keyword('[W] Wait Until Contains Element')
    def web_wait_until_contains_element(self, Attributes, Value, Timeout=10):
        keyword_execute = 'Wait Until Contains Element'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        BuiltIn().run_keyword(keyword_execute, Attributes, Value, Timeout)

    @keyword('[W] Get Message')
    def web_get_message(self, Attributes, Value, Timeout=10):
        keyword_execute = 'Get Message'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        data = BuiltIn().run_keyword(keyword_execute, Attributes, Value, Timeout)
        return data

    @keyword('[W] Click Element')
    def web_click_element(self, Attributes, Value, Timeout=10):
        keyword_execute = 'Click Elements'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        BuiltIn().run_keyword(keyword_execute, Attributes, Value, Timeout)

    @keyword('[W] Page Down To Message')
    def web_page_down_to_message(self, Element_text, Rounds=20):
        keyword_execute = 'Page Down To Message'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        BuiltIn().run_keyword(keyword_execute, Element_text, Rounds)

    @keyword('[W] Page Up To Message')
    def web_page_up_to_message(self, Element_text, Rounds=20):
        keyword_execute = 'Page Up To Message'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        BuiltIn().run_keyword(keyword_execute, Element_text, Rounds)

    @keyword('[W] Page Up To HOME')
    def web_page_up_to_home(self):
        keyword_execute = 'Page Up To HOME'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        BuiltIn().run_keyword(keyword_execute)        

    @keyword('[W] Page Down To END')
    def web_page_down_to_end(self):
        keyword_execute = 'Page Down To END'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/selenium.txt')
        BuiltIn().run_keyword(keyword_execute)
