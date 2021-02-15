from typing import Union
import sys

from watson_machine_learning_client.utils.autoai.utils import try_import_tqdm
try_import_tqdm()

from tqdm import tqdm as TQDM

__all__ = [
    "ProgressBar"
]


class ProgressBar(TQDM):
    """
    Progress Bar class for handling progress bar display. It is based on 'tqdm' class, could be extended.

    Parameters
    ----------
    desc: str, optional
        Description string to be added as a prefix to progress bar.

    total: int, optional
        Total length of the progress bar.
    """
    def __init__(self, ncols: Union[str, int], position: int = 0, desc: str = None, total: int = 100, leave: bool = True) -> None:
        super().__init__(desc=desc, total=total, leave=leave, position=position, ncols=ncols, file=sys.stdout)
        self.total = total
        self.previous_message = None
        self.counter = 0
        self.progress = 0

    def increment_counter(self, progress: int = 5) -> None:
        """
        Increments internal counter and waits for specified time.

        Parameters
        ----------
        progress: int, optional
            How many steps at a time progress bar will increment.
        """
        self.progress = progress
        self.counter += progress

    def reset_counter(self) -> None:
        """
        Restart internal counter
        """
        self.counter = 0

    def update(self):
        """
        Updates the counter with specific progress.
        """
        super().update(n=self.progress)

    def last_update(self):
        """Fill up the progress bar till the end, this was the last run."""
        super().update(n=self.total - self.counter)
