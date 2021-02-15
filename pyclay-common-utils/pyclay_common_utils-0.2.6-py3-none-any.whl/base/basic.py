from __future__ import annotations
from abc import abstractmethod
from typing import TypeVar, Generic, List, cast, Dict, Any
import json
import operator
import inspect
import random
import numpy as np
import yaml

from logger import logger
from ..check_utils import check_required_keys, check_type_from_list, \
    check_type, check_file_exists, check_issubclass, check_issubclass_from_list
from ..file_utils import file_exists
from ..path_utils import get_extension_from_path
from ..constants.number_constants import jsonable_types, \
    iterable_jsonable_types, noniterable_jsonable_types

T = TypeVar('T')
H = TypeVar('H')

class BasicObject(Generic[T]):
    @abstractmethod
    def __str__(self) -> str:
        ''' To override '''
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()
    
    def __key(self) -> tuple:
        return tuple([self.__class__.__name__] + list(self.__dict__.values()))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        return NotImplemented

    @classmethod
    def get_constructor_params(cls) -> list:
        return [param for param in list(inspect.signature(cls.__init__).parameters.keys()) if param != 'self']

    def to_constructor_dict(self) -> dict:
        constructor_dict = {}
        for key, val in self.__dict__.items():
            if key in self.get_constructor_params():
                constructor_dict[key] = val
        return constructor_dict

    @classmethod
    def buffer(cls: T, obj) -> T:
        return obj

    def copy(self: T) -> T:
        constructor_dict = self.to_constructor_dict()
        for key, val in constructor_dict.items():
            if hasattr(val, 'copy'):
                constructor_dict[key] = val.copy()
        return type(self)(**constructor_dict)

class BasicLoadableObject(BasicObject[T]):
    """
    Assumptions:
        1. self.__dict__ matches constructor parameters perfectly.
        2. Any to_dict or to_dict_list methods of any class object in the class variable list doesn't take any parameters.
        3. No special id class variable.
        4. Non-trivial classmethods must be defined in child class
    """
    def __init__(self):
        super().__init__()

    def __key(self) -> tuple:
        return tuple([self.__class__.__name__] + list(self.to_dict().items()))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.to_dict()})'

    @classmethod
    def get_constructor_params(cls) -> list:
        return [param for param in list(inspect.signature(cls.__init__).parameters.keys()) if param != 'self']

    def to_dict(self: T) -> dict:
        result = {}
        for key, val in self.to_constructor_dict().items():
            if hasattr(val, 'to_dict') and callable(val.to_dict):
                result[key] = val.to_dict()
            elif hasattr(val, 'to_dict_list') and callable(val.to_dict_list):
                result[key] = val.to_dict_list()
            else:
                result[key] = val
        return result
    
    @classmethod
    def from_dict(cls: T, item_dict: dict) -> T:
        """
        Note: It is required that all class constructor parameters be of a JSON serializable datatype.
              If not, it is necessary to override this classmethod.
        """
        constructor_dict = {}
        constructor_params = cls.get_constructor_params()
        unnecessary_params = []
        for key, value in item_dict.items():
            if key in constructor_params:
                constructor_dict[key] = value
            else:
                unnecessary_params.append(key)
        if len(unnecessary_params) > 0:
            logger.warning(f'Received unnecessary parameters in {cls.__name__}.from_dict')
            logger.warning(f'Received: {list(item_dict.keys())}')
            logger.warning(f'Expected: {constructor_params}')
            logger.warning(f'Extra: {unnecessary_params}')
        check_required_keys(constructor_dict, required_keys=constructor_params)
        return cls(**constructor_dict)

    def save_to_path(self: T, save_path: str, overwrite: bool=False):
        if file_exists(save_path) and not overwrite:
            logger.error(f'File already exists at save_path: {save_path}')
            raise Exception

        extension = get_extension_from_path(save_path)
        if extension == 'json':
            json.dump(self.to_dict(), open(save_path, 'w'), indent=2, ensure_ascii=False)
        elif extension == 'yaml':
            yaml.dump(self.to_dict(), open(save_path, 'w'), allow_unicode=True)
        else:
            raise ValueError(
                f"""
                Invalid file extension encountered: {extension}
                save_path: {save_path}

                Please use either a .json or a .yaml extension.
                """
            )
    
    @classmethod
    def load_from_path(cls: T, json_path: str) -> T:
        check_file_exists(json_path)
        extension = get_extension_from_path(json_path)
        if extension == 'json':
            item_dict = json.load(open(json_path, 'r'))
        elif extension == 'yaml':
            item_dict = yaml.load(open(json_path, 'r'), Loader=yaml.FullLoader)
        else:
            raise ValueError(
                f"""
                Invalid file extension encountered: {extension}
                json_path: {json_path}

                Please use either a .json or a .yaml extension.
                """
            )
        return cls.from_dict(item_dict)

    def verify_jsonable(self):
        def verify_obj(obj: Any, working_path: str):
            if isinstance(obj, tuple(noniterable_jsonable_types + [str])):
                pass
            elif isinstance(obj, dict):
                verify_dict(obj, working_path=working_path)
            elif isinstance(obj, (list, tuple)):
                verify_list(obj, working_path=working_path)
            else:
                has_to_dict = hasattr(obj, 'to_dict')
                has_to_dict_list = hasattr(obj, 'to_dict_list')
                class_name = obj.__class__.__name__
                message = f"""
                Found a non-jsonable type ({class_name}) at the following path:
                {working_path}
                """
                if has_to_dict or has_to_dict_list:
                    message += '\n\nNote:'
                    if has_to_dict:
                        message += f'\n{class_name}.to_dict() method exists.'
                    if has_to_dict_list:
                        message += f'\n{class_name}.to_dict_list() method exists.'
                raise Exception(message)

        def verify_dict(item_dict: Dict[str, Any], working_path: str):
            for key, val in item_dict.items():
                working_path0 = f"{working_path}['{key}']"
                verify_obj(val, working_path=working_path0)

        def verify_list(item_list: List[Any], working_path: str):
            for i in range(len(item_list)):
                working_path0 = f'{working_path}[{i}]'
                verify_obj(item_list[i], working_path=working_path0)

        assert hasattr(self, 'to_dict')
        base_path = f'{self.__class__.__name__}(...).to_dict()'
        verify_dict(self.to_dict(), working_path=base_path)

class BasicLoadableIdObject(BasicLoadableObject[T]):
    """
    Assumptions:
        1. self.__dict__ matches constructor parameters perfectly.
        2. Any to_dict or to_dict_list methods of any class object in the class variable list doesn't take any parameters.
        3. Non-trivial classmethods must be defined in child class
        4. Must implement __str__
    """
    def __init__(self, id: int):
        super().__init__()
        self.id = id

class BasicHandler(Generic[H, T]):
    """
    Assumptions:
        1. Handler has only one class parameter: the object list.
        2. All contained objects are of type obj_type.
    """
    def __init__(self: H, obj_type: type, obj_list: List[T]=None):
        check_type(obj_type, valid_type_list=[type])
        self.obj_type = obj_type
        if obj_list is not None:
            check_type_from_list(obj_list, valid_type_list=[obj_type])
        self.obj_list = obj_list if obj_list is not None else []

    def __key(self) -> tuple:
        return tuple([self.__class__] + list(self.__dict__.values()))

    def __hash__(self):
        return hash(self.__key())

    def __add__(self, other: H) -> H:
        if isinstance(other, type(self)):
            if self.obj_type == other.obj_type:
                return type(self)(self.obj_list + other.obj_list)
            else:
                raise TypeError(
                    f"""
                    Cannot add {type(self).__name__} of {self.obj_type.__name__} and {type(other).__name__} of {other.obj_type.__name__}
                    """
                )
        else:
            raise TypeError(
                f"""
                Cannot add {type(self).__name__} and {type(other).__name__}
                """
            )

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self: H):
        return f'{self.__class__.__name__}({[obj for obj in self]})'

    def __repr__(self: H):
        return self.__str__()

    def __len__(self: H) -> int:
        return len(self.obj_list)

    def __getitem__(self: H, idx: int) -> T:
        if type(idx) is int:
            if len(self.obj_list) == 0:
                logger.error(f"{type(self).__name__} is empty.")
                raise IndexError
            elif idx < -len(self.obj_list) or idx >= len(self.obj_list):
                logger.error(f"Index out of range: {idx}")
                raise IndexError
            else:
                return self.obj_list[idx]
        elif type(idx) is slice:
            return type(self)(self.obj_list[idx.start:idx.stop:idx.step])
        else:
            logger.error(f'Expected int or slice. Got type(idx)={type(idx)}')
            raise TypeError

    def __setitem__(self: H, idx: int, value: T):
        if type(idx) is int:
            check_type(value, valid_type_list=[self.obj_type])
            self.obj_list[idx] = value
        elif type(idx) is slice:
            check_type_from_list(value, valid_type_list=[self.obj_type])
            self.obj_list[idx.start:idx.stop:idx.step] = value
        else:
            logger.error(f'Expected int or slice. Got type(idx)={type(idx)}')
            raise TypeError

    def __delitem__(self: H, idx: int):
        if type(idx) is int:
            if len(self.obj_list) == 0:
                logger.error(f"{type(self).__name__} is empty.")
                raise IndexError
            elif idx < 0 or idx >= len(self.obj_list):
                logger.error(f"Index out of range: {idx}")
                raise IndexError
            else:
                del self.obj_list[idx]
        elif type(idx) is slice:
            del self.obj_list[idx.start:idx.stop:idx.step]
        else:
            logger.error(f'Expected int or slice. Got type(idx)={type(idx)}')
            raise TypeError

    def __iter__(self: H) -> H:
        self.n = 0
        return self

    def __next__(self: H) -> T:
        if self.n < len(self.obj_list):
            result = self.obj_list[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    @classmethod
    def buffer(cls: H, obj) -> H:
        return obj

    def copy(self: H) -> H:
        return type(self)([obj.copy() for obj in self.obj_list])

    def append(self: H, item: T):
        check_type(item, valid_type_list=[self.obj_type])
        self.obj_list.append(item)

    def extend(self: H, item_list: List[T]):
        for item in item_list:
            self.append(item)

    def sort(self: H, attr_name: str, reverse: bool=False):
        if len(self) > 0:
            attr_list = list(self.obj_list[0].__dict__.keys())
            property_names = [p for p in dir(type(self.obj_list[0])) if isinstance(getattr(type(self.obj_list[0]), p), property)]
            attr_list.extend(property_names)
            if attr_name not in attr_list:
                logger.error(f"{self.obj_type.__name__} class has not attribute: '{attr_name}'")
                logger.error(f'Possible attribute names:')
                for name in attr_list:
                    logger.error(f'\t{name}')
                raise Exception

            self.obj_list.sort(key=operator.attrgetter(attr_name), reverse=reverse)
        else:
            logger.error(f"Cannot sort. {type(self).__name__} is empty.")
            raise Exception

    def shuffle(self: H):
        random.shuffle(self.obj_list)

class BasicLoadableHandler(BasicHandler[H, T]):
    """
    Assumptions:
        1. Handler has only one class parameter: the object list.
        2. All contained objects are of type obj_type.
        3. Any to_dict or to_dict_list methods of any class object in the object list doesn't take any parameters.
    """
    def __init__(self: H, obj_type: type, obj_list: List[T]=None):
        super().__init__(obj_type=obj_type, obj_list=obj_list)

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.to_dict_list()})'

    def to_dict_list(self: H) -> List[dict]:
        return [item.to_dict() if not isinstance(item, tuple(jsonable_types)) else item for item in self]

    @classmethod
    @abstractmethod
    def from_dict_list(cls: H, dict_list: List[dict]) -> H:
        """
        To Override
        """
        raise NotImplementedError

    def save_to_path(self: H, save_path: str, overwrite: bool=False):
        if file_exists(save_path) and not overwrite:
            logger.error(f'File already exists at save_path: {save_path}')
            raise Exception

        extension = get_extension_from_path(save_path)
        if extension == 'json':
            json.dump(self.to_dict_list(), open(save_path, 'w'), indent=2, ensure_ascii=False)
        elif extension == 'yaml':
            yaml.dump(self.to_dict_list(), open(save_path, 'w'), allow_unicode=True)
        else:
            raise ValueError(
                f"""
                Invalid file extension encountered: {extension}
                save_path: {save_path}

                Please use either a .json or a .yaml extension.
                """
            )
    
    @classmethod
    def load_from_path(cls: H, json_path: str) -> H:
        check_file_exists(json_path)
        extension = get_extension_from_path(json_path)
        if extension == 'json':
            item_dict_list = json.load(open(json_path, 'r'))
        elif extension == 'yaml':
            item_dict_list = yaml.load(open(json_path, 'r'), Loader=yaml.FullLoader)
        else:
            raise ValueError(
                f"""
                Invalid file extension encountered: {extension}
                json_path: {json_path}

                Please use either a .json or a .yaml extension.
                """
            )
        return cls.from_dict_list(item_dict_list)

    def verify_jsonable(self):
        for item in self:
            assert hasattr(item, 'verify_jsonable')
            item.verify_jsonable()

    def split(self, ratio: List[int], shuffle: bool=True) -> List[H]:
        assert len(self) % sum(ratio) == 0, f'sum(ratio)={sum(ratio)} does not evenly divide into len(self)={len(self)}'
        locations = np.cumsum([val*int(len(self)/sum(ratio)) for val in ratio])
        start_location = None
        end_location = 0
        count = 0
        samples = []
        if shuffle:
            self.shuffle()
        while count < len(locations):
            start_location = end_location
            end_location = locations[count]
            count += 1
            samples.append(self[start_location:end_location].copy())
        return samples
    
    def get(self, **kwargs) -> H:
        def condition(obj) -> bool:
            for key, val in kwargs.items():
                if not hasattr(obj, key):
                    return False
                elif val is None or (val is not None and getattr(obj, key) == val):
                    pass
                elif isinstance(val, (list, tuple)) and not isinstance(getattr(obj, key), (list, tuple)):
                    found = False
                    for val_part in val:
                        if getattr(obj, key) == val_part:
                            found = True
                            break
                    if not found:
                        return False
                    else:
                        pass
                else:
                    return False
            return True
        return type(self)([obj for obj in self if condition(obj)])

class BasicLoadableIdHandler(BasicLoadableHandler[H, T], BasicHandler[H, T]):
    """
    TODO: Figure out why VSCode shows syntax error unless I explicitly inherit from all levels of nested parent classes.

    Assumptions:
        1. Handler has only one class parameter: the object list.
        2. All contained objects are of type obj_type.
        3. Any to_dict or to_dict_list methods of any class object in the object list doesn't take any parameters.
        4. All objects in handler must have an id class variable.
    """
    def __init__(self: H, obj_type: type, obj_list: List[T]=None):
        super().__init__(obj_type=obj_type, obj_list=obj_list)
    
    def get_obj_from_id(self: H, id: int) -> T:
        id_list = []
        for obj in self:
            if id == obj.id:
                return obj
            else:
                id_list.append(obj.id)
        id_list.sort()
        logger.error(f"Couldn't find {self.obj_type.__name__} with id={id}")
        logger.error(f"Possible ids: {id_list}")
        raise Exception

    @property
    def ids(self) -> List[int]:
        return [obj.id for obj in self]

class BasicSubclassHandler(Generic[H, T]):
    """
    TODO: Test Functionality
    Assumptions:
        1. Handler has only one class parameter: the object list.
        2. All contained objects are a subclass of obj_type.
    """
    def __init__(self: H, obj_parent_class: type, obj_list: List[T]=None):
        logger.warning(f"Warning: BasicSubclassHandler hasn't been tested yet. Use with caution.")
        check_type(obj_parent_class, valid_type_list=[type])
        self.obj_parent_class = obj_parent_class
        if obj_list is not None:
            check_issubclass_from_list(obj_list, valid_parent_class_list=[obj_parent_class])
        self.obj_list = obj_list if obj_list is not None else []

    def __key(self) -> tuple:
        return tuple([self.__class__] + list(self.__dict__.values()))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self: H):
        return f'{self.__class__.__name__}({[obj for obj in self]})'

    def __repr__(self: H):
        return self.__str__()

    def __len__(self: H) -> int:
        return len(self.obj_list)

    def __getitem__(self: H, idx: int) -> T:
        if type(idx) is int:
            if len(self.obj_list) == 0:
                logger.error(f"{type(self).__name__} is empty.")
                raise IndexError
            elif idx < 0 or idx >= len(self.obj_list):
                logger.error(f"Index out of range: {idx}")
                raise IndexError
            else:
                return self.obj_list[idx]
        elif type(idx) is slice:
            return type(self)(self.obj_list[idx.start:idx.stop:idx.step])
        else:
            logger.error(f'Expected int or slice. Got type(idx)={type(idx)}')
            raise TypeError

    def __setitem__(self: H, idx: int, value: T):
        if type(idx) is int:
            check_issubclass(value, valid_parent_class_list=[self.obj_parent_class])
            self.obj_list[idx] = value
        elif type(idx) is slice:
            check_issubclass_from_list(value, valid_parent_class_list=[self.obj_parent_class])
            self.obj_list[idx.start:idx.stop:idx.step] = value
        else:
            logger.error(f'Expected int or slice. Got type(idx)={type(idx)}')
            raise TypeError

    def __delitem__(self: H, idx: int):
        if type(idx) is int:
            if len(self.obj_list) == 0:
                logger.error(f"{type(self).__name__} is empty.")
                raise IndexError
            elif idx < 0 or idx >= len(self.obj_list):
                logger.error(f"Index out of range: {idx}")
                raise IndexError
            else:
                del self.obj_list[idx]
        elif type(idx) is slice:
            del self.obj_list[idx.start:idx.stop:idx.step]
        else:
            logger.error(f'Expected int or slice. Got type(idx)={type(idx)}')
            raise TypeError

    def __iter__(self: H) -> H:
        self.n = 0
        return self

    def __next__(self: H) -> T:
        if self.n < len(self.obj_list):
            result = self.obj_list[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    @classmethod
    def buffer(cls: H, obj) -> H:
        return obj

    def copy(self: H) -> H:
        return type(self)(self.obj_list.copy())

    def append(self: H, item: T):
        check_issubclass(item, valid_parent_class_list=[self.obj_parent_class])
        self.obj_list.append(item)

    def sort(self: H, attr_name: str, reverse: bool=False):
        # TODO: Test that this works.
        if len(self) > 0:
            attr_list = None
            class_list = []
            for obj in self.obj_list:
                if obj.__class__.__name__ not in class_list:
                    class_list.append(obj.__class__.__name__)
                if attr_list is None:
                    attr_list = list(obj.__dict__.keys())
                else:
                    attr_list = cast(List[str], attr_list)
                    for i in list(range(len(attr_list)))[::-1]:
                        if attr_list[i] not in list(obj.__dict__.keys()):
                            del attr_list[i]

            if attr_name not in attr_list:
                logger.error(f"'{attr_name}' is not an attribute shared by every class in this handler: {class_list}")
                logger.error(f'Shared attribute names:')
                for name in attr_list:
                    logger.error(f'\t{name}')
                raise Exception

            self.obj_list.sort(key=operator.attrgetter(attr_name), reverse=reverse)
        else:
            logger.error(f"Cannot sort. {type(self).__name__} is empty.")
            raise Exception

    def shuffle(self: H):
        random.shuffle(self.obj_list)

class MultiParameterHandler(Generic[H, T]):
    """
    Assumptions:
        1. Handler can have multiple class parameters, but one of them must be the object list. (This mainly affects constructor calls via type(self)(~).)
        2. All contained objects are of type obj_type.
    """
    def __init__(self: H, obj_type: type, obj_list: List[T]=None):
        check_type(obj_type, valid_type_list=[type])
        self.obj_type = obj_type
        if obj_list is not None:
            check_type_from_list(obj_list, valid_type_list=[obj_type])
        self.obj_list = obj_list if obj_list is not None else []

    @classmethod
    def get_constructor_params(cls) -> list:
        return [param for param in list(inspect.signature(cls.__init__).parameters.keys()) if param != 'self']

    def to_constructor_dict(self) -> dict:
        constructor_dict = {}
        for key, val in self.__dict__.items():
            if key in self.get_constructor_params():
                constructor_dict[key] = val
        return constructor_dict

    def __key(self) -> tuple:
        return tuple([self.__class__] + list(self.__dict__.values()))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self: H):
        return f'{self.__class__.__name__}({[obj for obj in self]})'

    def __repr__(self: H):
        return self.__str__()

    def __len__(self: H) -> int:
        return len(self.obj_list)

    def __getitem__(self: H, idx: int) -> T:
        if type(idx) is int:
            if len(self.obj_list) == 0:
                logger.error(f"{type(self).__name__} is empty.")
                raise IndexError
            elif idx < 0 or idx >= len(self.obj_list):
                logger.error(f"Index out of range: {idx}")
                raise IndexError
            else:
                return self.obj_list[idx]
        elif type(idx) is slice:
            # TODO: Test Functionality
            new_instance = self.copy()
            new_instance.obj_list = new_instance.obj_list[idx.start:idx.stop:idx.step]
            return new_instance
        else:
            logger.error(f'Expected int or slice. Got type(idx)={type(idx)}')
            raise TypeError

    def __setitem__(self: H, idx: int, value: T):
        if type(idx) is int:
            check_type(value, valid_type_list=[self.obj_type])
            self.obj_list[idx] = value
        elif type(idx) is slice:
            check_type_from_list(value, valid_type_list=[self.obj_type])
            self.obj_list[idx.start:idx.stop:idx.step] = value
        else:
            logger.error(f'Expected int or slice. Got type(idx)={type(idx)}')
            raise TypeError

    def __delitem__(self: H, idx: int):
        if type(idx) is int:
            if len(self.obj_list) == 0:
                logger.error(f"{type(self).__name__} is empty.")
                raise IndexError
            elif idx < 0 or idx >= len(self.obj_list):
                logger.error(f"Index out of range: {idx}")
                raise IndexError
            else:
                del self.obj_list[idx]
        elif type(idx) is slice:
            del self.obj_list[idx.start:idx.stop:idx.step]
        else:
            logger.error(f'Expected int or slice. Got type(idx)={type(idx)}')
            raise TypeError

    def __iter__(self: H) -> H:
        self.n = 0
        return self

    def __next__(self: H) -> T:
        if self.n < len(self.obj_list):
            result = self.obj_list[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    @classmethod
    def buffer(cls: H, obj) -> H:
        return obj

    def copy(self: H) -> H:
        # TODO: Test functionality
        new_instance = type(self)(**self.to_constructor_dict())
        for key, val in self.__dict__.items():
            if key not in self.get_constructor_params():
                new_instance.__dict__[key] = val
        return new_instance

    def append(self: H, item: T):
        check_type(item, valid_type_list=[self.obj_type])
        self.obj_list.append(item)

    def sort(self: H, attr_name: str, reverse: bool=False):
        if len(self) > 0:
            attr_list = list(self.obj_list[0].__dict__.keys())    
            if attr_name not in attr_list:
                logger.error(f"{self.obj_type.__name__} class has not attribute: '{attr_name}'")
                logger.error(f'Possible attribute names:')
                for name in attr_list:
                    logger.error(f'\t{name}')
                raise Exception

            self.obj_list.sort(key=operator.attrgetter(attr_name), reverse=reverse)
        else:
            logger.error(f"Cannot sort. {type(self).__name__} is empty.")
            raise Exception

    def shuffle(self: H):
        random.shuffle(self.obj_list)