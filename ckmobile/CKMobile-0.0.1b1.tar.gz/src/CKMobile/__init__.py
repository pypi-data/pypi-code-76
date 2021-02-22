# encoding: utf-8
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
import logging
import os
import socket
import sys
# sys.path.append('./Pyso8583')
from parser_iso8583 import *

dir_file = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

class CKMobile(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.1

    def __init__(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        logger = logging.getLogger(__name__)

    # Function appium
    @keyword('[M] Open Application Mobile')
    def mobile_open_application_mobile(self, deviceName, platformName, platformVersion, appPackage, appActivity, Appium_port='4723', noReset=True, automationName='UiAutomator2'):
        keyword_execute = 'Open Aapplication Mobile'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        BuiltIn().run_keyword(keyword_execute, deviceName, platformName, platformVersion, appPackage, appActivity, noReset, Appium_port, automationName)

    @keyword('[M] Wait Until Contains Message')
    def mobile_wait_until_contains_message(self, Element_text, Timeout=10):
        keyword_execute = 'Wait Until Contains Message'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        BuiltIn().run_keyword(keyword_execute, Element_text, Timeout)

    @keyword('[M] Click Element Message')
    def mobile_click_element_message(self, Element_text, Timeout=10):
        keyword_execute = 'Click Element Message'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        BuiltIn().run_keyword(keyword_execute, Element_text, Timeout)

    @keyword('[M] Input for Elements Text')
    def mobile_input_for_elements_text(self, Element_text, Index, Message):
        keyword_execute = 'Input for Elements Text'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        BuiltIn().run_keyword(keyword_execute, Element_text, Index, Message)

    @keyword('[M] Swipe By Percent Height')
    def mobile_swipe_by_percent_height(self, Start=1, End=99):
        keyword_execute = 'Swipe By Percent Height'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        BuiltIn().run_keyword(keyword_execute, Start, End)

    @keyword('[M] Get Message Regular')
    def mobile_get_message_regular(self, Element_text, Pattern, Timeout=10):
        keyword_execute = 'Get Message Regular'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        data = BuiltIn().run_keyword(keyword_execute, Element_text, Pattern, Timeout)
        return data

    @keyword('[M] Click Image Index')
    def mobile_click_image_index(self, Index=1):
        keyword_execute = 'Click Image Index'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        BuiltIn().run_keyword(keyword_execute, Index)

    @keyword('[M] Click Group Index')
    def mobile_click_group_index(self, Index=1):
        keyword_execute = 'Click Group Index'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        BuiltIn().run_keyword(keyword_execute, Index)

    @keyword('[M] Press Number')
    def mobile_press_number(self, Nunber=0):
        keyword_execute = 'Press Number'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        BuiltIn().run_keyword(keyword_execute, Nunber)

    @keyword('[M] Input for Elements')
    def mobile_input_for_elements(self, Index, Message):
        keyword_execute = 'Input for Elements'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        BuiltIn().run_keyword(keyword_execute, Index, Message)

    @keyword('[M] Wait Until Contains Element')
    def mobile_wait_until_contains_element(self, Attributes, Value, Timeout=10):
        keyword_execute = 'Wait Until Contains Element'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        BuiltIn().run_keyword(keyword_execute, Attributes, Value, Timeout)

    @keyword('[M] Get Message')
    def mobile_get_message(self, Attributes, Value, Timeout=10):
        keyword_execute = 'Get Message'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        data = BuiltIn().run_keyword(keyword_execute, Attributes, Value, Timeout)
        return data

    @keyword('[M] Click Element')
    def mobile_click_element(self, Attributes, Value, Timeout=10):
        keyword_execute = 'Click Elements'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        BuiltIn().run_keyword(keyword_execute, Attributes, Value, Timeout)

    @keyword('[M] Page Down To Message')
    def mobile_page_down_to_message(self, Element_text, Rounds=20):
        keyword_execute = 'Page Down To Message'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        BuiltIn().run_keyword(keyword_execute, Element_text, Rounds)

    @keyword('[M] Page Up To Message')
    def mobile_page_up_to_message(self, Element_text, Rounds=20):
        keyword_execute = 'Page Up To Message'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/appium.txt')
        BuiltIn().run_keyword(keyword_execute, Element_text, Rounds)
