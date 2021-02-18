import cased

from cguard.access_manager.access_manager import AccessManager


class TestGuardAccessManager(AccessManager):
    def __init__(self):
        pass

    def request_access(self):
        return True

    def check_access(self):
        return True
