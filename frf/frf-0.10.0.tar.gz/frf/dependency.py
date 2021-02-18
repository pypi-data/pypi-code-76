"""Declares various functions to inject dependencies."""
from typing import Any

import ioc
from fastapi import Depends


def Injected(name, *args, **kwargs):
    """Like :func:`fastapi.Depends`, but takes the identifier of a dependency
    that is injected through :func:`frf.provide`.
    """
    return Depends(lambda: ioc.require(name), *args, **kwargs)


def ContextualInjected(dependency: str, use_cache: bool = True) -> Any:
    """Like :func:`Injected`, but sets up a context."""
    async def context_factory():
        provider = ioc.require(dependency)
        async with provider.as_context() as ctx:
            yield ctx
    return Depends(context_factory, use_cache=use_cache)
