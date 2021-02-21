from pathlib import Path, PosixPath

from toml.encoder import _dump_str, TomlEncoder

from pyappconf.encoding.general import HasStr


def _dump_hasstr(obj: HasStr) -> str:
    return _dump_str(str(obj))


class CustomTomlEncoder(TomlEncoder):

    def __init__(self, _dict=dict, preserve=False):
        super().__init__(_dict=_dict, preserve=preserve)
        self.dump_funcs[Path] = _dump_hasstr
        self.dump_funcs[PosixPath] = _dump_hasstr