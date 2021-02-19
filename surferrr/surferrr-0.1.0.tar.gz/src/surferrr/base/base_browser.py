"""Base browser."""

from abc import ABC, abstractmethod
import time
from types import TracebackType
from typing import cast, List, Optional, Type

from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver
from selenium.webdriver.remote.webelement import WebElement


class BaseBrowser(ABC):
    """Base browser.."""

    max_wait = 3
    wait_interval = 1
    driver: selenium.webdriver.remote.webdriver.WebDriver

    def __init__(self,
                 binary_path: Optional[str] = None,
                 arguments: Optional[List[str]] = None) -> None:
        """Initialize object.

        Args:
            binary_path (str, optional): Binary path.
            arguments (List[str], optional): Arguments.
        """
        self.binary_path = binary_path
        self.arguments = arguments if arguments else []

    def __enter__(self) -> 'BaseBrowser':
        """Enter with statement.

        Returns:
            BaseBrowser: Browser.
        """
        self.launch()
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]):
        """Enter with statement.

        Args:
            exc_type (Optional[Type[BaseException]]): Exception type.
            exc_value (Optional[BaseException]): Exception.
            traceback (Optional[TracebackType]): Traceback.
        """
        self.shutdown()

    def get_url(self) -> str:
        """Get URL.

        Returns:
            str: URL.
        """
        return self.driver.current_url

    def get_content(self) -> str:
        """Get page content.

        Returns:
            str: Content.
        """
        return self.driver.page_source

    @abstractmethod
    def launch(self) -> None:
        """Launch browser.

        Raises:
            NotImplementedError: Not implemented.
        """
        raise NotImplementedError('This method was implemented.')

    def shutdown(self) -> None:
        """Shutdown browser."""
        self.driver.quit()

    def access(self, url: str) -> None:
        """Access.

        Args:
            url (str): URL.
        """
        self.driver.get(url)

    def get_user_agent(self) -> str:
        """Get userAgent.

        Returns:
            str: userAgent.
        """
        return self.driver.execute_script('return navigator.userAgent;')

    def get_element(self,
                    xpath: str,
                    max_wait: Optional[int] = None) -> WebElement:
        """Get web element.

        Args:
            xpath (str): XPath.
            max_wait (int, optional): Max wait.

        Raises:
            NoSuchElementException: Cannot get element.

        Returns:
            WebElement: Target element.
        """
        if not max_wait:
            max_wait = self.max_wait

        e = None
        last_err = None
        for _ in range(max_wait + 1):
            try:
                e = self.driver.find_element_by_xpath(xpath)
                break
            except NoSuchElementException as err:
                last_err = err
                print('retry...')
                time.sleep(self.wait_interval)
        else:
            if last_err:
                raise NoSuchElementException(
                    msg=last_err.msg,
                    screen=last_err.screen,
                    stacktrace=last_err.stacktrace,
                )

            raise NoSuchElementException()

        return cast(WebElement, e)

    def type_text(self,
                  xpath: str,
                  keys: str,
                  max_wait: Optional[int] = None) -> WebElement:
        """Type text.

        Args:
            xpath (str): XPath.
            keys (str): Keys.
            max_wait (int, optional): Max wait.

        Returns:
            WebElement: Target element.
        """
        e = self.get_element(xpath, max_wait=max_wait)
        e.send_keys(keys)
        return e

    def submit(self, xpath: str, max_wait: Optional[int] = None) -> WebElement:
        """Submit.

        Args:
            xpath (str): XPath.
            max_wait (int, optional): Max wait.

        Returns:
            WebElement: Target element.
        """
        e = self.get_element(xpath, max_wait=max_wait)
        e.submit()
        return e

    def click(self, xpath: str, max_wait: Optional[int] = None) -> WebElement:
        """Click.

        Args:
            xpath (str): XPath.
            max_wait (int, optional): Max wait.

        Returns:
            WebElement: Target element.
        """
        e = self.get_element(xpath, max_wait=max_wait)
        e.click()
        return e

    def capture(self, output_path: str) -> None:
        """Capture window.

        Args:
            output_path (str): Output path.
        """
        self.driver.get_screenshot_as_file(output_path)

    def get_text(self, xpath: str, max_wait: Optional[int] = None) -> str:
        """Get text.

        Args:
            xpath (str): XPath.
            max_wait (int, optional): Max wait.

        Returns:
            str: Result.
        """
        e = self.get_element(xpath, max_wait=max_wait)
        return e.text
