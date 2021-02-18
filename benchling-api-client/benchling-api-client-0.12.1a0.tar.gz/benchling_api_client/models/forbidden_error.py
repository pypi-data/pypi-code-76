from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.forbidden_error_error import ForbiddenErrorError
from ..types import UNSET, Unset

T = TypeVar("T", bound="ForbiddenError")


@attr.s(auto_attribs=True)
class ForbiddenError:
    """  """

    error: Union[Unset, ForbiddenErrorError] = UNSET

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
        error: Union[Unset, ForbiddenErrorError] = UNSET
        _error = d.pop("error", UNSET)
        if not isinstance(_error, Unset):
            error = ForbiddenErrorError.from_dict(_error)

        forbidden_error = cls(
            error=error,
        )

        return forbidden_error
