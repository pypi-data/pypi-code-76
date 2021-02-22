import os
from logging import getLogger
from pathlib import Path
from time import sleep
from typing import List, Union

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains, Chrome
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


logger = getLogger()


class ChromeDriver:
    def __init__(self):
        self.driver = self.__start_chrome_driver()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()

    def __del__(self):
        self.__close()

    def __close(self):
        try:
            self.driver.close()
        except Exception:
            pass

    def find_element(
        self, select: str, strategy, driver_or_element=None, first=True
    ) -> Union[List[WebElement], WebElement]:
        """
        It will find a element in the driver, following the strategy available on this module
        `downloader.adapters.strategy`
        Could be -> FindByXpath, FindById, FindByCss, FindByName, FindByClassName, FindByTagName
        :param select: String
        :param strategy: downloader.adapters.strategy
        :param driver_or_element: use an specific element or the properly driver
        :param first: Bool
        :return: List of elements, or first element, or None
        """

        driver_or_element = driver_or_element or self.driver

        return strategy.execute(select, driver_or_element, first)

    def expect_presence_of_element(
        self, select: str, strategy: By, max_wait_time: int = 5
    ) -> Union[WebElement, None]:
        """
        This method expect some condition or element exists to be truth and continue.
        To know more, see this article
        https://selenium-python.readthedocs.io/waits.html#explicit-waits
        :param select: STRING -> A selector in XPATH, ID, CSS, etc.
        :param strategy: selenium.webdriver.common.by.BY ->
                            A strategy to find some element, like:
                            By.XPATH, By.ID, etc
        :param max_wait_time: INT
        :return: WebElement
        """
        try:
            return WebDriverWait(self.driver, max_wait_time).until(
                ec.presence_of_element_located((strategy, select))
            )
        except TimeoutException:
            return None

    @staticmethod
    def fill(element, value: str, submit=False):
        element.send_keys(value)
        if submit:
            element.submit()

    def move_mouse_to_element(self, element):
        try:
            action = ActionChains(self.driver)
            action.move_to_element(element)
            action.perform()
        except Exception as err:
            logger.error(
                f"Couldn't move to element - {type(err)} - {err}"
            )

    def scroll_until_end_page(self, SCROLL_PAUSE_TIME=0.3, SCROLL_VALUE=500):
        SCROLL_PAUSE_TIME = SCROLL_PAUSE_TIME

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight;")

        x = 0
        y = SCROLL_VALUE

        SCROLL_VALUE = SCROLL_VALUE

        self.driver.execute_script("window.scrollTo(0, 0);")

        while y < last_height:
            # Scroll down to bottom
            self.driver.execute_script(f"window.scrollTo({x},{y});")

            x += SCROLL_VALUE
            y += SCROLL_VALUE

            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)

    @staticmethod
    def __start_chrome_driver() -> WebDriver:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")

        try:
            parent_path = Path(os.getcwd()).parent
            path = Path(parent_path).parent
            return Chrome(f"{path}/chromedriver", options=chrome_options)
        except (ImportError, FileNotFoundError):
            return Chrome("chromedriver", options=chrome_options)
