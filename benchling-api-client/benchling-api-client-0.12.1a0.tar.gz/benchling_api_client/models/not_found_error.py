from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.not_found_error_error import NotFoundErrorError
from ..types import UNSET, Unset

T = TypeVar("T", bound="NotFoundError")


@attr.s(auto_attribs=True)
class NotFoundError:
    """  """

    error: Union[Unset, NotFoundErrorError] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        error: Union[Unset, NotFoundErrorError] = UNSET
        _error = d.pop("error", UNSET)
        if not isinstance(_error, Unset):
            error = NotFoundErrorError.from_dict(_error)

        not_found_error = cls(
            error=error,
        )

        return not_found_error
