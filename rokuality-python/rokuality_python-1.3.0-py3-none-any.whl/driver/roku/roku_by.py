from src.driver.by import By

class RokuBy(By):
    pass

    """
	Constructs a text based locator to search for within the text on the device screen.

	:param text: - String The text to search for on the device screen, i.e. "hello world"
	:returns: The constructed locator
	"""

    def text(self, text):
        return "RokuBy.Text: " + text

    """
	Constructs an attribute/value based locator to search for within the the device screen.

	:param attribute: The attribute to search for on the device screen, i.e. "index"
	:param value: The attributes value to search for on the device screen, i.e. "0"
	:returns: The constructed locator
	"""

    def attribute(self, attribute, value):
        return "RokuBy.Attribute: " + attribute + "::::::::" + value

    """
	Constructs an attribute/value based locator to search for within the the device screen.
	
	:param tag: The tag to search for on the device screen, i.e. "Label"
	:returns: The constructed locator
	"""

    def tag(self, tag):
        return "RokuBy.Tag: " + tag
