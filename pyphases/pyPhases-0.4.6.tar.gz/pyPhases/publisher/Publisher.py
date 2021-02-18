from abc import ABC, abstractmethod
from ..Phase import Phase
from ..decorator.Decorator import Decorator


class Publisher(Decorator):
    def after(self, phase: Phase):
        self.publish(phase)

    def publish(self, phase: Phase):
        pass
