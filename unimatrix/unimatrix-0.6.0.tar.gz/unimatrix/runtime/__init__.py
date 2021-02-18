"""The :mod:`unimatrix.runtime` package provides a common interface to set
up the application runtime environment.
"""
import inspect
import pkg_resources
import os
import warnings

import ioc
import ioc.loader

from unimatrix.lib import meta


IS_CONFIGURED = False


def get_entrypoints(name):
    entrypoints = [
        (entry_point.name, entry_point.load())
        for entry_point
        in pkg_resources.iter_entry_points(name)
    ]
    return sorted(entrypoints, key=lambda x: getattr(x[1], 'WEIGHT', 0))


@meta.allow_sync
async def setup():
    """Setup all :mod:`unimatrix` components."""
    global IS_CONFIGURED
    if IS_CONFIGURED:
        return

    ioc.setup()
    for _, module in get_entrypoints('unimatrix.runtime'):
        on_setup = getattr(module, 'on_setup', None)
        if on_setup is None:
            continue
        await on_setup()\
            if inspect.iscoroutinefunction(on_setup)\
            else on_setup()

    IS_CONFIGURED = True


@meta.allow_sync
async def teardown():
    """Teardown all :mod:`unimatrix` components."""
    for _, module in get_entrypoints('unimatrix.runtime'):
        on_teardown = getattr(module, 'on_teardown', None)
        if on_teardown is None:
            continue
        await on_teardown()\
            if inspect.iscoroutinefunction(on_teardown)\
            else on_teardown()

    ioc.teardown()
    IS_CONFIGURED = False # pylint: disable=unused-variable


@meta.allow_sync
async def on(name, *args, runlevel=None, **kwargs):
    if name == 'boot':
        await setup()
    elif name == 'shutdown':
        await teardown()

    qualname = os.getenv('UNIMATRIX_BOOT_MODULE')
    if qualname is None:
        return
    try:
        obj = ioc.loader.import_symbol(qualname)
    except ImportError:
        warnings.warn(
            f"UNIMATRIX_BOOT_MODULE points to a non-existant symbol: "
            f"{qualname}.")
        return

    if not callable(obj) and not inspect.ismodule(obj):
        raise TypeError(
            "UNIMATRIX_BOOT_MODULE must point to a callable or module."
        )
    if callable(obj):
        return await obj(name, *args, **kwargs)\
            if inspect.iscoroutinefunction(obj)\
            else obj(name, *args, **kwargs)

    f = getattr(obj, name, None)
    if f is None:
        return
    return await f(*args, **kwargs)\
        if inspect.iscoroutinefunction(f)\
        else f(*args, **kwargs)
