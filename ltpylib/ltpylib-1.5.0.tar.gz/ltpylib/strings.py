#!/usr/bin/env python3
import re
from decimal import Decimal
from typing import List, Union

BOOLEAN_STRINGS_FALSE = frozenset([
  "no",
  "n",
  "false",
])
BOOLEAN_STRINGS_TRUE = frozenset([
  "yes",
  "y",
  "true",
])
TO_SNAKE_CASE_REMOVE_REGEX = re.compile(r"[']")
TO_SNAKE_CASE_REGEX = re.compile(r"[^a-zA-Z0-9]")
MULTI_SPACE_REGEX = re.compile(r"\s+")


def convert_to_bool(val: str, check_if_valid: bool = False) -> Union[bool, str, None]:
  if val is None:
    return None

  if check_if_valid and not is_boolean(val):
    return val

  lower_val = val.lower()

  if lower_val in BOOLEAN_STRINGS_FALSE:
    return False
  elif lower_val in BOOLEAN_STRINGS_TRUE:
    return True

  raise ValueError("String is not a boolean: " % val)


def convert_to_number(
  val: str,
  check_if_valid: bool = False,
  float_only: bool = False,
  use_decimal: bool = False,
) -> Union[int, float, str, None]:
  if val is None:
    return None

  if check_if_valid and not is_number(val):
    return val

  if float_only:
    return Decimal(val) if use_decimal else float(val)

  try:
    return int(val)
  except ValueError:
    return Decimal(val) if use_decimal else float(val)


def is_boolean(val: str) -> bool:
  if not val:
    return False

  return val.lower() in BOOLEAN_STRINGS_FALSE or val.lower() in BOOLEAN_STRINGS_TRUE


def is_number(val: str) -> bool:
  if not val:
    return False

  if val.isdigit():
    return True

  val = val.replace(".", "", 1)
  if val.isdigit():
    return True

  if val.startswith("-") and val.replace("-", "", 1).isdigit():
    return True

  return False


def str_list_max_length(values: List[str]) -> int:
  return len(max(values, key=len))


def strip_color_codes(val: str) -> str:
  return re.sub(r"\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]", "", val)


def substring_after(val: str, before_str: str) -> str:
  return val.split(before_str, 1)[1]


def substring_before(val: str, before_str: str) -> str:
  return val.split(before_str)[0]


def to_snake_case(val: str) -> str:
  return MULTI_SPACE_REGEX.sub(
    " ",
    TO_SNAKE_CASE_REGEX.sub(
      " ",
      TO_SNAKE_CASE_REMOVE_REGEX.sub(
        "",
        val.lower(),
      ),
    ),
  ).strip().replace(" ", "_")


def _main():
  import sys

  result = globals()[sys.argv[1]](*sys.argv[2:])
  if result is not None:
    print(result)


if __name__ == "__main__":
  try:
    _main()
  except KeyboardInterrupt:
    exit(130)
