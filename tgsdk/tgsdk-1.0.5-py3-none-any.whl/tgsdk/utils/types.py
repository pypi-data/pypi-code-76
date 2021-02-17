#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2021 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, Dict, List, Optional, Tuple, TypeVar, Union

if TYPE_CHECKING:
	from tgsdk import InputFile

ID = Union[str, int]

FileInput = Union[str, bytes, Path, Union[IO, "InputFile"]]

