from src.driver.by import By


class HTMLBy(By):
    pass

    """
	Constructs a CSS based locator to search for within your html 5 application.

	:param css_locator: - String The css locator to look for.
	:returns: The constructed locator
	"""

    def css(self, css_locator):
        return "By.CSS: " + css_locator

    """
	Constructs an XPath based locator to search for within your html 5 application.
	
	:param xpath_locator: The xpath to look for.
	:returns: The constructed locator
	"""

    def xpath(self, xpath_locator):
        return "By.XPath: " + xpath_locator
