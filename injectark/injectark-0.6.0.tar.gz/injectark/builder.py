from .factory import Strategy, Factory
from typing import List, Dict, Type, TypeVar, Any


class StrategyBuilder:
    def __init__(self, strategies: Dict[str, Strategy]) -> None:
        self.strategies = strategies

    def build(self, strategies: List[str],
              custom_strategy: Strategy = {}) -> Strategy:
        strategy: Dict[str, Any] = {}
        for name in strategies:
            strategy.update(self.strategies[name])
        strategy.update(custom_strategy)
        return strategy


class FactoryBuilder:
    def __init__(self, factories: List[Type[Factory]]) -> None:
        self.factories = {factory.__name__: factory
                          for factory in factories}

    def build(self, config: Dict[str, str], name: str = None) -> Factory:
        name = name or config.get('factory', '')
        factory = self.factories[name]
        return factory(config)  # type: ignore
