class ConfigurationError(Exception):
    def __init__(self, message, *args):

        # Call the base class constructor with the parameters it needs
        super().__init__(message, *args)
