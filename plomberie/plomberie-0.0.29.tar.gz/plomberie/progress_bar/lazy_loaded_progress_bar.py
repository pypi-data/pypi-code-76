from typing import Optional

from tqdm import tqdm

from plomberie.progress_bar.abstract_progress_bar import AbstractProgressBar


class LazyLoadedProgressBar(AbstractProgressBar):

    def __init__(self, label: str):
        self.__label = label
        self.__tqdm: Optional[tqdm] = None

    def set_total(self, total: int) -> None:
        self.__init_tqdm(total)

    def increment(self) -> None:
        self.__tqdm.update(1)

    def close(self) -> None:
        if self.__tqdm:
            self.__tqdm.update(self.__tqdm.total - self.__tqdm.n)
            self.__tqdm.close()
            self.__tqdm = None

    def __init_tqdm(self, total: int) -> None:
        if not self.__tqdm:
            self.__tqdm = tqdm(
                desc=self.__label,
                total=total,
                bar_format='{desc}: |{bar}| {percentage:.2f}% [{n_fmt}/{total_fmt}, {elapsed}<{remaining}]'
            )
        else:
            self.__tqdm.reset(total)

    @staticmethod
    def get_instance(label: str) -> 'AbstractProgressBar':
        return LazyLoadedProgressBar(label)
