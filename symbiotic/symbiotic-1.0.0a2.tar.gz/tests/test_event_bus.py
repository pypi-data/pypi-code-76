from typing import Set, Callable
from unittest import TestCase, mock

import io
import pytest

from symbiotic.event_bus import EventBusAdapter

EVENT_NAME: str = 'test-event'


@pytest.fixture
def mock_function():
    pass


class Test_EventBus(TestCase):

    def setUp(self) -> None:
        self.event_bus: EventBusAdapter = EventBusAdapter()
        self.assertIsNotNone(self.event_bus)

    def event_subscribers(self, event_name) -> Set[Callable]:
        return self.event_bus._bus._events[event_name]

    @pytest.mark.usefixtures('mock_function')
    def test_subscribe_func_to_event(self):
        self.event_bus.subscribe_func_to_event(mock_function, EVENT_NAME)
        event_subscribers = self.event_subscribers(EVENT_NAME)
        expected: set = {mock_function}
        self.assertEqual(expected, event_subscribers)

    @pytest.mark.usefixtures('mock_function')
    def test_unsubscribe_func_from_event(self):
        self.event_bus.subscribe_func_to_event(mock_function, EVENT_NAME)
        self.event_bus.unsubscribe_func_from_event(mock_function, EVENT_NAME)
        self.assertEqual(set(), self.event_subscribers(EVENT_NAME))

    def test_emit_event(self):
        mock_func_result = 'mock_function called'
        expected_result = 'mock_function called\n'

        def mock_func_print():
            print(mock_func_result)

        with mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.event_bus.subscribe_func_to_event(mock_func_print, EVENT_NAME)
            self.event_bus.emit(EVENT_NAME)
            self.assertEqual(expected_result, mock_stdout.getvalue())
