from __future__ import annotations
from abc import ABC

class BaseMediator(ABC):
    '''
    Base class of the BrowserEngine, which functions as
    mediator between all other components of the browser
    (i.e. the text interface, the network client, etc.)
    '''

    def notify(self, sender: object, event: str) -> None:
        pass

class BaseComponent:
    '''
    The base component provides the basic functionality of
    storing a mediator's instance inside component objects.
    '''

    def __init__(self, mediator: BaseMediator = None) -> None:
        self._mediator = mediator
    
    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator