from abc import ABCMeta, abstractmethod


class BaseDataSource(metaclass=ABCMeta):
    """
    A base class for all data sources
    """
    @abstractmethod
    def get_holding_register(self, unit_id: int, address: int) -> int:
        ...

    @abstractmethod
    def get_analog_input(self, unit_id: int, address: int) -> int:
        ...

    @abstractmethod
    def get_discrete_input(self, unit_id: int, address: int) -> bool:
        ...

    @abstractmethod
    def get_coil(self, unit_id: int, address: int) -> bool:
        ...

    @abstractmethod
    def set_holding_register(self, unit_id: int, address: int, value: int) -> None:
        ...

    @abstractmethod
    def set_coil(self, unit_id: int, address: int, value: bool) -> None:
        ...
