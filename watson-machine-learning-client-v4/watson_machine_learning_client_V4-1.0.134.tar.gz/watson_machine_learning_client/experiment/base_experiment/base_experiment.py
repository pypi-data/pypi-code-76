from abc import ABC, abstractmethod

__all__ = [
    "BaseExperiment"
]


class BaseExperiment(ABC):
    """
    Base abstract class for Experiment.
    """

    @abstractmethod
    def runs(self, *, filter: str):
        """Get the historical runs but with WML Pipeline name filter.

        Parameters
        ----------
        filter: str, required
            WML Pipeline name to filter the historical runs.
        """
        pass
