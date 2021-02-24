"""Compatibility stuff for old python versions"""
from typing import TypeVar, cast, TYPE_CHECKING
import asyncio

T = TypeVar("T")  # pylint: disable=C0103
if TYPE_CHECKING:
    from typing import Any  # pylint: disable=C0412


class NamedTask(asyncio.Task):  # type: ignore
    """wrapper for mypy checking in older python versions"""

    def get_name(self) -> str:
        """dummy"""
        raise NotImplementedError()

    def set_name(self, __value: object) -> None:
        """dummy"""
        raise NotImplementedError()


def cast_task(task: "asyncio.Task[T]") -> "NamedTask[T]":  # type: ignore
    """Cast task to NamedTask"""
    return cast("NamedTask[Any]", task)  # type: ignore
