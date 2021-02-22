import atexit
import logging
import sys
import time
from contextlib import contextmanager

from dependency_injector import providers
from dependency_injector.providers import Configuration

from .actions import ActionScheduler
from .containers import (
    Container,
    DeviceContainer,
    SensorContainer,
    ServiceContainer,
)
from .event_bus import EventBusAdapter, EventSubscriber
from .schedule import Schedule


class Symbiotic(object):

    def __init__(self):
        self.container: Container = self.create_container()
        self._scheduler: ActionScheduler = ActionScheduler()
        atexit.register(self.shutdown)

    def create_container(self) -> Container:
        container = Container(event_bus=providers.Singleton(EventBusAdapter))
        container.config.debug.from_env('SYMBIOTIC_DEBUG')
        container.init_resources()
        container.wire(modules=[sys.modules[__name__]])
        return container

    @property
    def config(self) -> Configuration:
        return self.container.config

    @property
    def debug(self) -> bool:
        debug = self.config.debug
        if debug is not None:
            return debug
        return False

    @property
    def name(self) -> str:
        return 'Symbiotic'

    @property
    def logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)

        if self.debug and not logger.level:
            logger.setLevel(logging.DEBUG)

        return logger

    @property
    def devices(self) -> DeviceContainer:
        return self.container.devices

    @contextmanager
    def events(self, event_name: str) -> EventSubscriber:
        event_subscriber = EventSubscriber(self.event_bus, event_name)
        yield event_subscriber

    @property
    def event_bus(self):
        return self.container.event_bus()

    @contextmanager
    def scheduler(self, schedule: Schedule):
        self._scheduler.start_session(schedule)
        yield self._scheduler
        self._scheduler.end_session()

    @property
    def sensors(self) -> SensorContainer:
        return self.container.sensors

    @property
    def services(self) -> ServiceContainer:
        return self.container.services

    def run(self, sleep_interval: int = 1) -> None:
        try:
            self.logger.info(
                'The application is running... (Press CTRL+C to terminate)')
            while True:
                self._scheduler.run()
                time.sleep(sleep_interval)
        except KeyboardInterrupt:
            pass

    def shutdown(self, *args) -> None:
        # sys.stderr.write("\r")  # suppress '^C' in terminal
        # https://stackoverflow.com/a/48726537/5874339
        self.logger.info('Shutdown initiated. Please wait...')
        # Handle application shutdown here...
        self.container.shutdown_resources()
        self.logger.info('Application successfully shutdown.')
        sys.exit(0)
