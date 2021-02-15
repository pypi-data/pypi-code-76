"""
Helper to recursively expand cls.__subclasses__()
"""
__all__ = ['all_subclasses']


def all_subclasses_gen(cls):
    """Generator to recursively expand cls.__subclasses__()"""
    yield cls
    for klass in cls.__subclasses__():
        yield from all_subclasses(klass)


def all_subclasses(cls) -> list:
    """Recursively expand cls.__subclasses__()"""
    return list(all_subclasses_gen(cls))
