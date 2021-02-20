class FetchByDateError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class SessionModeError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class TokenRefreshError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class UnexpectetTokenError(Exception):
    def __init__(self, msg):
        super().__init__(msg)