"""Chrome."""

from typing import List, Optional

import selenium.webdriver
from selenium.webdriver.chrome.options import Options

from surferrr.base.base_browser import BaseBrowser

ARGUMENT_HEADLESS = '--headless'


class Chrome(BaseBrowser):
    """Chrome."""

    def __init__(self,
                 headless: bool = False,
                 binary_path: Optional[str] = None,
                 driver_path: Optional[str] = None,
                 arguments: Optional[List[str]] = None) -> None:
        """Initialize object.

        Args:
            headless (bool): Headless or not. Default to False.
            binary_path (str, optional): Binary path.
            driver_path (str, optional): Driver path.
            arguments (List[str], optional): Arguments.
        """
        super().__init__(binary_path=binary_path, arguments=arguments)
        self.headless = headless
        self.driver_path = driver_path if driver_path else 'chromedriver'
        if self.headless:
            self.arguments.append(ARGUMENT_HEADLESS)

    def launch(self) -> None:
        """Launch browser."""
        options = Options()

        if self.binary_path:
            options.binary_location = self.binary_path

        for arg in self.arguments:
            options.add_argument(arg)

        self.driver = selenium.webdriver.Chrome(self.driver_path,
                                                options=options)

        if self.headless:
            user_agent = self.get_user_agent().replace('Headless', '')
            d = {
                'userAgent': user_agent,
                # 'platform': 'Windows',
            }
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', d)
