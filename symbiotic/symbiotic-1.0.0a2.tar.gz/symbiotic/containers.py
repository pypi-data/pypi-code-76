from dependency_injector import containers, providers
from gpiozero.pins.pigpio import PiGPIOFactory

from .devices import LightBulb
from .event_bus import EventBus
from .sensors import GPIOMotionSensor
from .services import IFTTT


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # It's not possible to pass the root config 'config.services'
    # because, if the configuration does not contain the service's
    # config (e.g. IFTTT), any object trying to call that service will
    # throw "AttributeError: 'NoneType' object has no attribute 'get'"
    IFTTT = providers.Singleton(IFTTT, config=config.IFTTT)


class DeviceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    light_bulb: LightBulb = providers.Factory(LightBulb)


class SensorContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    event_bus = providers.Dependency(instance_of=EventBus)

    pin_factory = providers.FactoryAggregate(
        pigpio=providers.Factory(
            PiGPIOFactory,
            host=config.pigpio.host,
            port=config.pigpio.port
        ),
    )

    gpio_motion_sensor: GPIOMotionSensor = providers.Factory(
        GPIOMotionSensor,
        event_bus=event_bus
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    event_bus = providers.Dependency(instance_of=EventBus)

    devices: DeviceContainer = providers.Container(
        DeviceContainer,
        config=config.devices,
    )

    sensors: SensorContainer = providers.Container(
        SensorContainer,
        config=config.sensors,
        event_bus=event_bus,
    )

    services: ServiceContainer = providers.Container(
        ServiceContainer,
        config=config.services,
    )
