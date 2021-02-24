from typing import Any, Dict, Callable, Optional, Union, List, Tuple
from inspect import isclass
from os import path
import json
import yaml
from deepmerge import always_merger

FactoryType = Callable[..., Any]
ConfigurationType = Dict[str, Union[List, Dict[str, Any]]]
GetItemType = Union[str, FactoryType]


def configure(config: Union[str, ConfigurationType], file_type: Optional[str] = None):
    Registry.default_registry().configure(config, file_type)


def get(item: GetItemType, *args: Any, **kwargs: Any) -> Any:
    return Registry.default_registry().get(item, *args, **kwargs)


def register(factory: FactoryType, name: Optional[str] = None):
    Registry.default_registry().register(factory, name)


def override_factory(item: GetItemType, factory: FactoryType):
    Registry.default_registry().override_factory(item, factory)


def default_registry() -> 'Registry':
    return Registry.default_registry()


class Registry:
    CONFIG_META_PREFIX = '$'
    ARGS_KEY = '$args'
    TYPE_KEY = '$type'
    _default_registry: Optional['Registry'] = None

    @staticmethod
    def reset():
        Registry._default_registry = None

    @staticmethod
    def default_registry() -> 'Registry':
        if Registry._default_registry is None:
            Registry._default_registry = Registry()

        return Registry._default_registry

    def __init__(self,
                 config_path: Optional[str] = None,
                 configuration: Optional[ConfigurationType] = None,
                 factories: Optional[Dict[str, FactoryType]] = None,
                 objects: Optional[Dict[str, Any]] = None,
                 set_default: bool = True):
        self.config_path = config_path
        self.configuration = configuration or {}
        self.factories = factories or {}
        self.factory_types = {val: key for key, val in self.factories.items()}
        self.objects = objects or {}

        if set_default and Registry._default_registry is None:
            Registry._default_registry = self

        if self.config_path is not None:
            self.load_configuration()

    def reset_object(self, object_name: str):
        self.objects.pop(object_name)

    def configure(self, config: Union[str, ConfigurationType], file_type: Optional[str] = None):
        if isinstance(config, dict):
            self.merge_configuration(config)
        else:
            self.load_configuration(config, file_type)

    def merge_configuration(self, config: ConfigurationType):
        self.configuration = always_merger.merge(self.configuration or {}, config)

    def load_configuration(self, config_path: Optional[str] = None, file_type: Optional[str] = None):
        file_path = config_path or self.config_path

        # use the file extension as the file type if none is given
        if file_type is None:
            _, config_ext = path.splitext(file_path)
            config_type = config_ext[1:]  # remove .
        else:
            config_type = file_type

        with open(file_path or self.config_path) as config_file:
            if config_type == 'json':
                self.merge_configuration(json.load(config_file))
            elif config_type == 'yaml':
                self.merge_configuration(yaml.safe_load(config_file))
            else:
                raise RegistryError(f'Invalid config file format, must be "json" or "yaml": {config_type}')

    def get_object_meta_configuration(self, object_name: str) -> Dict[str, Any]:
        if object_name not in self.configuration:
            return {}

        config = self.configuration[object_name]
        # remove any keys that don't start with @ (and aren't @args) and remove the @ from the keys
        return {k[1:]: v for k, v in config.items() if k.startswith(self.CONFIG_META_PREFIX) and k != self.ARGS_KEY}

    def find_value(self, path: List[str], config: Dict[str, Any]) -> Any:
        if path[0] not in config:
            raise RegistryError(f'Unable to find value, {path[0]} not found in config: {config}')

        value = config[path[0]]

        if len(path) == 1:
            return value

        return self.find_value(path[1:], value)

    def inject_value(self, value: Any) -> Any:
        if isinstance(value, str):
            if value.startswith('\\$'):
                return value[1:]

            if value.startswith('$'):
                if '.' in value:
                    return self.find_value(value[1:].split('.'), self.configuration)

                return self.get_by_name(value[1:])

        return value

    def get_object_configuration(self, object_name: Optional[str], *args: Any, **kwargs: Any) -> Tuple[List, Dict]:
        if object_name is None or object_name not in self.configuration:
            return [], {}

        config = self.configuration[object_name]

        if isinstance(config, list):
            return [*config, *args], kwargs

        # start with the config of the factory defined by the $type key in the config, if it exists
        config_args, config_kwargs = self.get_object_configuration(config.get(self.TYPE_KEY, None))

        # merge object config, if defined
        config_args = [*config_args, *config.get(self.ARGS_KEY, [])]
        config_kwargs = {**config_kwargs, **{k: v for k, v in config.items() if not k.startswith(self.CONFIG_META_PREFIX)}}

        # merge in any additional args and kwargs
        config_args = [*config_args, *args]
        config_kwargs = {**config_kwargs, **kwargs}

        # loop through values and find instances to be injected
        config_args = [self.inject_value(arg) for arg in config_args]
        config_kwargs = {key: self.inject_value(arg) for key, arg in config_kwargs.items()}

        return config_args, config_kwargs

    def get_object_factory(self, object_name: str) -> FactoryType:
        if object_name not in self.factories:
            if object_name not in self.configuration:
                raise RegistryFactoryNotFoundError(f'Unable to find a factory or config for object: {object_name}')

            if self.TYPE_KEY not in self.configuration[object_name]:
                raise RegistryFactoryNotFoundError(
                    f'No factory or "$type" key found in config for object: {object_name}')

            factory_name = self.configuration[object_name][self.TYPE_KEY]

            if factory_name not in self.factories:
                raise RegistryFactoryNotFoundError(
                    f'Unable to find a factory for "{object_name}" with $type: {factory_name}')

            return self.factories[factory_name]

        return self.factories[object_name]

    def register(self, factory: FactoryType, name: Optional[str] = None):
        if name is None:
            if not isclass(factory):
                raise RegistryError(f'Only classes can be registered without a name')

            name = factory.__name__

        if name in self.factories:
            raise RegistryFactoryExists(f'Factory with name "{name}" already registered')

        self.factories[name] = factory
        self.factory_types[factory] = self.factory_types.get(factory, []) + [name]

    def override_factory(self, item: GetItemType, factory: FactoryType):
        object_name = item if isinstance(item, str) else item.__name__

        if object_name not in self.factories:
            raise RegistryFactoryNotFoundError(f'Cannot override factory, existing factory not found for item: {item}')

        self.factories[object_name] = factory

    def create_object(self, object_name: str, *args: Any, **kwargs: Any):
        factory = self.get_object_factory(object_name)
        object_args, object_kwargs = self.get_object_configuration(object_name, *args, **kwargs)
        return factory(*object_args, **object_kwargs)

    def get_by_name(self, object_name: str, *args: Any, **kwargs: Any):
        if object_name in self.objects:
            return self.objects[object_name]

        self.objects[object_name] = self.create_object(object_name, *args, **kwargs)
        return self.objects[object_name]

    def get_by_type(self, factory: FactoryType, *args: Any, **kwargs: Any) -> Any:
        if factory not in self.factory_types:
            raise RegistryFactoryNotFoundError(f'Unable to find factory: {factory}')

        if not isclass(factory):
            raise RegistryFactoryIsNotClassError(f'Cannot get default object, factory must be a class: {factory}')

        object_names = self.factory_types[factory]
        object_name = factory.__name__

        if object_name not in object_names:
            raise RegistryFactoryDefaultNotFoundError(f'Unable to find a default object for factory: {factory}')

        return self.get_by_name(object_name, *args, **kwargs)

    def get(self, item: GetItemType, *args: Any, **kwargs: Any) -> Any:
        if isinstance(item, str):
            return self.get_by_name(item, *args, **kwargs)

        return self.get_by_type(item, *args, **kwargs)


class RegistryError(Exception):
    pass


class RegistryFactoryNotFoundError(RegistryError):
    pass


class RegistryFactoryDefaultNotFoundError(RegistryError):
    pass


class RegistryFactoryExists(RegistryError):
    pass


class RegistryFactoryIsNotClassError(RegistryError):
    pass
