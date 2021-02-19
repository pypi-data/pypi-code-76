from abc import ABC
from abc import abstractmethod


class Step(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def process(self, data, input, utils):  # input是一個字典
        pass


class StepException(Exception):  # Exception是python內建的不用Import
    pass
