# -*- coding: utf-8 -*-
#
# Copyright 2019 SoloKeys Developers
#
# Licensed under the Apache License, Version 2.0, <LICENSE-APACHE or
# http://apache.org/licenses/LICENSE-2.0> or the MIT license <LICENSE-MIT or
# http://opensource.org/licenses/MIT>, at your option. This file may not be
# copied, modified, or distributed except according to those terms.
#

"""Python library for OnlyKey with Solo FIDO2"""

import pathlib

from . import client, commands, dfu, helpers, operations

__version__ = "0.0.27"


del pathlib
__all__ = ["client", "commands", "dfu", "enums", "exceptions", "helpers", "operations"]
