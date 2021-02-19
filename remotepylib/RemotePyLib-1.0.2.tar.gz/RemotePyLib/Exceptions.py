""" A Python file keeping all the exceptions raised (or to be raised) by the library """

class InvalidAccessError(Exception):
    """
    An Exception to inform the user that the key entered is incorrect and thus, Access is Denied.
    """
    def __init__(self):
        super().__init__("Access is denied. Check your Access Key and try again")


class RemoteModuleNotFoundError(Exception):
    """
    An Exception to inform the user that the remote module could not be found
    """
    def __init__(self, name):
        """
        Args:
            name (str): name of the module that could not be imported
        """
        super().__init__(f"Remote Module {name} could not be found")


class ExportError(Exception):
    """
    An Exception to inform the user that the module that was tried to be exported could not be successfully uploaded. 
    This could be due to the presence of another module with the same name present in the server
    """
    def __init__(self, name):
        """
        Args:
            name (str): name of the module that was being tried to export
        """
        super().__init__(f"Could not Export module {name} because another module with the same name was present on the server. Try renaming the module and trying again.")


class InvalidEmailError(Exception):
    """An Exception thrown when the email address entered to upload a module is invalid
    """
    def __init__(self, email, chars):
        super().__init__(f'The email address {email} is not a valid email because the following characters were not present in it: {chars}')