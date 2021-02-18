import pytest


@pytest.fixture(scope="session")
def Anything():
    return type.__new__(
        type,
        "Anything",
        (object,),
        {
            "__repr__": lambda self: self.__class__.__name__,
            "__eq__": lambda _, __: True,
        },
    )()


@pytest.fixture(scope="session")
def Something():
    return type.__new__(
        type,
        "Something",
        (object,),
        {
            "__repr__": lambda self: self.__class__.__name__,
            "__eq__": lambda _, other: other is not None,
        },
    )()
