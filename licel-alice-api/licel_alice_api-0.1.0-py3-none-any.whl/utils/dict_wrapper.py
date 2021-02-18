from typing import (
    Iterator,
    Mapping,
    TypeVar,
    Sequence,
    overload,
    Optional,
    Callable,
    List,
)


class DictWrapper(Mapping):
    __response: dict = {}

    def __init__(self, response: dict):
        self.__response = response

    def __getitem__(self, k):
        return self.__response.__getitem__(k)

    def __len__(self) -> int:
        return self.__response.__len__()

    def __iter__(self) -> Iterator:
        return self.__response.__iter__()

    @property
    def __dict__(self) -> dict:
        return self.__response

    @property
    def raw(self) -> dict:
        """
        Original dict
        """
        return self.__dict__


T = TypeVar("T")


class DictListWrapper(Sequence[T]):
    __list: List[dict]
    __wrapper: Callable = None

    def __init__(self, original_list: List[dict], wrapper: Callable):
        self.__list = original_list
        self.__wrapper = wrapper

    @overload
    def __getitem__(self, i: int) -> T:
        return self.__wrapper(self.__list.__getitem__(i))

    @overload
    def __getitem__(self, s: slice) -> Sequence[T]:
        return list(map(self.__wrapper, self.__list.__getitem__(s)))

    def __getitem__(self, i: int) -> T:
        return self.__wrapper(self.__list.__getitem__(i))

    def __len__(self) -> int:
        return self.__list.__len__()

    @property
    def raw(self) -> List[dict]:
        """
        Original list
        """
        return self.__list


class DictWrapperProp(Mapping):
    __name: str
    __wrapper_attr: str
    __wrapper: Callable = None
    __is_list: bool

    def __init__(
        self,
        name: str = None,
        wrapper: Callable = None,
        is_list=False,
        wrapper_attr: str = None,
    ):
        self.__name = name
        self.__wrapper = wrapper
        self.__is_list = is_list
        self.__wrapper_attr = wrapper_attr

    def __get_wrapper(self, instance: DictWrapper) -> Optional[Callable]:
        if self.__wrapper:
            return self.__wrapper

        if self.__wrapper_attr:
            return getattr(instance, self.__wrapper_attr, None)

        return None

    def __len__(self) -> int:
        pass

    def __getitem__(self, k):
        pass

    def __iter__(self) -> Iterator:
        pass

    def __set_name__(self, owner, name):
        if self.__name is None:
            self.__name = name

    def __get__(self, instance: DictWrapper, owner):
        value = instance.raw.get(self.__name)
        wrapper = self.__get_wrapper(instance)

        if wrapper is None or value is None:
            return value

        if self.__is_list and isinstance(value, list):
            return DictListWrapper(value, wrapper)

        return wrapper(value)

    def __set__(self, instance: DictWrapper, value) -> None:
        raise AttributeError(f"'{self.__name}' can't be assigned")


def dict_prop(
    name: str = None,
    wrapper: Callable = None,
    is_list=False,
    wrapper_attr: str = None,
):
    return DictWrapperProp(name, wrapper, is_list, wrapper_attr)
