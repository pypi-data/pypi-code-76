"""Utils used by the CodeGrade API.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
import io
import json
import math
import re
import sys
import typing as t
import uuid
import warnings
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Union

import cg_maybe
import structlog
from httpx import Response

logger = structlog.get_logger()

T = t.TypeVar("T")


def response_code_matches(code: int, expected: Union[str, int]) -> bool:
    if expected == "default":
        return True
    elif isinstance(expected, int) and code == expected:
        return True
    return (
        isinstance(expected, str)
        and code > 100
        and code / 100 == int(expected[0])
    )


def to_multipart(dct: Dict[str, Any]) -> Dict[str, Any]:
    res = {}
    for key, value in dct.items():
        if isinstance(value, list):
            for idx, subval in enumerate(value):
                assert isinstance(subval, tuple)
                res[f"{key}_{idx}"] = subval
        elif isinstance(value, tuple):
            res[key] = value
        else:
            res[key] = (key, io.StringIO(json.dumps(value)))

    return res


def to_dict(obj: Any) -> t.Any:
    from .models.types import File

    if obj is None:
        return None
    elif isinstance(obj, (str, bool, int, float)):
        return obj
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    elif isinstance(obj, dict):
        # Store locally for faster lookup
        _to_dict = to_dict
        return {k: _to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # Store locally for faster lookup
        _to_dict = to_dict
        return [_to_dict(sub) for sub in obj]
    elif isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return obj.total_seconds()
    elif isinstance(obj, File):
        return obj.to_tuple()
    else:
        return obj.to_dict()


def get_error(
    response: Response,
    code_errors: t.Sequence[t.Tuple[t.Sequence[t.Union[str, int]], t.Any]],
) -> Exception:
    found_code = response.status_code
    for codes, make_error in code_errors:
        if any(response_code_matches(found_code, code) for code in codes):
            return make_error.from_dict(response.json(), response=response)

    from .errors import ApiResponseError

    return ApiResponseError(response=response)


_WARNING_SUB = re.compile(r"\\(.)")


@dataclass
class HttpWarning:
    __slots__ = ("code", "agent", "text")
    code: int
    agent: str
    text: str

    @classmethod
    def parse(cls, *, warning: str) -> "HttpWarning":
        code, agent, text = warning.split(" ", maxsplit=3)
        text = text.strip()
        if text[0] != '"' or text[-1] != '"':
            raise ValueError("Warning string is malformed")
        text = _WARNING_SUB.sub(r"\1", text[1:-1])
        return cls(
            code=int(code),
            agent=agent,
            text=text,
        )


def log_warnings(response: Response) -> None:
    headers = response.headers
    get = getattr(headers, "get_list", None)
    if get is None:
        get = headers.getlist

    for warn_str in get("Warning"):
        try:
            warning = HttpWarning.parse(warning=warn_str)
        except ValueError:
            logger.warn(
                "Cannot parse warning",
                warning=warn_str,
                exc_info=True,
            )
        else:
            warnings.warn(
                "Got a API warning from {}: {}".format(
                    warning.agent, warning.text
                )
            )


def maybe_input(prompt: str, dflt: str = "") -> cg_maybe.Maybe[str]:
    try:
        res = input(
            "{}{}: ".format(
                prompt,
                " [default: {}]".format(dflt) if dflt else "",
            )
        )
    except EOFError:
        return cg_maybe.Nothing
    else:
        return cg_maybe.Just(res or dflt)


def select_from_list(
    prompt: str, lst: t.Iterable[T], make_label: t.Callable[[T], str]
) -> cg_maybe.Maybe[T]:
    lst = list(lst)
    max_width = math.ceil(math.log10(len(lst) + 1))
    for idx, item in enumerate(lst):
        print(
            "[{0: >{1}}] {2}".format(idx + 1, max_width, make_label(item)),
            file=sys.stderr,
        )

    while True:
        inp = maybe_input(prompt)
        if inp.is_nothing:
            return cg_maybe.Nothing

        try:
            res = lst[int(inp.value) - 1]
            print("Selecting", make_label(res), file=sys.stderr)
            return cg_maybe.Just(res)
        except ValueError:
            continue
