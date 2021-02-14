from abc import ABC, abstractmethod
from typing import List, Type

from plomberie.progress_bar.abstract_progress_bar import AbstractProgressBar
from plomberie.progress_bar.disabled_progress_bar import DisabledProgressBar


class Task(ABC):
    def __init__(self):
        self.__dependencies: List[Task] = []
        self.__progress_bar: AbstractProgressBar = DisabledProgressBar()

    @property
    def dependencies(self) -> List['Task']:
        return self.__dependencies

    def depends_on(self, *dependencies: 'Task') -> 'Task':
        self.__dependencies.extend(dependencies)
        return self

    def set_progress_total(self, total: int) -> None:
        self.__progress_bar.set_total(total)

    def increment_progress(self) -> None:
        self.__progress_bar.increment()

    def set_progress_bar(self, progress_bar: Type[AbstractProgressBar]):
        self.__progress_bar = progress_bar.get_instance(self.__class__.__name__)

    def post_run(self):
        self.__progress_bar.close()

    @abstractmethod
    def run(self) -> None:
        pass
