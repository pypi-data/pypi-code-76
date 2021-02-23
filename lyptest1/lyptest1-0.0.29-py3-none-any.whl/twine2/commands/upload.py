# Copyright 2013 Donald Stufft
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import logging
import os.path
from typing import Dict, List, cast

import requests


logger = logging.getLogger(__name__)


def main(args: List[str]) -> None:
    # parser = argparse.ArgumentParser(prog="twine upload")
    print("main say4")
    parser = argparse.ArgumentParser(prog="say4 upload")
    # settings.Settings.register_argparse_arguments(parser)
    parser.add_argument(
        "dists",
        nargs="+",
        metavar="dist",
        help="The distribution files to upload to the repository "
        "(package index). Usually dist/* . May additionally contain "
        "a .asc file to include an existing signature with the "
        "file upload.",
    )

    parsed_args = parser.parse_args(args)

    print("upload main ")
    # upload_settings = settings.Settings.from_argparse(parsed_args)

    # Call the upload function with the arguments from the command line
    # return upload(upload_settings, parsed_args.dists)
