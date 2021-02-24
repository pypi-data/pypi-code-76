from abc import ABC, abstractmethod


class InterstateServer(ABC):
    @abstractmethod
    def start_server(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()