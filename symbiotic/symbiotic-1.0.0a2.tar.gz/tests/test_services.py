from enum import Enum
from unittest import TestCase, mock

import pytest
import schema
from symbiotic.services import IFTTT


class StatusCodes(Enum):
    # pylint: disable=unsubscriptable-object
    # the above to suppress errors for the instance methods
    # https://github.com/PyCQA/pylint/issues/2063

    OK = (200, 'ok')
    NO_CONTENT = (204, 'no_content')
    BAD_REQUEST = (400, 'bad_request')
    UNAUTHORIZED = (401, 'unauthorized')
    FORBIDDEN = (403, 'forbidden')
    NOT_FOUND = (404, 'not_found')
    INVALID_PARAMETERS = (422, 'invalid_parameters')
    INTERNAL_SERVER_ERROR = (500, 'internal_server_error')
    BAD_GATEWAY = (502, 'bad_gateway')

    @staticmethod
    def by_reason(reason: str) -> 'StatusCodes':
        for item in StatusCodes:
            if reason == item.value[1]:
                return item
        raise Exception(f'Reason not found in status codes: {reason}')

    @staticmethod
    def has_reason(reason: str) -> str:
        values = set(item.value[1] for item in StatusCodes)
        return reason in values

    @property
    def code(self) -> int:
        return self.value[0]

    @property
    def reason(self) -> str:
        return self.value[1]


def ifttt_service_valid_key() -> IFTTT:
    config = {'key': 'clearly_a_valid_key'}
    return IFTTT(config=config)


def ifttt_service_invalid_key() -> IFTTT:
    config = {'key': 'clearly_an_invalid_key'}
    return IFTTT(config=config)


@mock.patch('symbiotic.services.requests.post', autospec=True)
class Test_IFTTT_Unit(TestCase):

    def test_trigger_valid_request_no_params(self, mock_post):
        ifttt = IFTTT(config={'key': 'valid_key'})
        response = ifttt.trigger(event_name='name')
        self.assertTrue(response.success)

    def test_trigger_valid_request_with_params1(self, mock_post):
        ifttt = IFTTT(config={'key': 'valid_key'})
        response = ifttt.trigger(event_name='name', parameters={'value1': 42})
        self.assertTrue(response.success)

    def test_trigger_valid_request_with_params2(self, mock_post):
        ifttt = IFTTT(config={'key': 'valid_key'})
        response = ifttt.trigger(event_name='name', parameters={'value2': 42, 'value3': 'some-value'})
        self.assertTrue(response.success)

    def test_trigger_valid_request_with_params3(self, mock_post):
        ifttt = IFTTT(config={'key': 'valid_key'})
        response = ifttt.trigger(event_name='name', parameters={})
        self.assertTrue(response.success)

    def test_trigger_valid_request_with_params4(self, mock_post):
        ifttt = IFTTT(config={'key': 'valid_key'})
        response = ifttt.trigger(event_name='name', parameters={})
        self.assertTrue(response.success)

    def test_trigger_valid_request_with_params5(self, mock_post):
        ifttt = IFTTT(config={'key': 'valid_key'})
        with pytest.raises(schema.SchemaUnexpectedTypeError):
            ifttt.trigger(event_name='name', parameters='test')

    def test_trigger_valid_request_with_params6(self, mock_post):
        ifttt = IFTTT(config={'key': 'valid_key'})
        with pytest.raises(TypeError):
            ifttt.trigger(event_name='name', color='black')

    def test_trigger_valid_request_with_params7(self, mock_post):
        ifttt = IFTTT(config={'key': 'valid_key'})
        with pytest.raises(schema.SchemaWrongKeyError):
            ifttt.trigger(event_name='name', parameters={'value1': 'some-value', 'value4': 55})

    def test_trigger_valid_request_with_params8(self, mock_post):
        ifttt = IFTTT(config={'key': 'valid_key'})
        with pytest.raises(schema.SchemaWrongKeyError):
            ifttt.trigger(event_name='name', parameters={'value1': 'some-value', 'sheep': 'baaah'})
