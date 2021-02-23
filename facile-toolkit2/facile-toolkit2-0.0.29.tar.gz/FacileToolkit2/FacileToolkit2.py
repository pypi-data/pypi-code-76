"""

Robot library with often needed keywords.

"""

import datetime
import os
import random
import time

import robot
from SeleniumLibrary import LibraryComponent, JavaScriptKeywords, SelectElementKeywords, SeleniumLibrary
from SeleniumLibrary.errors import ElementNotFound
from SeleniumLibrary.utils import is_noney
from dateutil.relativedelta import relativedelta
from robot.api import logger
from robot.api.deco import keyword
from robot.errors import RobotError
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.utils.asserts import assert_true
from robot.utils.robottime import secs_to_timestr
from robot.utils.robottypes import is_list_like, is_truthy
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException


JS_DOM_LOADED = "return document.readyState=='complete'"


class Error(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True


class FacileToolkit2:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"

    def __init__(self):
        self.ajax_activation = "800ms"
        self.ajax_timeout = "120s"

    @keyword
    def set_ajax_activation(self, timeout):
        self.ajax_activation = timeout

    @keyword
    def set_ajax_timeout(self, timeout):
        self.ajax_timeout = timeout

    @keyword
    def wait(self, keyword, *keywordargs, retry="15x", retry_interval="1s"):
        """
        Wrapper for 'wait_until_keyword_succeeds' keyword, default 15 retries with 1s interval.

        ``keyword`` Keyword name to execute

        ``keywordargs`` Arguments

        ``retry`` retry timeout or retry times, (eg. 10x or 10s)

        ``retry_interval`` interval between retries
        """
        BuiltIn().wait_until_keyword_succeeds(retry, retry_interval, keyword, *keywordargs)

    @keyword
    def get_element_class(self, locator):
        """
        Get attribute 'class' of en element

        ``locator`` Locator to use when searching the element.
            See library documentation for the supported locator syntax.

        """
        self.set_selenium_library()
        return self.sl.find_element(locator).get_attribute("class")

    @keyword
    def get_element_css_property(self, locator, property):
        """
        The value of a CSS property
        ``locator`` Locator to use when searching the element.
            See library documentation for the supported locator syntax.
        ``property`` is the CSS property to get.
        """
        self.set_selenium_library()
        return self.sl.find_element(locator).value_of_css_property(property)

    @keyword
    def element_css_property_should_be(self, locator, property, expected):

        return BuiltIn().should_be_equal_as_strings(self.get_element_css_property(locator, property), expected)

    @keyword
    def element_attribute_should_contain_value(self, locator, attribute, value, message=None):
        """
        Fails if element attribute does not contain a value

        ``locator`` Locator to use when searching the element.
            See library documentation for the supported locator syntax.

        ``attribute`` attribute to get.
        
        ``value`` value that should be contained in ``attribute``    

        ``message`` custom error message
        """
        self.set_selenium_library()
        current_expected = self.sl.find_element(locator).get_attribute(attribute)
        if value not in current_expected:
            if is_noney(message):
                message = ("Element '%s' attribute should have contained value '%s' but "
                           "its value was '%s'." % (locator, value, current_expected))
            raise AssertionError(message)
        self.lc.info("Element '%s' attribute '%s' contains value '%s'." % (locator, attribute, value))

    @keyword
    def element_attribute_should_not_contain_value(self, locator, attribute, value, message=None):
        self.set_selenium_library()
        current_expected = self.sl.find_element(locator).get_attribute(attribute)
        if value in current_expected:
            if is_noney(message):
                message = ("Element '%s' attribute should not have contained value '%s' but "
                           "its value was '%s'." % (locator, value, current_expected))
            raise AssertionError(message)
        self.lc.info("Element '%s' attribute '%s' does not contain value '%s'." % (locator, attribute, value))

    @keyword
    def clear_session(self):
        """
        This keyword cleans the current session in order to isolate the execution
        """
        self._wait_until(
            self._clear_session,
            "Could not clear session in <TIMEOUT>."
        )

    def _clear_session(self):
        self.set_selenium_library()
        self.sl.delete_all_cookies()
        self.sl.reload_page()
        return True

    @keyword
    def scroll(self, range="0"):
        """ Scrolls the document.

            ``range`` might span between 0 to X where 0 is the beginning of the document.

            default is set to 0.
        """
        self.set_selenium_library()
        self.sl.execute_javascript("document.documentElement.scrollTop = " + range + ";")

    @keyword
    def dom_is_loaded(self, timeout="10s"):
        """
        returns True if DOM readyState equals "complete" before the given ``timeout``.
        """
        self.set_selenium_library()
        self.sl.wait_for_condition("return document.readyState=='complete'", timeout)

    @keyword
    def checkpoint(self, locator, timeout=None, error=None):
        self.set_selenium_library()
        self._wait_until(
            lambda: self.sl.find_element(locator).is_displayed() and self.sl.execute_javascript(JS_DOM_LOADED),
            "Element '%s' or their parents did not contain class in <TIMEOUT>." % locator, timeout, error
        )

    @keyword
    def select_from_list_random_index(self, locator, start_index=None, end_index=None, timeout=None, error=None):
        """
        Selects a random option from a Select WebElement specified by a locator,
        it is possible to specify a start index for the random selection
        """
        self.set_selenium_library()
        self._wait_until(
            lambda: not is_noney(self.lc.find_element(locator, required=False)) and
                    len(SelectElementKeywords(self.sl)._get_options(locator)),
            "Error selecting list %s random item" % locator,
            timeout, error
        )
        len_options = len(SelectElementKeywords(self.sl)._get_options(locator))
        if start_index is not None:
            assert_true(len_options >= int(start_index), "List length %s is less than start_index %s"
                        % (len_options, start_index))
        if is_noney(start_index) and len_options > 1:
            start_index = 1
        elif is_noney(start_index) and len_options == 1:
            start_index = 0
        else:
            start_index = int(start_index)
        end_index = len_options - 1 if is_noney(end_index) or int(end_index) > len_options else int(end_index)
        random_index = self.generate_random_number_as_string(start_index, end_index)
        self.sl.select_from_list_by_index(locator, random_index)
        self.lc.info("Selected index %s from list %s" % (random_index, locator))

    @keyword
    def select_from_list_random_index_optional(self, *locators, start_index=None, end_index=None, timeout=None):
        """
        Wrapper for "select from list random index" keyword, the random selection
        is performed only if the select element is present on the page
        """
        timeout = self.lc.get_timeout(timeout)
        for locator in locators:
            lista_presente = BuiltIn().run_keyword_and_return_status("Wait Until Element is Visible", locator, timeout)
            if lista_presente:
                self.select_from_list_random_index(locator=locator, start_index=start_index, end_index=end_index, timeout=timeout) 

    @keyword
    def i_land_on_page(self, url, timeout="60s", error=None):
        """
        Waits for a maximum time, defined by timeout argument (default=60s),
        until the location contains a portion of the url (specified by the parameter 'url')
        """
        self.set_selenium_library()
        try:
            self.sl.log_location()
            self.sl.wait_until_location_contains(url, timeout)
            is_jquery_present = BuiltIn().run_keyword_and_return_status('wait_for_condition', 'if(typeof(jQuery) == "function") {return true;} return false;', "1s")
            if is_jquery_present:
                self.wait_ajax_optional()

        # except TimeoutException as e:
        #     if "renderer" in str(e.msg).lower():
        #         self.sl.driver.refresh()
        #         self.sl.wait_until_location_contains(url, timeout)
        #     else:
        #         self.sl.capture_page_screenshot(filename="EMBED")
        finally:
            self.sl.log_location()

    @keyword
    def click_js(self, locator):
        """
        This keyword clicks a WebElement or a locator that represent a WebElement via Javascript
        """
        is_webelement = "webelement" in str(type(locator)).lower()
        if is_webelement:
            self.click_element_js(locator)
        else:
            self.click_locator_js(locator)

    @keyword
    def click_element_js(self, element):
        """
        This keyword clicks a WebElement via Javascript
        """
        self.set_selenium_library()
        self.sl.execute_javascript("arguments[0].click()", "ARGUMENTS", element)

    @keyword
    def click_locator_js(self, locator):
        """
        Clicks a locator that represent a WebElement via Javascript
        """
        self.set_selenium_library()
        element = self.sl.get_webelement(locator)
        self.sl.execute_javascript("arguments[0].click()", "ARGUMENTS", element)

    @keyword
    def i_see(self, *locators):
        """
        Loops over an array of locators and checks
        if the webelements represented by them are visible on the page
        """
        """
        Loops over an array of locators and checks
        if the webelements represented by them are visible on the page
        """
        self.set_selenium_library()
        not_visible_elements = [x for x in locators if
                                is_noney(self.lc.find_element(x, required=False)) or not self.sl.find_element(
                                    x).is_displayed()]
        if not_visible_elements:
            errors = ', '.join(not_visible_elements)
            BuiltIn().run_keyword_and_ignore_error("Should Be Empty", errors, "Following elements are not visible: %s" % errors)

    @keyword
    def i_dont_see(self, *locators):
        """
        Loops over an array of locators and checks
        if the webelements represented by them are visible on the page
        """
        self.set_selenium_library()
        visible_elements = [x for x in locators if
                            not is_noney(self.lc.find_element(x, required=False)) and self.sl.find_element(
                                x).is_displayed()]
        if visible_elements:
            errors = ', '.join(visible_elements)
            BuiltIn().run_keyword_and_ignore_error("Should Be Empty", errors, "Following elements are visible: %s" % errors)

    @keyword
    def select_first_autocomplete_option(self,
                                         locator_option="css:.autocomplete-suggestions:not([style*='display']):not(["
                                                        "style*='none']) strong",
                                         timeout=None, error=None):
        """
        Selects the first autocomplete option for auto-complete fields.
        """
        self.set_selenium_library()
        self.sl.wait_until_element_is_visible(locator_option, timeout=timeout, error=error)
        self.click_js(locator_option)

    @keyword
    def press_keys_on_active_element(self, *keys):
        """
        Inputs the given key to the active element in DOM
        """
        self.set_selenium_library()
        active_element = self.sl.execute_javascript("return document.activeElement;")
        self.sl.press_keys(active_element, *keys)

    @keyword
    def get_text_from_webelements(self, *webelements, timeout=None, error=None):
        """
        Takes in input a WebElements array and
        returns a string array containing the stripped texts retrieved from the webelements
        """
        self.set_selenium_library()
        self._wait_until(
            lambda: [self.sl.get_text(element) for element in webelements],
            "Error retrieving element texts",
            timeout, error
        )
        return [self.sl.get_text(element) for element in webelements]

    @keyword
    def get_text_from_locators(self, *webelements, timeout=None, error=None):
        """
        Takes in input a Locators array and
        returns a string array containing the stripped texts retrieved from the webelements
        """
        self.set_selenium_library()
        texts = []
        self._wait_until(
            lambda: [texts.extend(self.get_texts(element)) for element in webelements],
            "Error retrieving element texts",
            timeout, error
        )
        return texts

    def get_texts(self, locator):
        self.set_selenium_library()
        return [self.sl.get_text(element) for element in self.sl.find_elements(locator)]
    
    @keyword
    def generate_random_number_as_string(self, minimum, maximum):
        """
        Generates a random number between the range given by "min", "max" arguments
        and returns it as string
        """
        minimum = BuiltIn().convert_to_integer(minimum)
        maximum = BuiltIn().convert_to_integer(maximum)
        num = str(random.randint(minimum, maximum))
        return num

    @keyword
    def select_random_item_from_list(self, *in_list):
        """
        Returns a random item from the given list
        """

        if is_list_like(in_list):
            if in_list:
                return random.choice(*in_list)
            else:
                raise AssertionError("List is empty")
        else:
            raise AssertionError("Argument is %s, not a list" % type(in_list))

    @keyword
    def error_message_should_be(self, message,
                                error_locator="//span[(contains(@class, 'err') or contains(@class, 'wrong')) and "
                                              "normalize-space(.) and not(.//ancestor::*[contains(@style, "
                                              "'display:none') or contains(@style, 'display: none')])]",
                                timeout=None,
                                case_insensitive=True, match=True):
        """
        Checks if the given error message is present in DOM
        """
        self.set_selenium_library()
        try:
            self.sl.wait_until_element_is_visible(error_locator, timeout)
            error_msgs = self.sl.get_webelements(error_locator)
            found_errors = [el.text for el in error_msgs]
            Collections().log_list(found_errors)
            if is_truthy(match):
                Collections().should_contain_match(found_errors, message, case_insensitive=is_truthy(case_insensitive))
            else:
                Collections().list_should_contain_value(found_errors, message)
            logger.info("%s is contained in error message" % message)
        except Exception as error_thrown:
            raise Error(error_thrown)

    @keyword
    def wait_ajax(self, timeout=None, wait_active=None):
        self.set_selenium_library()
        if is_noney(timeout):
            timeout = self.ajax_timeout
        if is_noney(wait_active):
            wait_active = self.ajax_activation
        is_active = BuiltIn().run_keyword_and_return_status("wait_ajax_activation", wait_active)
        if is_active:
            self.sl.wait_for_condition('if(typeof(jQuery) == "function") {return jQuery.active == 0} return false', timeout)

    @keyword
    def wait_ajax_activation(self, timeout=None):
        self.set_selenium_library()
        if is_noney(timeout):
            timeout = self.ajax_activation
        self.sl.wait_for_condition('if(typeof(jQuery) == "function") {return jQuery.active == 1} return false', timeout)

    @keyword
    def wait_ajax_optional(self, timeout=None, wait_active=None):
        BuiltIn().run_keyword_and_ignore_error("wait_ajax", timeout, wait_active)

    @keyword
    def field_or_parents_should_contain_error(self, locator, timeout=None, error_class="wrong", error=None):
        self.wait_ultil_element_or_parents_contain_class(locator, error_class, timeout, error)

    @keyword
    def field_or_parents_should_be_verified(self, locator, timeout=None, verified_class="verified", error=None):
        self.wait_ultil_element_or_parents_contain_class(locator, verified_class, timeout, error)

    @keyword
    def field_should_contain_error(self, locator, timeout=None, error_class="wrong", error=None):
        self.wait_ultil_element_contains_class(locator, error_class, timeout, error)

    @keyword
    def field_should_be_verified(self, locator, timeout=None, verified_class="verified", error=None):
        self.wait_ultil_element_contains_class(locator, verified_class, timeout, error)

    @keyword
    def fields_should_be_verified(self, *locators, timeout=None, verified_class="verified", error=None):
        for locator in locators:
            BuiltIn().run_keyword_and_continue_on_failure("field_or_parents_should_be_verified", locator, timeout,
                                                          verified_class, error)

    @keyword
    def fields_should_contain_error(self, *locators, timeout=None, error_class="wrong", error=None):
        for locator in locators:
            BuiltIn().run_keyword_and_continue_on_failure("field_or_parents_should_contain_error", locator, timeout,
                                                          error_class, error)

    @keyword
    def select_checkboxes(self, *locators, timeout="60s"):
        for locator in locators:
            self.wait_ajax_optional(timeout)
            if BuiltIn().run_keyword_and_return_status("checkbox_should_not_be_selected", locator):
                self.click_js(locator)
        if timeout is not None:
            self.wait_ajax_optional(timeout)
        self.should_be_checked(*locators)

    @keyword
    def unselect_checkboxes(self, *locators):
        for locator in locators:
            if BuiltIn().run_keyword_and_return_status("checkbox_should_be_selected", locator):
                self.click_js(locator)
        self.should_not_be_checked(*locators)

    @keyword
    def should_be_checked(self, *locators):
        self.set_selenium_library()
        for locator in locators:
            is_checked = self.sl.driver.execute_script(
                "return arguments[0].checked || arguments[0].classList.contains('checked');",
                self.sl.find_element(locator))
            BuiltIn().run_keyword_and_continue_on_failure("should_be_true", is_checked,
                                                          "Locator %s is not checked" % locator)

    @keyword
    def should_not_be_checked(self, *locators):
        self.set_selenium_library()
        for locator in locators:
            is_checked = self.sl.driver.execute_script(
                "return arguments[0].checked || arguments[0].classList.contains('checked');",
                self.sl.find_element(locator))
            BuiltIn().run_keyword_and_continue_on_failure("should_not_be_true", is_checked,
                                                          "Locator %s is checked" % locator)

    @keyword
    def element_attribute_value_should_not_be(self, locator, attribute, expected, message=None):
        self.set_selenium_library()
        current_expected = self.sl.find_element(locator).get_attribute(attribute)
        if current_expected == expected:
            if is_noney(message):
                message = ("Element '%s' attribute should not have value '%s'"
                           % (locator, expected))
            raise AssertionError(message)
        self.lc.info("Element '%s' attribute '%s' contains value '%s'." % (locator, attribute, expected))

    @keyword
    def textfield_value_should_not_be(self, locator, expected, message=None):
        """Verifies text field ``locator`` does not have text ``expected``.

        ``message`` can be used to override default error message.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.set_selenium_library()
        actual = self.lc.find_element(locator, 'text field').get_attribute('value')
        if actual == expected:
            if is_noney(message):
                message = "Value of text field '%s' should not have been '%s' " \
                          "." % (locator, expected)
            raise AssertionError(message)
        self.lc.info("Content of text field '%s' is '%s'." % (locator, expected))

    @staticmethod
    @keyword
    def get_browser_options(browser, headless=False):
        if browser.lower() == "chrome":
            return FacileToolkit2.get_chrome_options(headless=headless)
        elif browser == "firefox" or browser == "ff":
            return FacileToolkit2.get_ff_options(headless=headless)
        else:
            raise RobotError("{} unexpected browser name.".format(browser))

    @staticmethod
    @keyword
    def get_chrome_options(headless=False):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-browser-side-navigation")
        chrome_options.add_argument("----dns-prefetch-disable")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.set_capability("pageLoadStrategy", "eager")
        if headless:
            chrome_options.add_argument("--window-size=1920,960")
            chrome_options.headless = True
        return chrome_options

    @staticmethod
    @keyword
    def get_ff_options(headless=False):
        os.environ['MOZ_HEADLESS_WIDTH'] = '1920'
        os.environ['MOZ_HEADLESS_HEIGHT'] = '960'
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--disable-extensions")
        firefox_options.set_preference("browser.link.open_newwindow.restriction", 0)
        firefox_options.set_preference("browser.link.open_newwindow", 3)
        if headless:
            firefox_options.headless = True
        return firefox_options

    @staticmethod
    @keyword
    def get_chrome_mobile_options(headless=False, device="iPhone X"):
        chrome_options = webdriver.ChromeOptions()
        mobile_emulation = {"deviceName": device}
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-browser-side-navigation")
        chrome_options.add_argument("----dns-prefetch-disable")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.set_capability("pageLoadStrategy", "eager")
        if headless:
            chrome_options.headless = True
        return chrome_options

    @staticmethod
    @keyword
    def add_argument_to_browser_options(options, argument):
        options.add_argument(argument)
        return options

    @staticmethod
    @keyword
    def add_experimental_to_browser_options(options, argument, value):
        options.add_experimental_option(argument, value)
        return options

    @staticmethod
    def get_current_date_decremented_by_time(years=0, months=0, days=0):
        date = datetime.datetime.now() - relativedelta(years=years, months=months, days=days)
        return date.strftime('%Y'), date.strftime('%m'), date.strftime('%d')

    @keyword
    def wait_ultil_element_contains_class(self, locator, clazz, timeout=None, error=None):
        self.set_selenium_library()
        self._wait_until(
            lambda: clazz in self.sl.get_element_attribute(locator, "class"),
            "Element '%s' did not contain class '%s' in <TIMEOUT>." % (locator, clazz),
            timeout, error
        )

    @keyword
    def wait_ultil_element_does_not_contain_class(self, locator, clazz, timeout=None, error=None):
        self.set_selenium_library()
        self._wait_until(
            lambda: clazz not in self.sl.get_element_attribute(locator, "class"),
            "Element '%s' did not contain class '%s' in <TIMEOUT>." % (locator, clazz),
            timeout, error
        )

    def get_element_parents(self, locator):
        self.set_selenium_library()
        get_parents = "let parents = node => (node.parentElement ? parents(node.parentElement) : [])" \
                      ".concat([node]);return parents(arguments[0]);"
        return self.sl.driver.execute_script(get_parents, self.sl.find_element(locator))

    @keyword
    def wait_ultil_element_or_parents_contain_class(self, locator, clazz, timeout=None, error=None):
        elements = self.get_element_parents(locator)
        self._wait_until(
            lambda: any(clazz in element.get_attribute("class") for element in elements),
            "Element '%s' or their parents did not contain class '%s' in <TIMEOUT>." % (locator, clazz),
            timeout, error
        )

    @keyword
    def wait_ultil_element_or_parents_do_not_contain_class(self, locator, clazz, timeout=None, error=None):
        elements = self.get_element_parents(locator)
        self._wait_until(
            lambda: any(clazz not in element.get_attribute("class") for element in elements),
            "Element '%s' or their parents did not contain class '%s' in <TIMEOUT>." % (locator, clazz),
            timeout, error
        )

    @keyword
    def click_label_from_field_locator(self, locator):
        self.set_selenium_library()
        element_id = self.sl.get_element_attribute(locator, "id")
        self.click_js("css: label[for='%s']" % element_id)

    @keyword
    def scroll_to_bottom(self):
        self.scroll("99999")

    @keyword
    def wait_for_condition_extended(self, *condition, timeout=None, error=None):
        self.set_selenium_library()
        jk = JavaScriptKeywords(self.sl)
        js_code, _ = jk._get_javascript_to_execute(condition)
        if 'return' not in js_code:
            raise ValueError("Condition '%s' did not have mandatory 'return'." % js_code)
        self._wait_until(
            lambda: self.sl.execute_javascript(*condition),
            "Condition '%s' did not become true in <TIMEOUT>." % js_code,
            timeout, error
        )

    @keyword
    def screenshot_on_failure(self):
        self.set_selenium_library()
        if self.sl._drivers.current:
            self._log_field_values()
            BuiltIn().run_keyword_if_test_failed("capture_page_screenshot", "EMBED")
            self.sl.log_location()

    def _log_field_values(self):
        try:
            status, return_value = BuiltIn().run_keyword_and_ignore_error("execute_javascript",
                                                                          "return Array.from(document.querySelectorAll('select, input')).map(p=>{return {id: p.id, value:p.value, text:p.text}})")
            if status == 'PASS' and return_value is not None:
                Collections().log_list(list(return_value))
        except Exception:
            pass

    @keyword
    def teardown_with_screenshot(self):
        self.set_selenium_library()
        if self.sl._drivers.current:
            self._log_field_values()
            BuiltIn().run_keyword_if_test_failed("capture_page_screenshot", "EMBED")
            self.sl.log_location()
            self.sl.close_all_browsers()

    def i_see_elements_label(self, *locators):
        self.set_selenium_library()
        for locator in locators:
            BuiltIn().run_keyword_and_continue_on_failure("element_should_be_visible",
                                                          "css:label[for='%s']" % self.sl.get_element_attribute(locator,
                                                                                                                "id"))

    @keyword
    def close_symfony_toolbar(self, timeout=None):
        self.set_selenium_library()
        if BuiltIn().run_keyword_and_return_status("wait_until_element_is_visible", "css:body > .sf-toolbar", timeout):
            self.sl.execute_javascript("document.querySelector('body > .sf-toolbar').style='display:none'")

    @keyword
    def execute_jquery_method_on_webelement(self, locator, method):
        self.set_selenium_library()
        element = self.sl.find_element(locator)
        self.sl.driver.execute_script("$(arguments[0]).%s" % method, element)

    @keyword
    def select_jquery(self, locator):
        self.execute_jquery_method_on_webelement(locator, "select();")

    @keyword
    def focus_jquery(self, locator):
        self.execute_jquery_method_on_webelement(locator, "focus();")

    @keyword
    def change_jquery(self, locator):
        self.execute_jquery_method_on_webelement(locator, "change();")

    @keyword
    def blur_jquery(self, locator):
        try:
            self.execute_jquery_method_on_webelement(locator, "blur();")
            BuiltIn().sleep("200ms")
            self.execute_jquery_method_on_webelement(locator, "blur();")
        except Exception:
            pass

    @keyword
    def val_jquery(self, locator, value):
        self.execute_jquery_method_on_webelement(locator, "val('%s');" % value)


    @keyword
    def is_visible(self, locator, timeout="1s"):
        self.set_selenium_library()
        return BuiltIn().run_keyword_and_return_status("wait_until_element_is_visible", locator, timeout)

    @staticmethod
    @keyword
    def return_2nd_if_1st_is_none(first, second):
        return second if first is None else first

    @keyword
    def i_handle_gdpr(self, mandatory=False, timeout="5s"):
        self.set_selenium_library()
        mandatory = is_truthy(mandatory)
        try:
            self.sl.wait_until_element_is_visible('css:#onetrust-banner-sdk[style*="0px"]', timeout)
        except:
            if mandatory:
                raise
        try:
            self.click_js('id:onetrust-accept-btn-handler')
        except:
            if mandatory:
                raise

    def _wait_until(self, condition, error, timeout=None, custom_error=None):
        self.set_selenium_library()
        timeout = self.lc.get_timeout(timeout)
        if is_noney(custom_error):
            error = error.replace('<TIMEOUT>', secs_to_timestr(timeout))
        else:
            error = custom_error
        self._wait_until_worker(condition, timeout, error)

    def _wait_until_worker(self, condition, timeout, error):
        self.set_selenium_library()
        max_time = time.time() + timeout
        not_found = None
        while time.time() < max_time:
            try:
                if condition():
                    return
            except ElementNotFound as err:
                not_found = str(err)
            except StaleElementReferenceException as err:
                self.lc.info('Suppressing StaleElementReferenceException from Selenium.')
                not_found = err
            else:
                not_found = None
            time.sleep(0.2)
        raise AssertionError(not_found or error)

    def set_selenium_library(self):
        self.sl = BuiltIn().get_library_instance('SeleniumLibrary')
        self.lc = LibraryComponent(self.sl)


if __name__ == "__main__":
    robot.run('%s/atests/keyword_tests.robot' % os.getcwd())
