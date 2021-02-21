import contextlib
import contextvars
import inspect
from functools import wraps
from typing import Mapping

_dependencies = contextvars.ContextVar("dependencies", default={})
_dependency_functions = contextvars.ContextVar("dependency_functions", default={})
_context = contextvars.Context()


def _init_context():
    _dependencies.set({})
    _dependency_functions.set({})


_context.run(_init_context)


def dependency(function: callable, expand_mapping: bool = False):
    if expand_mapping:
        @wraps(function)
        async def _function(*args, **kwargs):
            if isinstance(result := await function(*args, **kwargs), Mapping):
                _context[_dependencies].extend(result)

            return result
    else:
        _function = function
    _context[_dependency_functions][function.__name__] = _function


async def _get_dependency(name):
    dependencies_ = _context[_dependencies]
    dependency_functions = _context[_dependency_functions]

    try:
        return dependencies_[name]
    except KeyError:
        dep = await dependency_functions[name]()
        dependencies_[name] = dep
        return dep


def bind(function: callable):
    signature = inspect.signature(function, follow_wrapped=True)

    @wraps(function)
    async def _function(*args, **kwargs):
        parameters = list(signature.parameters.values())[len(args):]
        matched_dependencies = {it.name: await _get_dependency(it.name)
                                for it in parameters
                                if it.name not in kwargs}
        matched_dependencies.update(kwargs)
        return await _context.run(function, *args, **matched_dependencies)

    return _function


@contextlib.asynccontextmanager
async def dependencies(**kwargs):
    token = _context.run(lambda: _dependencies.set(kwargs))
    try:
        yield
    finally:
        _context.run(lambda: _dependencies.reset(token))
