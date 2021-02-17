'''
Created on 13 feb. 2018

@author: ex03210
'''
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotVisibleException

from nemonet.seleniumwebdriver.page_capture import PageCapturing

import random
import string
import time

from nemonet.cvision.computer_vision import ComputerVision

class Command(object):
    """
        All kind of selenium actions
    """


    def __init__(self, driver=None):
        """Constructor"""
        self.driver = driver
        self._wait = WebDriverWait(self.driver, 60)

    def openurl(self, url ):
        self.driver.get(str(url))

    def screenshot(self, filename):
        capture = PageCapturing(self.driver)
        capture.capture_save(file_name_cpatured=filename)

    def element(self, locator):
        element = self._wait.until(ec.element_to_be_clickable(locator), message='Cannot locate {}'.format(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    def click(self, locator):
        self.element(locator).click()

    def select_drop_down_by_value(self, select_locator, value):
        Select(self.element(select_locator)).select_by_value(value)

    def select_drop_down_by_text(self, select_locator, text):
        Select(self.element(select_locator)).select_by_visible_text(text)

    def find_element_xpath(self, xpath_str):
        return self._wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))

    def find_elements_xpath(self, xpath_str):
        return self._wait.until(ec.visibility_of_all_elements_located((By.XPATH, xpath_str)))

    def fill_in_text(self, xpath_str, text):
        # element = WebDriverWait(self.driver, 60 ).until(EC.presence_of_element_located(( By.XPATH, xpathStr )))
        element = self._wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        actions.click()
        actions.send_keys(text)
        actions.perform()

    def fill_in_text_no_action_chain(self, xpath_str, text):
        element = self._wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        element.send_keys(text)

    def element_fill_in_text(self, element, text):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        actions.click()
        actions.send_keys(text)
        actions.perform()

    def fill_in_text_enter(self, xpath_str, text):
        element = self._wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click()
        actions.send_keys(text)
        actions.send_keys(Keys.RETURN).perform()

    def clear_fill_in_text(self, xpath_str, text):
        element = self._wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        actions = ActionChains(self.driver)
        element.clear()
        actions.move_to_element(element).perform()
        actions.click()
        actions.send_keys(text)
        actions.perform()

    def clear_fill_in_text_tab(self, xpath_str, text):
        element = self._wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        actions = ActionChains(self.driver)
        element.clear()
        actions.move_to_element(element).perform()
        actions.click()
        actions.send_keys(text)
        actions.send_keys(Keys.TAB)
        actions.perform()


    def click_xpath(self, xpath_str):
        element = self._wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        actions.click()
        actions.perform()

    def click_css(self, css_str):
        element = self._wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, css_str)))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        actions.click()
        actions.perform()

    def click_element_in_list(self, xpath_str, index):
        element = self._wait.until(ec.visibility_of_all_elements_located((By.XPATH, xpath_str)))
        actions = ActionChains(self.driver)
        actions.move_to_element(element[index]).perform()
        actions.click()
        actions.perform()

    def element_click(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        actions.click()
        actions.perform()

    def double_click_xpath(self, xpath_str):
        element = self._wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        actions.double_click()
        actions.perform()

    def __movedDownEnter__(self, xpStr, nbrofMoves):
        element = self._wait.until(ec.visibility_of_element_located((By.XPATH, xpStr)))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        actions.click().perform()
        for i in range(nbrofMoves):
            actions.send_keys(Keys.DOWN)
        actions.perform()
        actions.send_keys(Keys.RETURN).perform()

    def __scrollToTop__(self):
        element = self.driver.find_element_by_tag_name("head")
        self.driver.execute_script("return arguments[0].scrollIntoView(true);", element)

    def scroll_to_element(self, xpath_str):
        element = WebDriverWait(self.driver, 120).until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        self.driver.execute_script("return arguments[0].scrollIntoView(true);", element)

    def __findTextAndClick__(self, text):
        self.driver.find_element_by_xpath("//*[contains(text(), '%s')]" % (text)).click()

    def get_text_xpath(self, xpath_str):
        element = self._wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        return element.text

    def get_text_from_element(self, element):
        return element.text

    def __selectFromDropDown__(self, xpathStr, text):
        element = WebDriverWait(self.driver, 120).until(ec.visibility_of_element_located((By.XPATH, xpathStr)))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        actions.click()
        actions.send_keys(text)
        actions.click()
        actions.perform()

    def select_drop_down_enter(self, xpath_str, text):
        element = self._wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        actions.click()
        actions.send_keys(text)
        actions.click()
        actions.send_keys(Keys.RETURN)
        actions.perform()

    def __selectFromDropDownByValue__(self, xpathStr, value):
        element = Select(WebDriverWait(self.driver, 120).until(ec.visibility_of_element_located((By.XPATH, xpathStr))))
        element.select_by_value(value)

    def wait(self, number_of_seconds):
        time.sleep(number_of_seconds)

    def executeSequences(self, seq, g):

        for step in g.getSetup():
            self.execute_action(step.getAction())

        pa = seq.get()
        for l in pa:
            #logger.info("Excute sequence=%s" % (str(l)))
            for el in l:
                a = g.getVertex(el).getAction()
                self.execute_action(a)

    def execute_action(self, a):
        """
        TODO : error handling
        :param a:
        :return:
        """
        command_type = a.getElementType()
        if command_type == 'CLICKABLE':
            self.click_xpath(a.getXpathStr())
        elif command_type == 'TEXTABLE':
            if a.getValue() == None:
                rStr = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
            else:
                rStr = a.getValue()
            self.fill_in_text(a.getXpathStr(), rStr)
        elif command_type == 'JSexec':
            self.driver.execute_script(a.getXpathStr())
        elif command_type == 'SELECTABLE':
            self.click_element_in_list(a.getXpathStr(), 2)
        elif command_type == 'OPENURL':
            self.openurl(a.getValue())
        elif command_type == 'SCREENSHOT':
            self.screenshot(a.getValue())
        elif command_type == 'CLEARTEXTABLE':
            if a.getValue() == None:
                rStr = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
            else:
                rStr = a.getValue()
            self.clear_fill_in_text(a.getXpathStr(), rStr)
        elif command_type == 'CLEARTEXTABLETAB':
            if a.getValue() == None:
                rStr = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
            else:
                rStr = a.getValue()
            self.clear_fill_in_text_tab(a.getXpathStr(), rStr)
        elif command_type == 'TEXTABLE-ENTER':
            if a.getValue() == None:
                rStr = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
            else:
                rStr = a.getValue()
            self.fill_in_text_enter(a.getXpathStr(), rStr)
        elif command_type == 'COMPAREPNG':
            arguments = eval(a.getValue())
            filenameA = arguments[0]
            filenameB = arguments[1]
            cv = ComputerVision()
            result = cv.diff(filenameA, filenameB)
            assert result, 'Difference between %s and %s' % (filenameA, filenameB)
        elif command_type == 'WAIT':
            time.sleep(int(a.getValue()))
        elif command_type == 'SCROLLTOP':
            self.driver.execute_script("window.scrollTo(0,0);")
        elif command_type == 'DUMMY':
            #command for testing purposes
            pass
        else:
            assert False, "unknown command"

class AbstractPage(Command):

    def __init__(self, driver, sleepTime=20, pollFrequency=1):
        super(AbstractPage, self).__init__(driver)
        self.sleepTime = sleepTime
        self.pollFrequency = pollFrequency

    def WaitUntilLoaded(self):
        aList = self.xPathWaitForList()
        for item in aList:
            wait = WebDriverWait(self.driver, self.sleepTime, poll_frequency=self.pollFrequency,
                                 ignored_exceptions=[ElementNotVisibleException])
            element = wait.until(ec.presence_of_all_elements_located((By.XPATH, item)))
            time.sleep(self.sleepTime)
        return True

    def xPathWaitForList(self):
        raise NotImplementedError()

    def __fillInTextAtIndex__(self, xpathStr, text, index=0):
        element = WebDriverWait(self.driver, 120).until(ec.visibility_of_all_elements_located((By.XPATH, xpathStr)))
        actions = ActionChains(self.driver)
        actions.move_to_element(element[index]).perform()
        actions.click()
        actions.send_keys(text)
        actions.perform()
