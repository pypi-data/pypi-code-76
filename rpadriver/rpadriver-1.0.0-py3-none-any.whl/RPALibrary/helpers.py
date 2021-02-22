"""
Utility functions for TOSLibrary.
"""
import signal
import re
import time
from typing import List

import robot
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Screenshot import Screenshot

from tos.settings import PLATFORM
from .exceptions import AbortException
from . import messages


def handle_dead_selenium():
    """
    If selenium/chromedriver is killed on purpose or by error,
    stop the robot execution to prevent unnecessary retrying.
    """
    # TODO: find a way to use this automatically in a sensible way.
    # Selenium existence should be enforced only in stages
    # where selenium is used!
    try:
        selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
    except Exception:
        logger.debug(
            "Not checking webdriver existence as SeleniumLibrary was not found"
        )
        return
    status = get_webdriver_status(selenium_lib)
    if status == "dead":  # alive means an open chrome window
        raise RuntimeError(messages.WEBDRIVER_DEAD)


def get_webdriver_status(selenium_lib):
    from selenium.webdriver.remote.command import Command
    try:
        selenium_lib.driver.execute(Command.STATUS)
    except Exception:
        return "dead"
    return "alive"


def handle_signals():
    """Listen for TERM / INT signals and handle appropriately"""
    # TODO: find a way to test catching SIGINT/KeyboardInterrupt
    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigint_handler)


def sigint_handler(signum, frame):
    """Detect SIGINT or Keyboard interrupt signals.

    Pass the information as exception message to ``action_on_fail``
    later on to be handled.
    """
    raise AbortException(messages.SIGINT_MESSAGE)


def sigterm_handler(signum, frame):
    """Detect SIGTERM signals.

    Pass the information as exception message to ``action_on_fail``
    later on to be handled.
    """
    raise AbortException(messages.SIGTERM_MESSAGE)


def take_screenshot():
    """Take screenshot of all visible screens.

    Use Robot Framework standard library with Scrot screenshotting utility.
    """
    if PLATFORM == "Linux":
        module = "Scrot"  # NOTE: needs Scrot to be installed with apt-get or similar
    elif PLATFORM == "Windows":  # pragma: no cover
        module = "Pil"
    else:  # pragma: no cover
        logger.warn("Screenshotting is supported only on Windows and Linux")
        return
    try:
        Screenshot(screenshot_module=module).take_screenshot()
    except robot.libraries.BuiltIn.RobotNotRunningError as err:
        logger.warn(
            f"Robot needs to be running for screenshotting to work: {str(err)}")
    except Exception:  # pragma: no cover
        logger.warn("You need to install Scrot on Linux and Pil on Windows")


def repeat_call_until(*args, **kwargs):
    """Repeat given function or method call until given condition is True.

    :param kwargs:

        - **callable** (func) - Callable method or function (required).

        - **condition** (func) - Condition to wait for (required)

        - **arguments** (tuple) - Tuple of arguments to pass for the callable.

        - **kwarguments** (dict) - Dict of kw arguments to pass for the callable.

        - **limit** (int) - limit for retries.

        - **sleep** (int) - time to sleep between retries.


    Usage:

    .. code-block:: python

        class RobotLibrary:
            '''Example RF library with retry condition as a method.'''
            def btn1_is_enabled(self):
                return browser.find_element_by_name("btn1").is_enabled()

            @keyword
            def retry_clicking_until_success(self):
                repeat_call_until(
                    callable=BuiltIn().run_keyword,
                    condition=self.btn1_is_enabled,
                    arguments=("SeleniumLibrary.Click Element", "btn2"),
                    limit=5
                )
    """
    required_kwargs = ("callable", "condition")

    if not all(kwarg in kwargs for kwarg in required_kwargs):
        raise TypeError(f"Missing required kwargs {required_kwargs}")

    func = kwargs["callable"]
    condition = kwargs["condition"]
    limit = kwargs.get("limit", 3)
    sleep = kwargs.get("sleep", 1)

    counter = 0
    while not condition():
        if counter <= limit:
            value = func(
                *kwargs.get("arguments", ()),
                **kwargs.get("kwarguments", {})
            )
        else:
            raise RuntimeError(
                f"Tried to retry action {str(func)} {limit} times without success."
            )
        counter += 1
        time.sleep(sleep)

    return value


def get_stage_from_tags(tags: List) -> int:
    """Get the stage number from the stage tag.

    It is required that the stage tags include one tag of the form 'stage_0'.

    Example:

        >>> tags = ["stage_0", "repeat"]
        >>> get_stage_from_tags(tags)
        0

    """
    try:
        stage_tag = next(filter(lambda tag: tag.startswith("stage_"), tags))
        return int(re.search(r"\d+", stage_tag).group())
    except (StopIteration, ValueError):
        raise ValueError
