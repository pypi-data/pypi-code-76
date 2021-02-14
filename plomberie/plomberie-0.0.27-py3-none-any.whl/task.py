from abc import ABC, abstractmethod
from typing import List, Optional

from tqdm import tqdm


class Task(ABC):
    def __init__(self, enable_progress_bar: bool = True):
        self.__dependencies: List[Task] = []
        self.__enable_progress_bar: bool = enable_progress_bar
        self.__progress_bar: Optional[tqdm] = None

    def depends_on(self, *dependencies: 'Task') -> 'Task':
        self.__dependencies.extend(dependencies)
        return self

    def post_run(self):
        if self.__progress_bar:
            self.__progress_bar.update(100 - self.__progress_bar.n)
            self.__progress_bar.close()

    @property
    def dependencies(self) -> List['Task']:
        return self.__dependencies

    def set_progress_percent(self, out_of_100: float) -> None:
        if self.__enable_progress_bar:
            if not self.__progress_bar:
                self.__progress_bar = self.__create_progress_bar()
            self.__progress_bar.update(out_of_100 - self.__progress_bar.n)

    @abstractmethod
    def run(self) -> None:
        pass

    def enable_progress_bar(self, enable: bool = True) -> 'Task':
        self.__enable_progress_bar = enable
        if self.__progress_bar and not enable:
            self.__progress_bar.close()
            self.__progress_bar = None
        return self

    def __create_progress_bar(self) -> tqdm:
        return tqdm(
            desc=self.__class__.__name__,
            total=100,
            bar_format='{desc}: |{bar}| {percentage:.2f}% ({elapsed}<{remaining})'
        )
