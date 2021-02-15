"""Run Applications."""

import json
import logging
import sys
from enum import Enum, IntEnum
from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from time import time
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Type, Union, cast

import structlog

from kelvin.icd import Message
from kelvin.icd.model import timestamper
from kelvin.icd.utils import snake_name

from ...core.application import ApplicationInterface, DataApplication, PollerApplication
from ...core.context import ContextInterface
from ..logs import configure_logs
from ..mapping_proxy import MappingProxy
from ..utils import build_messages, get_io, inflate
from .client import CoreClient
from .connection import SyncConnection
from .response import Response

logger = structlog.get_logger(__name__)
SYS_PATH = sys.path


class LogLevel(IntEnum):
    """Logging level."""

    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    INFO = logging.INFO
    ERROR = logging.ERROR
    TRACE = logging.ERROR


class InterfaceType(str, Enum):
    """Application interface type."""

    DATA = "data"
    POLLER = "poller"

    def __str__(self) -> str:
        """Representation of value as string."""

        return str(self.value)  # pragma: no cover


class CoreClientContext(ContextInterface):
    """Core Client context."""

    def __init__(
        self,
        connection: SyncConnection,
        startup_time: float = 0.0,
        select_window: Optional[float] = 5.0,
        buffer: Optional[Sequence[Response]] = None,
    ) -> None:
        """Initialise Core Client Context."""

        core_config = MappingProxy(connection.client_config.configuration).get(
            "app.kelvin.core", {}
        )

        self._connection = connection
        self.process_time = startup_time
        self.buffer: List[Response] = [*buffer] if buffer is not None else []
        self._outputs: List[Message] = []
        self._input_registry_map = {
            item["name"]: {"data_model": item["data_model"], "name": item["name"]}
            for item in core_config.get("inputs", [])
        }
        self._output_registry_map = {
            item["name"]: {"data_model": item["data_model"], "name": item["name"]}
            for item in core_config.get("outputs", [])
        }

        self._select_window = select_window

    def get_process_time(self) -> float:
        """
        Returns the current time of the application.

        This time should be used by applications for timestamping of
        messages. This time will be the real wall time by default and
        the replay time when running in simulation mode.

        """

        return self.process_time

    def get_real_time(self) -> float:
        """
        Returns the actual time of the system clock.

        This time should be used by applications when the actual wall
        time is required.  This is typically used when timestamping
        sensor measures and computing latencies.

        """

        return time()

    def emit(self, output: Message) -> None:
        """Takes the incoming data and publishes the contents to the software
        bus."""

        self._outputs += [output]

    def get_outputs(self, clear: bool = True) -> List[Message]:
        """Get outputs."""

        outputs = self._outputs[:]
        if clear:
            self._outputs[:] = []

        return outputs

    def select(
        self,
        metric_name: str,
        window: Tuple[float, float] = (0.0, 0.0),
        limit: int = 1000,
    ) -> List[Message]:
        """Get a list of metrics from the application storage."""

        start, end = window
        request = self._connection.select([metric_name], int(start * 1e9), int(end * 1e9), limit)
        if self._select_window is None:
            # don't wait on select
            return []  # pragma: no cover

        end_time = time() + self._select_window
        request_hash = request.hash

        while True:
            response = self._connection.receive(self._connection.client_config.period)
            if response is None:
                return []
            if response._.hash == request_hash:
                return response.messages
            self.buffer += [response]
            if time() > end_time:
                return []  # pragma: no cover

    def get_input_registry_map(self) -> str:
        """Get a dict with the registry map of the inputs."""

        return json.dumps(self._input_registry_map)

    def get_output_registry_map(self) -> str:
        """Get a dict with the registry map of the outputs."""

        return json.dumps(self._output_registry_map)

    # unsupported methods
    def create_timer(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError

    def delete_timer(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    def get_timers(self) -> List[str]:
        raise NotImplementedError


def load_entry_point(entry_point: str, default_class_name: str = "App") -> Type:
    """Load class."""

    if ":" in entry_point:
        module_name, class_name = entry_point.rsplit(":", 1)
    else:
        module_name, class_name = entry_point, default_class_name

    try:
        sys.path = ["", *SYS_PATH]
        try:
            module = import_module(module_name)
        finally:
            sys.path = SYS_PATH
    except (ModuleNotFoundError, TypeError):
        path = Path(module_name).expanduser().resolve()

        if path.exists():
            if path.is_dir():
                filename = path / "__init__.py"
                if filename.exists():
                    path = filename
        elif not path.suffix:
            filename = path.with_suffix(".py")
            if filename.exists():
                path = filename

        if path.exists():
            name = path.parent.stem if path.name == "__init__.py" else path.stem
            spec = spec_from_file_location(snake_name(name), path)
            if spec is None:
                raise ValueError(f"Unable to load module {module_name!r}")
            module = module_from_spec(spec)
            spec.loader.exec_module(module)  # type: ignore
        else:
            raise ValueError(f"Module {module_name!r} not found")

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ValueError(f"Application class {class_name!r} not found in {module_name!r} module")


def run_app(
    entry_point: str,
    interface_type: Optional[InterfaceType] = None,
    sub_url: Optional[str] = None,
    pub_url: Optional[str] = None,
    configuration: Optional[Union[str, Path, Mapping[str, Any]]] = None,
    max_steps: Optional[int] = None,
    log_level: Optional[LogLevel] = None,
    startup_time: Optional[float] = None,
    **kwargs: Any,
) -> Any:
    """Run Kelvin app."""

    app_class = load_entry_point(entry_point)

    if not isinstance(app_class, type):
        raise TypeError(f"Application class {app_class!r} is not a class")

    if not issubclass(app_class, ApplicationInterface):
        raise TypeError(
            "Application class {app_class.__name__!r} does not derive from 'kelvin.core.ApplicationInterface'"
        )

    if interface_type is not None:
        if interface_type not in {InterfaceType.DATA, InterfaceType.POLLER}:  # pragma: no cover
            raise ValueError(f"Unknown interface type: {interface_type}")
    elif issubclass(app_class, DataApplication):
        interface_type = InterfaceType.DATA
    elif issubclass(app_class, PollerApplication):
        interface_type = InterfaceType.POLLER
    else:
        raise ValueError(f"Unsupported interface type: {interface_type}")  # pragma: no cover

    kwargs = {"pub_url": pub_url, "sub_url": sub_url, "configuration": configuration, **kwargs}
    client = CoreClient(config={k: v for k, v in kwargs.items() if v is not None})

    main_config = MappingProxy(client.config.configuration)
    core_config = main_config.get("app.kelvin.core", {})
    inputs, outputs, config, params = get_io(core_config)

    if log_level is None:
        log_level = LogLevel[core_config.get("logging_level", "INFO").upper()]
        configure_logs(default_level=log_level)

    if not core_config:
        logger.warning("No core-configuration provided. All inputs/outputs are unfiltered.")

    kelvin_app_config = inflate(
        (item["name"], item["value"]) for item in config.pop("kelvin.app", {}).get("values", [])
    )

    uploader_config = core_config.get("uploader", {})
    info_config = main_config.get("info", {})
    kelvin_info = {
        "name": info_config.get("name"),
        "title": info_config.get("title"),
        "description": info_config.get("description"),
        "version": info_config.get("version"),
        "acp_name": uploader_config.get("acp_name"),
        "source": uploader_config.get("source"),
    }

    if startup_time is None:
        startup_time = time()

    with timestamper(lambda: 0):
        init_inputs = build_messages({k: v for k, v in inputs.items() if v.get("values")})
        init_configuration = cast(Dict[str, Any], build_messages(config))
        init_configuration.setdefault("kelvin", {}).update(
            {"app": kelvin_app_config, "info": kelvin_info}
        )
        init_parameters = build_messages(params)

    with client.connect(sync=True, keep_state=False) as connection:
        context = CoreClientContext(connection, startup_time=startup_time)

        if init_inputs:
            context.buffer += [
                Response(_={"time_of_validity": 0}, messages=[*init_inputs.values()])
            ]

        with timestamper(lambda: int(context.process_time * 1e9)):
            app = app_class(context=context)
            app.on_initialize(init_configuration, init_parameters)

            trash: List[int]

            step = 0

            while True:
                step += 1
                if max_steps is not None and step > max_steps:
                    logger.info(f"Maximum number of steps reached ({max_steps})")
                    break

                messages: List[Message] = []
                parameters: List[Message] = []

                try:
                    # pick up deferred messages
                    if context.buffer:
                        for x in context.buffer:
                            messages += x.messages
                        context.buffer[:] = []

                    response = connection.receive(timeout=client.config.period)
                    if response is not None:
                        # update time from request
                        context.process_time = response._.time_of_validity / 1e9
                        messages += response.messages
                    else:
                        # TODO: get core to provide empty responses even if no inputs as heartbeat
                        context.process_time = time()

                    if core_config:
                        trash = []
                        for index, message in enumerate(messages):
                            name = message._.name

                            if name in inputs:
                                continue

                            if name in params:
                                trash += [index]
                                parameters += [message]
                                continue

                            if name in config:
                                trash += [index]
                                logger.warning(
                                    "Configuration can only be changed at initialisation",
                                    message_name=name,
                                )
                                continue

                            trash += [index]
                            logger.warning(
                                "Dropping unknown inbound message",
                                message_name=name,
                                message_type=message._.type,
                            )

                        # take out the trash
                        for offset, index in enumerate(trash):
                            del messages[index - offset]

                        if parameters:
                            app.on_parameter_change(parameters)

                    if interface_type == InterfaceType.DATA:
                        app.on_data(messages)
                    elif interface_type == InterfaceType.POLLER:
                        app.on_poll()
                    else:  # pragma: no cover
                        raise ValueError(f"Unknown interface type: {interface_type}")

                    # get emitted messages
                    results = context.get_outputs()

                    if core_config:
                        trash = []
                        for index, message in enumerate(results):
                            name = message._.name
                            if name in outputs:
                                continue

                            trash += [index]
                            logger.warning(
                                "Dropping unknown outbound message",
                                message_name=name,
                                message_type=message._.type,
                            )

                        # take out the trash
                        for offset, index in enumerate(trash):
                            del results[index - offset]

                    connection.emit(results)

                except KeyboardInterrupt:  # pragma: no cover
                    break
                except Exception:  # pragma: no cover
                    logger.exception("Unable to process application")

    # terminate the app
    logger.info("Terminating app")
    try:
        app.on_terminate()
    except Exception:  # pragma: no cover
        logger.exception("Error while terminating")

    logger.info("Finished.")

    return app
