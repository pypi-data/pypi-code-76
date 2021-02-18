# -*- coding: utf-8 -*-

__doc__ = """This module implements the wait.
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


CONDITION_DIC = {
    "presence": EC.presence_of_element_located,
    "clickable": EC.element_to_be_clickable,
    "selected": EC.element_to_be_selected,
    "presence_all": EC.presence_of_all_elements_located,
    "visibility": EC.visibility_of_element_located,
    "visibility_all": EC.visibility_of_all_elements_located,
    "alert_presence": EC.alert_is_present,
}


def element_wait(
        element,
        time: int,
        by_strat: str,
        val: str,
        condition_type: str
) -> webdriver.firefox.webelement.FirefoxWebElement:
    """Tell a selenium webelement to wait for `time` seconds
    until the val in element is located.

    Parameters
    ----------
    element : selenium.webdriver.webelement
        The element which is searched for val given the
        condition type and the by strategy.
    time : int
        The amount of time in seconds which should be waited.
    by_strat : str
        The by-strategy chosen.
    val : str
        The value which is searched in element given the by strategy.
    condition_type : str
        The type of condition to be applied.
        If no valid condition is given, the element waits until the value in
        element is present. Valid conditions are:

        * "presence": Wait until value in element is present.
        * "clickable": Wait until value in element is clickable.
        * "selected": Wait until value in element is selected.
        * "presence_all": Wait until all values in element are present.
        * "visibility": Wait until value in element is visible.
        * "visibility_all": Wait until all values in element are visible.
        * "alert_presence": Wait until an alert is present.

    Returns
    -------
    list
        A list containing the element(s) which was/were found,
        if no element was found, either None or an empty list is returned,
        depending on the condition chosen.

    Raises
    ------
    selenium.common.exceptions.TimeoutException
        If no element is found in the given `time`,
        then a TimeoutException is raised.

    """
    condition = CONDITION_DIC.get(
        condition_type, EC.presence_of_element_located)
    try:
        element = WebDriverWait(element, time).until(
            condition((by_strat, val)))
    except TimeoutException as timeout:
        msg = f"The value {val} which should be searched in {element} " \
              f"could not be located in {time} " \
              f"seconds given the by strategy {by_strat} " \
              f"and the condition {condition}."
        raise TimeoutException(msg) from timeout
    return element
