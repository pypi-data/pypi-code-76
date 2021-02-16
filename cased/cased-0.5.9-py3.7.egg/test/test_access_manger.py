import cguard

from cguard.access_manager import CasedGuardAccessManager
from cguard.requestor import GuardRequestor
from cguard.test.util import mock_response


class TestAccessManager(object):
    def test_access_manager_creation(self):
        access_manager = CasedGuardAccessManager()
        assert access_manager.requestor.__class__ == GuardRequestor

    def test_access_manager_check_access_approval(self):
        with mock_response():
            access_manager = CasedGuardAccessManager()

            assert access_manager.check_access(
                "app_123", "token_123", "session_abc", "user_abc"
            )

            cguard.requestor.HTTPClient.make_request.assert_called_with(
                "get",
                "https://api.cased.com/guard/sessions/session_1234?user_token=user_12345",
                data={
                    "guard_application_id": "test-app",
                },
                key="12345",
            )
