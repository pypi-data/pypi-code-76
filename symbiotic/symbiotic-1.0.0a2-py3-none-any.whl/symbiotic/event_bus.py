import functools
from abc import ABC, abstractmethod
from collections import Callable

from event_bus import EventBus as SimpleEventBus


class EventBus(ABC):

    @abstractmethod
    def subscribe_func_to_event(self, func: Callable, event_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def unsubscribe_func_from_event(self, func: Callable, event_name: str) -> None:
        raise NotImplementedError

    def subscribe(self, event_name: str) -> Callable:
        def event_wrapper(func):
            self.subscribe_func_to_event(func, event_name)

            @functools.wraps(func)
            def func_wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return func_wrapper

        return event_wrapper

    @abstractmethod
    def emit(self, event_name: str, *args, **kwargs) -> None:
        raise NotImplementedError


class EventBusAdapter(EventBus):

    def __init__(self):
        self._bus = SimpleEventBus()

    def subscribe_func_to_event(self, func: Callable, event_name: str) -> None:
        self._bus.add_event(func, event_name)

    def unsubscribe_func_from_event(self, func: Callable, event_name: str) -> None:
        self._bus.remove_event(func.__name__, event_name)

    def emit(self, event_name: str, *args, **kwargs) -> None:
        self._bus.emit(event_name, *args, **kwargs)


class EventSubscriber(object):

    def __init__(self, event_bus: EventBus, event_name: str):
        self.event_bus = event_bus
        self.event_name = event_name

    def do(self, func: Callable, *args, **kwargs):
        subscriber = functools.partial(func, *args, **kwargs)
        self.event_bus.subscribe_func_to_event(subscriber, self.event_name)
