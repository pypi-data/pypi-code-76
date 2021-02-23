from typing import Any, Callable, List, Mapping

from itertools import repeat, zip_longest
import functools

class Builder(object):
    def __init__(self) -> None:
        self._steps: List[Callable] = []
        self._executed_steps: int = 0

    @property
    def steps(self) -> int:
        return len(self._steps)

    @property
    def steps_list(self) -> List[Callable]:
        return self._steps

    @property
    def executed_steps(self) -> int:
        return self._executed_steps

    @property
    def progress(self) -> float:
        return self.executed_steps / self.steps

    def build(self, args_list=()) -> None:
        for fnc, args in zip_longest(
            self.steps_list,
            args_list
        ):
            if args is None:
                args = tuple()
            fnc(*args)

    def build_step(self) -> Callable:
        """Counts each method decorated with this decorator"""
        def decorator(func: Callable):
            @functools.wraps(func)
            def decorated(*args, **kwargs):
                self._executed_steps += 1
                ret = func(*args, **kwargs)
                return ret
            self.steps_list.append(decorated)
            return decorated
        return decorator

    def capture_results(self, *args: Callable) -> Callable:
        """Calls each function in *args with the result of the decorated function"""
        output_functions = args
        def decorator(func):
            @functools.wraps(func)
            def decorated(*args, **kwargs):
                ret = func(*args, **kwargs)
                for output_func in output_functions:
                    output_func(ret)
                return ret
            return decorated
        return decorator

    def capture_progress(self, *args: Callable[[float], Any]) -> Callable:
        """Calls each function in *args with the
        result of ```executed steps / steps```"""
        progress_functions = args
        def decorator(func):
            @functools.wraps(func)
            def decorated(*args, **kwargs):
                ret = func(*args, **kwargs)
                for progress_func in progress_functions:
                    progress_func(self.progress)
                return ret
            return decorated
        return decorator

    def composed(self, *decorators):
        """Used to compose a decorator. Useful for defining specific
        outputs and progress reports to a build step and resusing"""
        def decorated(func):
            for decorator in reversed(decorators):
                func = decorator(func)
            return func
        return decorated
