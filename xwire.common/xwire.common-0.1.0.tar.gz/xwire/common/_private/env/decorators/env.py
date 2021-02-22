import os
from typing import Callable


def env(name: str) -> Callable[[], property]:
    def decorator(_: Callable[..., str]) -> property:
        env_value = None

        def wrapper(_: Callable[..., str]) -> str:
            nonlocal env_value
            if env_value is None:
                env_value = os.environ.get(name)
                if env_value is None:
                    raise ValueError(f'Unknown environment variable "{name}"')

            return env_value
        return property(wrapper)
    return decorator
