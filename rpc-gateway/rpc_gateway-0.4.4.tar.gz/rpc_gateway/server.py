from typing import Optional, Dict, Any, List, Union, ClassVar, Callable
import logging
import websockets
import pickle
import json
from dataclasses import dataclass, asdict
from inspect import isclass, signature, getdoc, Signature, Parameter, _empty
from concurrent.futures import ThreadPoolExecutor
from rpc_gateway import errors, messages, gateway
from rpc_gateway.utils import await_sync

logger = logging.getLogger(__name__)


def get_attribute_path(obj, attribute_path: List[str]):
    if len(attribute_path) == 1:
        return getattr(obj, attribute_path[0])

    return get_attribute_path(getattr(obj, attribute_path[0]), attribute_path[1:])


def set_attribute_path(obj, attribute_path: List[str], value: Any):
    if len(attribute_path) == 1:
        return setattr(obj, attribute_path[0], value)

    return get_attribute_path(getattr(obj, attribute_path[0]), attribute_path[1:])


def is_json_serializable(value: Any) -> bool:
    try:
        json.dumps(value)
        return True
    except TypeError:
        return False


@dataclass
class Instance:
    name: str
    instance: Any
    group: str
    locked: bool


@dataclass
class Argument:
    name: str
    default: Any
    serializable: bool

    @classmethod
    def from_parameter(cls, parameter: Parameter) -> 'Argument':
        default = None if parameter.default is _empty else parameter.default
        serializable = is_json_serializable(default)

        return cls(
            name=parameter.name,
            default=default if serializable else str(default),
            serializable=serializable
        )


@dataclass
class Attribute:
    name: str
    value: Any
    serializable: bool

    @classmethod
    def from_value(cls, name: str, value: Any) -> 'Attribute':
        serializable = is_json_serializable(value)

        return cls(
            name=name,
            value=value if serializable else str(value),
            serializable=serializable
        )


@dataclass
class Method:
    name: str
    description: str
    arguments: List[Argument]

    @classmethod
    def from_method(cls, name: str, method: Callable) -> 'Method':
        method_signature = signature(method)
        return cls(
            name=name,
            description=getdoc(method),
            arguments=[Argument.from_parameter(param) for param in method_signature.parameters.values()]
        )


@dataclass
class InstanceMetadata:
    name: str
    locked: bool
    description: str
    attributes: List[Attribute]
    methods: List[Method]

    @classmethod
    def from_instance(cls, instance: Instance) -> 'InstanceMetadata':
        attributes = []
        methods = []

        for name in dir(instance.instance):
            if not name.startswith('_'):
                value = getattr(instance.instance, name)

                if callable(value):
                    methods.append(Method.from_method(name, value))
                else:
                    attributes.append(Attribute.from_value(name, value))

        return cls(
            name=instance.name,
            description=getdoc(instance.instance),
            attributes=attributes,
            methods=methods,
            locked=instance.locked
        )


class Server(gateway.GatewayClient):
    def __init__(self, gateway_url: str = 'ws://localhost:8888', max_workers: int = 5, instances: Optional[Dict[str, Instance]] = None, auth_key: str = 'DEFAULT_KEY'):
        super().__init__(gateway_url=gateway_url, auth_key=auth_key)
        self.instances = {} if instances is None else instances
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def _on_start(self):
        await self._register_gateway_instances(self.instances)

    async def _on_stop(self):
        self.instances = {}

    async def _register_gateway_instances(self, instances: Dict[str, Instance]):
        instance_data = [(instance.name, instance.group) for name, instance in instances.items()]
        await self.websocket_connection.send_request(messages.Method.REGISTER, instance_data)

    def register(self, name: str, instance: Any, group: Optional[str] = None) -> Any:
        self.logger.info(f'Registering instance: {name}')

        if name is None or name == '':
            raise errors.InvalidInstanceError(f'Cannot register instance with name: {name}')

        if name in self.instances:
            raise errors.InstanceAlreadyRegisteredError(f'Instance already registered with name: {name}')

        if group is None:
            group = instance.__class__.__name__

        self.instances[name] = Instance(name=name, instance=instance, locked=False, group=group)

        return instance

    def deregister(self, name: str) -> Any:
        self.logger.info(f'Deregistering instance: {name}')
        self.websocket_connection.send_request_sync(messages.Method.DEREGISTER, [name])

    def _get_instance(self, instance_name: Union[type, str]) -> Instance:
        try:
            if isclass(instance_name):
                return self.instances[instance_name.__name__]

            return self.instances[instance_name]
        except KeyError:
            raise errors.InstanceNotFoundError(f'Instance not found: {instance_name}')

    def _available(self, instance_name: str) -> messages.Response:
        if instance_name not in self.instances:
            return messages.Response(status=messages.Status.NOT_FOUND)

        if self.instances[instance_name].locked:
            return messages.Response(status=messages.Status.LOCKED)

        return messages.Response()

    def _lock(self, instance_name: str) -> messages.Response:
        instance = self._get_instance(instance_name)
        instance.locked = True

        return messages.Response()

    def _unlock(self, instance_name: str) -> messages.Response:
        instance = self._get_instance(instance_name)
        instance.locked = False

        return messages.Response()

    def _metadata(self, instance_name: str) -> messages.Response:
        instance = self._get_instance(instance_name)
        metadata = InstanceMetadata.from_instance(instance)

        return messages.Response(data=asdict(metadata))

    def _get(self, instance_name: str, attribute_path: str) -> messages.Response:
        try:
            instance = self._get_instance(instance_name)
            data = get_attribute_path(instance.instance, attribute_path.split('.'))

            if callable(data):
                return messages.Response(status=messages.Status.METHOD)

            try:
                serialized_data = pickle.dumps(data)
            except (pickle.PickleError, TypeError):
                return messages.Response(status=messages.Status.PROXY)

            return messages.Response(data=data)
        except Exception as err:
            return messages.Response(status=messages.Status.ERROR, data=err)

    def _set(self, instance_name: str, attribute_path: str, value: Any) -> messages.Response:
        try:
            instance = self._get_instance(instance_name)
            set_attribute_path(instance.instance, attribute_path.split('.'), value)
            return messages.Response()
        except Exception as err:
            return messages.Response(status=messages.Status.ERROR, data=err)

    def _call(self, instance_name: str, attribute_path: str, args: Union[List[Any], Dict[str, Any]], kwargs: Dict[str, Any]) -> messages.Response:
        try:
            instance = self._get_instance(instance_name)
            method = get_attribute_path(instance.instance, attribute_path.split('.'))

            # handle special case where args is encoded as a dict with numerical string indexes
            if isinstance(args, dict):
                args = [args[str(i)] for i in range(len(args))]

            data = method(*args, **kwargs)
            return messages.Response(data=data)
        except Exception as err:
            return messages.Response(status=messages.Status.ERROR, data=err)

    async def _run(self, *args: Any) -> Any:
        return await self.event_loop.run_in_executor(self.executor, *args)

    async def _handle_request(self, websocket_connection: websockets.WebSocketCommonProtocol, request: messages.Request) -> messages.Response:
        try:
            if request.method == messages.Method.GET:
                return await self._run(self._get, request.data['instance'], request.data['attribute'])

            if request.method == messages.Method.SET:
                return await self._run(self._set, request.data['instance'], request.data['attribute'], request.data['value'])

            if request.method == messages.Method.CALL:
                return await self._run(self._call, request.data['instance'], request.data['attribute'], request.data['args'], request.data['kwargs'])

            if request.method == messages.Method.AVAILABLE:
                return await self._run(self._available, request.data['instance'])

            if request.method == messages.Method.LOCK:
                return await self._run(self._lock, request.data['instance'])

            if request.method == messages.Method.UNLOCK:
                return await self._run(self._unlock, request.data['instance'])

            if request.method == messages.Method.METADATA:
                return await self._run(self._metadata, request.data['instance'])
        except KeyError:
            return messages.Response(status=messages.Status.ERROR, data=errors.InvalidMessageError(f'Invalid message'))

        return messages.Response(status=messages.Status.ERROR, data=errors.InvalidMethodError(f'Invalid method: {request.method}'))


if __name__ == '__main__':
    import time
    logging.basicConfig(level=logging.INFO)

    class TestClass:
        foo = 'bar'

        def method(self):
            return 'baz'

        def sleep(self, duration):
            time.sleep(duration)

    server = Server()
    server.register('test', TestClass())
    server.start()