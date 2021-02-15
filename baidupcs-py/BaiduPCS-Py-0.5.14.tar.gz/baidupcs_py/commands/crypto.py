from typing import Any
from os import PathLike
from pathlib import Path

from baidupcs_py.common.io import to_decryptio, READ_SIZE
from baidupcs_py.common.path import exists


def decrypt_file(
    from_encrypted: PathLike, to_decrypted: PathLike, encrypt_key: Any = None
):
    assert exists(from_encrypted)

    dio = to_decryptio(open(from_encrypted, "rb"), encrypt_key=encrypt_key)

    dpath = Path(to_decrypted)
    dir_ = dpath.parent
    if not dir_.exists():
        dir_.mkdir(parents=True)

    with dpath.open("wb") as dfd:
        while True:
            data = dio.read(READ_SIZE)
            if not data:
                break
            dfd.write(data)
