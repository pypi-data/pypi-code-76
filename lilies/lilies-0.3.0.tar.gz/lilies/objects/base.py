from abc import ABC, abstractmethod


class LilyBase(ABC):
    @abstractmethod
    def wilt(self):
        raise NotImplementedError("wilt")

    @abstractmethod
    def _isstringish(self):
        raise NotImplementedError("_isstringish")

    @abstractmethod
    def _isblockish(self):
        raise NotImplementedError("_isblockish")

    @property
    @abstractmethod
    def width(self):
        raise NotImplementedError("width")

    @property
    @abstractmethod
    def height(self):
        raise NotImplementedError("height")

    @classmethod
    def __subclasshook__(cls, subclass):
        required = ["wilt", "_isstringish", "_isblockish"]
        for r in required:
            if not any(r in c.__dict__ for c in subclass.__mro__):
                return NotImplemented
        return True
