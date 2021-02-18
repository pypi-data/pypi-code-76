# -*- coding: utf-8 -*-

__doc__ = """This module implements the webdriver.

The selenium based websdriver is useful for navigating through
webpages.
"""

import pathlib
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        ElementNotInteractableException)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from .wait import element_wait
from ._base import Scraper


class Webdriver(Scraper):
    """The `Webdriver` class.
    """

    def __init__(self, url: str, headless: bool = True) -> None:
        """Init the class.

        Parameters
        ----------
        url : str
            The url which should be loaded.
        headless : bool, optional
            Determine if the browser should be executed
            without opening a window, by default True.

        """
        super().__init__()
        # define the path to the driver
        self._path = pathlib.Path("./scraper/drivers/geckodriver.exe")
        # set some options using the built-in Options class
        options = Options()
        options.headless = headless
        # define the engine, i.e. the browser to be used
        self._engine = webdriver.Firefox(
            options=options, executable_path=self._path)
        self.url = url
        # define a strategy dictionary
        self._strategy_dic = {
            "id": By.ID,
            "xpath": By.XPATH,
            "link_text": By.LINK_TEXT,
            "partial_link_test": By.PARTIAL_LINK_TEXT,
            "name": By.NAME,
            "tag_name": By.TAG_NAME,
            "class_name": By.CLASS_NAME,
            "css_selector": By.CSS_SELECTOR,
        }
        # define a timeout
        self._timeout = 10

    def __enter__(self) -> None:
        self.load()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager and ensure that the connection is closed.

        Parameters
        ----------
        exc_type : [type]
            The  execution type.
        exc_val : [type]
            The execution value.
        exc_tb : [type]
            The execution traceback.

        """
        self._engine.quit()

    @property
    def engine(self) -> webdriver.Firefox:
        """Get the current engine.

        Returns
        -------
        webdriver
            The current engine.

        """
        return self._engine

    def click_hyperlink(self, hyperlink) -> None:
        """Click a hyperlink object.

        Parameters
        ----------
        hyperlink : selenium.webdriver.Webelement
            A selenium webelement representing a hyperlink.

        References
        ----------
        [1] https://sqa.stackexchange.com/questions/13792/how-to-proceed-after-clicking-a-link-to-new-page-in-selenium-in-python

        """
        try:
            hyperlink.click()
        except ElementClickInterceptedException:
            self._engine.execute_script("arguments[0].click();", hyperlink)
        except ElementNotInteractableException:
            self._engine.execute_script(
                "return arguments[0].scrollIntoView(true);", hyperlink)
            self._engine.execute_script("arguments[0].click();", hyperlink)
        finally:
            window_after = next(
                iter(self._engine.window_handles), self._engine.window_handles[0])
            self._engine.switch_to.window(window_after)

    def parse(  # pylint: disable=arguments-differ
            self,
            by_strat: Optional[str],
            **kwargs: dict
    ) -> list:
        """Find all <object></object> html elements in the given
        html page or in the given webelement.

        Parameters
        ----------
        by_strat : str or None
            Determine a by-strategy by which the given element
            should be searched for value.
            Can be one of the following:
            * "id"
            * "xpath"
            * "link_text"
            * "partial_link_test"
            * "name"
            * "tag_name"
            * "class_name"
            * "css_selector"

        Other Parameters
        ----------------
        element : selenium.webdriver.webelement
            The webelement which should be searched.
        val : str or None
            The value of the table element corresponding to the type
            of strategy chosen, see [1]. If `val` is None, then the html
            is returned.
        condition_type : str
            See the docs for `element_wait()`.

        Returns
        -------
        list
            A list containing the selenium.webdriver.webelements.
            If the index, i.e. `idx` is set to a single value,
            i.e. an integer, then the webdriver element is directly returned.

        Notes
        -----
        - This function extracts all content in the table:

        .. highlight:: html
        .. code-block:: html

            <object>
                content
            </object>

        - If no by strategy is given, the default is set to CSS_SELECTOR.
        - If a specific element is chosen, the val parameter has to be adapted
          to the by strategy, which is set to CSS_SELECTOR if set to None,
          thus the val parameter has to be as CSS_SELECTOR.
        - If no kwargs are given, the whole html element is searched for <object></object>.

        References
        ----------
        .. [1] https://selenium-python.readthedocs.io/locating-elements.html

        """
        by_strat = self._strategy_dic.get(by_strat, By.CSS_SELECTOR)
        element = kwargs.get("element", self._engine)
        val = kwargs.get("val", "html")
        condition_type = kwargs.get("condition_type", "presence_all")
        # get the object
        obj = element_wait(
            element=element,
            time=self._timeout,
            by_strat=by_strat,
            val=val,
            condition_type=condition_type
        )
        return obj

    def load(self) -> None:  # pylint: disable=arguments-differ
        """Load the given url.

        Notes
        -----
        This method has to be called before making any other operations
        on the webpage, otherwise the url will not be
        loaded into to driver object.

        """
        self._engine.get(self._url)
