from abc import ABC, abstractmethod


class AbstractProgressBar(ABC):
    @abstractmethod
    def set_total(self, total: int) -> None:
        pass

    @abstractmethod
    def increment(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def get_instance(label: str) -> 'AbstractProgressBar':
        pass
