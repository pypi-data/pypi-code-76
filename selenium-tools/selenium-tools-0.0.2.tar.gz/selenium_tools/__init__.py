"""# API"""

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from datetime import datetime

def click_range(driver, range_, target, horizontal=True, tol=0, max_iter=10):
    """
    Click a range slider to a desired target value.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver or other webdriver
        Webdriver in which the form is open.

    range_ : selenium.webdriver.remote.webelement.WebElement
        The range slider to be clicked.

    target : float
        Target value to which the sider should be dragged.

    horizontal : bool, default=True
        Indicates the slider is oriented horizontally, as opposed to 
        vertically.

    tol : float, default=0
        Tolerance for error if the slider cannot be dragged to the exact 
        target.

    max_iter : int, default=10
        Maximum number of iterations for the slider to reach the target.

    Returns
    -------
    delta : float
        Remaining difference between the target and actual value.

    Examples
    --------
    ```python
    from selenium_tools import click_range
    
    from selenium.webdriver import Chrome

    driver = Chrome()
    driver.get('data:text/html,<input type="range">')
    range_ = driver.find_element_by_css_selector('input[type=range]')
    click_range(driver, range_, 80)
    range_.get_property('value')
    ```

    Out:

    ```
    '80'
    ```
    """
    size = range_.size['width'] if horizontal else range_.size['height']
    max_ = float(range_.get_attribute('max') or 100)
    min_ = float(range_.get_attribute('min') or 0)
    ac = ActionChains(driver)
    ac.move_to_element(range_).perform()
    for _ in range(max_iter):
        value = float(range_.get_property('value'))
        if abs(value-target) <= tol:
            break
        offset = (target-value) * size / (max_-min_)
        xoffset, yoffset = (offset, 0) if horizontal else (0, -offset)
        ac.move_to_element(range_).move_by_offset(xoffset, yoffset).click()\
            .perform()
    return target - float(range_.get_property('value'))

def click_slider_range(driver, range_, target, horizontal=True, tol=0, max_iter=10):
    """
    Click a <a href="https://github.com/seiyria/bootstrap-slider" target="_blank">
    bootstrap range slider</a> to a desired target value.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver or other webdriver
        Webdriver in which the form is open.

    range_ : selenium.webdriver.remote.webelement.WebElement
        The range slider to be clicked.

    target : float
        Target value to which the sider should be dragged.

    horizontal : bool, default=True
        Indicates the slider is oriented horizontally, as opposed to 
        vertically.

    tol : float, default=0
        Tolerance for error if the slider cannot be dragged to the exact 
        target.

    max_iter : int, default=10
        Maximum number of iterations for the slider to reach the target.

    Returns
    -------
    delta : float
        Remaining difference between the target and actual value.

    Examples
    --------
    ```python
    from selenium_tools import click_range_slider
    
    from selenium.webdriver import Chrome

    driver = Chrome()
    driver.get('https://my-url/')
    range_ = driver.find_element_by_css_selector('#my-slider-id')
    drag_range(driver, range_, 80)
    range_.get_property('value')
    ```

    Out:

    ```
    '80'
    ```
    """
    data_slider_id = range_.get_attribute('data-slider-id')
    data_slider = driver.find_element_by_id(data_slider_id)
    handle = data_slider.find_element_by_class_name('min-slider-handle')
    size = data_slider.size['width']
    max_ = float(handle.get_attribute('aria-valuemax'))
    min_ = float(handle.get_attribute('aria-valuemin'))
    ac = ActionChains(driver)
    for _ in range(max_iter):
        value = float(range_.get_property('value'))
        if abs(value-target) <= tol:
            break
        offset = (target-value) * size / (max_-min_)
        xoffset, yoffset = (offset, 0) if horizontal else (0, -offset)
        ac.move_to_element(handle).move_by_offset(xoffset, yoffset).click()\
            .perform()
    return target - float(range_.get_property('value'))

def drag_range(driver, range_, target, horizontal=True, tol=0, max_iter=10):
    """
    Drag a range slider to a desired target value.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver or other webdriver
        Webdriver in which the form is open.

    range_ : selenium.webdriver.remote.webelement.WebElement
        The range slider to be dragged.

    target : float
        Target value to which the sider should be dragged.

    horizontal : bool, default=True
        Indicates the slider is oriented horizontally, as opposed to 
        vertically.

    tol : float, default=0
        Tolerance for error if the slider cannot be dragged to the exact 
        target.

    max_iter : int, default=10
        Maximum number of iterations for the slider to reach the target.

    Returns
    -------
    delta : float
        Remaining difference between the target and actual value.

    Examples
    --------
    ```python
    from selenium_tools import drag_range
    
    from selenium.webdriver import Chrome

    driver = Chrome()
    driver.get('data:text/html,<input type="range">')
    range_ = driver.find_element_by_css_selector('input[type=range]')
    drag_range(driver, range_, 80)
    range_.get_property('value')
    ```

    Out:

    ```
    '80'
    ```
    """
    size = range_.size['width'] if horizontal else range_.size['height']
    max_ = float(range_.get_attribute('max') or 100)
    min_ = float(range_.get_attribute('min') or 0)
    ac = ActionChains(driver)
    ac.click_and_hold(range_).perform()
    for _ in range(max_iter):
        value = float(range_.get_property('value'))
        if abs(target - value) <= tol:
            break
        offset = (target-value) * size / (max_-min_)
        xoffset, yoffset = (offset, 0) if horizontal else (0, -offset)
        ac.move_by_offset(xoffset, yoffset).perform()
    ac.release().perform()
    return target - float(range_.get_property('value'))

def send_datetime(input_, datetime_):
    """
    Send a datetime object to a form input.

    Parameters
    ----------
    input_ : selenium.webdriver.remote.webelement.WebElement
        The form input to which the datetime object will be sent.

    datetime_ : datetime.datetime
        The datetime object to be sent.

    Examples
    --------
    ```python
    from selenium_tools import send_datetime

    from selenium.webdriver import Chrome

    from datetime import datetime

    driver = Chrome()
    driver.get('data:text/html,<input type="date">')
    input_ = driver.find_element_by_css_selector('input[type=date]')
    send_datetime(input_, datetime.utcnow())
    ```

    You should see the current date entered in the date input field in your 
    browser.
    """
    return html_selenium[input_.get_attribute('type')](input_, datetime_)

def _send_date(input_, datetime_):
    return input_.send_keys(datetime_.strftime('%m%d%Y'))

def _send_datetime_local(input_, datetime_):
    date = datetime_.strftime('%m%d%Y')
    time = datetime_.strftime('%I%M%p')
    return input_.send_keys(date, Keys.TAB, time)

def _send_month(input_, datetime_):
    month = datetime_.strftime('%B')
    year = datetime_.strftime('%Y')
    return input_.send_keys(month, Keys.TAB, year)

def _send_time(input_, datetime_):
    return input_.send_keys(datetime_.strftime('%I%M%p'))

def _send_week(input_, datetime_):
    return input_.send_keys(datetime_.strftime('%U%Y'))

html_selenium = {
    'date': _send_date,
    'datetime-local': _send_datetime_local,
    'month': _send_month,
    'time': _send_time,
    'week': _send_week,
}

def get_datetime(input_type, response):
    """
    Get a datetime object from a form response after a POST request.

    Parameters
    ----------
    input_type : str
        Type of the input tag.

    response : str
        Response to the input tag.

    Returns
    -------
    datetime : datetime.datetime
        The response converted to a datetime object if possible, otherwise 
        the raw response. This method will fail to convert the response if 
        the input type is invalid or if the client did not enter a response 
        in this input tag.

    Examples
    --------
    ```python
    from selenium_tools import get_datetime, send_datetime

    from selenium.webdriver import Chrome

    from datetime import datetime

    driver = Chrome()
    driver.get('data:text/html,<input type="date">')
    input_ = driver.find_element_by_css_selector('input[type=date]')
    send_datetime(input_, datetime.utcnow())
    get_datetime(input_.get_attribute('type'), input_.get_property('value'))
    ```

    Out:

    ```
    datetime.datetime(2020, 6, 30, 0, 0)
    ```
    """
    format_ = html_datetime.get(input_type)
    return (
        datetime.strptime(response, format_) if response and format_
        else response
    )

html_datetime = {
    'date': '%Y-%m-%d',
    'datetime-local': '%Y-%m-%dT%H:%M',
    'month': '%Y-%m',
    'time': '%H:%M',
    'week': '%Y-W%W'
}