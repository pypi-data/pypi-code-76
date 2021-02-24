class CircleCIException(RuntimeError):
    def __init__(self, message: str, *args, status_code: int = 1, **kwargs):
        self.status_code = status_code
        super().__init__(message, *args)
