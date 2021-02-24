"""An improved version of the pactman handler, that has better request matching."""

import urllib.parse

from pactman.mock.mock_urlopen import MockURLOpenHandler as OriginalMockURLOpenHandler
from pactman.mock.pact_request_handler import RecordResult, Request
from pactman.verifier.verify import RequestVerifier
from urllib3.response import HTTPResponse


class MockURLOpenHandler(OriginalMockURLOpenHandler):
    def validate_request(self, method: str) -> HTTPResponse:  # pragma: no cover
        url_parts = urllib.parse.urlparse(self.path)

        # Only modification from the original `validate_request`: we add the `method` arg to `get_interaction`
        interaction = self.get_interaction_from_path(method=method, path=url_parts.path)

        body = self.get_body()

        request = Request(method, url_parts.path, url_parts.query, self.headers, body)
        result = RecordResult()
        RequestVerifier(self.pact, interaction['request'], result).verify(request)

        if not result.success:
            return self.handle_failure(result.reason)
        self.handle_success(interaction)
        if self.pact.file_write_mode != 'never':
            self.write_pact(interaction)
        return self.respond_for_interaction(interaction)

    def get_interaction_from_path(self, method: str, path: str):
        # This is our custom way to `get_interaction` to improve the original way (which is `self.interactions.pop()`)
        matched_interactions = []

        for interaction in self.interactions:
            interaction_method = interaction['request']['method'].lower()
            interaction_path = interaction['request']['path'].lower()
            if interaction_method == method.lower() and interaction_path == path.lower():
                matched_interactions.append(interaction)

        if len(matched_interactions) > 1:
            raise AssertionError(f'Request {method} at {path} received, several interactions matching')
        elif not matched_interactions:
            raise AssertionError(f'Request {method} at {path} received, no interaction matching')
        return matched_interactions[0]
