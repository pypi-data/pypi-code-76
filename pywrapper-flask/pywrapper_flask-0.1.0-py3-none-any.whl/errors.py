class StandardError(Exception):
    """
    Error that serializes to a human readable 400 status code
    """
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code

        if code < 400 or code > 499:
            raise ValueError(f'Invalid code {code}. Must be a 4XX error')

    def __str__(self) -> str:
        return self.message
