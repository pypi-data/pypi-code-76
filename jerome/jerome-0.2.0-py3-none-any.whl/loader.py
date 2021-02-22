import typing as t
from io import StringIO
from pathlib import Path


def loader(
    text: t.Optional[str] = None,
    file_path: t.Optional[Path] = None,
    size: int = -1,
    read_bytes: bool = False,
) -> t.Iterator[t.Union[bytes, str]]:
    if file_path is not None:
        p = Path(file_path)
        if read_bytes:
            io_handle = p.open(mode="rb")
        else:
            io_handle = p.open(encoding="utf-8")
    elif text is None:
        raise ValueError("Must provide either text or file_path parameter")
    else:
        io_handle = StringIO(text)
    while True:
        chunk = io_handle.read(size)
        if len(chunk) > 0:
            yield chunk
        else:
            io_handle.close()
            break
