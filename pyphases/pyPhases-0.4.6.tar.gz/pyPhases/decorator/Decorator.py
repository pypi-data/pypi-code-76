from ..Phase import Phase
from ..util.Optionizable import Optionizable


class Decorator(Optionizable):
    phase: Phase

    def filter(self, phase : Phase) -> bool:
        """  this method can be used to filter the stages it should be used on
        """
        return True

    def before(self, phase : Phase):
        """  this method is called every stage before its executed
        """
        pass

    def after(self, phase : Phase):
        """ this method is called every stage after its executed
        """
        pass
