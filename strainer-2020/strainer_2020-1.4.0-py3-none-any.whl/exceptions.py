class ValidationException(Exception):
    """Exception that keeps all validation errors.
    """
    def __init__(self, errors):
        super().__init__()
        self.errors = errors

    def __str__(self):
        return str(self.errors)
