class ConnectionException(Exception):
    """
    Exception for failed connections to the WEASEL-API
    """
    pass


class InvalidTokenException(Exception):
    """
    Exception for authorization errors based on a false token
    """
    pass
