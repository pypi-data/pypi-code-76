import logging
import re
from pathlib import Path
from typing import Generator, List, Optional, Tuple, Type

from lilili.apis.api import Api
from lilili.apis.npmjs import NpmjsApi
from lilili.apis.pypi import PypiApi
from lilili.apis.rubygems import RubygemsApi
from lilili.db.defs import Domain, Session
from lilili.errors import NotDetectedApiError

logger = logging.getLogger(__name__)


def _auto_detect(first_line: str) -> Tuple[Type[Api], str]:
    if "Package" in first_line and "Version" in first_line:
        api = PypiApi
        regex = r"(?P<name>[^\s]*[a-zA-Z]+[^\s]*)\s+(?P<version>[^\s]*\d+[^\s]*)\s*"
    elif "Gems included by the bundle" in first_line:
        api = RubygemsApi
        regex = r".*\* (?P<name>[^()]+) \((?P<version>[^()\s]+).*\)"
    elif "yarn list" in first_line:
        api = NpmjsApi
        regex = r".*─ (?P<name>[^\\^]+)@(?P<version>[\w.-]+)"
    else:
        raise NotDetectedApiError("first line of the file: " + first_line)
    return api, regex


def _get_api(domain: Domain) -> Type[Api]:
    for api in (PypiApi, RubygemsApi, NpmjsApi):
        if api.domain is domain:
            return api
    raise ValueError


def _extract_libraries(lines: List[str], regex: str) -> List[re.Match]:
    libraries = []
    for line in lines:
        m = re.match(regex, line)
        if m is None or ".x" in m.group("version"):
            logger.debug("skipped: " + line)
        else:
            libraries.append(m)
    return libraries


class Search(object):
    def __init__(self, file_path: Path, domain: Optional[Domain] = None):
        with open(file_path, mode="rt", encoding="utf-8") as f:
            logger.info(f"read file: {file_path}")
            lines = f.read().splitlines()

        if len(lines) == 0:
            return

        if domain is None:
            self.__api, regex = _auto_detect(lines[0])
        else:
            self.__api = _get_api(domain)
            regex = r"(?P<name>.+),(?P<version>[^,]+)"  # csv

        self.__match_objects = _extract_libraries(lines, regex)
        logger.info(str(self.size) + " libraries were found.")

    @property
    def size(self) -> int:
        return len(self.__match_objects)

    def search_libraries(self) -> Generator:
        session = Session()
        for m in self.__match_objects:
            name = m.group("name")
            version = m.group("version")
            logger.info(f"library: {name} {version}")
            library = self.__api(session, name, version).find_library()
            yield library.to_dict()
        session.close()
