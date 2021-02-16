import requests

from cguard.access_manager.access_manager import AccessManager


class LocalGuardAccessManager(AccessManager):
    def __init__(self):
        pass

    def request_access(self):
        res = requests.post("http://localhost:5000/approvals")

    def check_access(self):
        res = requests.get("http://localhost:5000/approvals/123?delay=7")
        if res.status_code == 200:
            return True
        else:
            return False
