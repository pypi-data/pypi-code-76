import typing as t
from io import StringIO

STX = "\002"
ETX = "\003"
NEWLINE = "\n"

def split(
    text: t.Optional[str] = None,
    size: int = -1,
) -> t.Iterator[str]:
    io_handle = StringIO(text)
    while True:
        chunk = io_handle.read(size)
        if len(chunk) > 0:
            yield chunk
        else:
            io_handle.close()
            break

def forward_bw(text: str, mark: str = ETX, split_marker=STX, split_size = 5000) -> str:
    """Returns the Burrows Wheeler transform of text.
    Mark is by convention $
    Mark must be the lowest sort order character in text.
    """
    if mark in text:
        raise ValueError(f"The mark '{mark}' exists in text: {NEWLINE.join([l for l in text.splitlines() if mark in l])}")
    result = []
    for s in split(text, split_size):
        matrix = [s + mark]
        [matrix.append(matrix[-1][1:] + matrix[-1][:1]) for i in s if i != mark]
        result.append("".join([i[-1] for i in sorted(matrix)]))
    return split_marker.join(result)


def reverse_bw(text: str, mark: str = ETX, split_marker=STX) -> str:
    """Returns the Burrows Wheeler reverse transform of text."""
    result = ""
    for s in text.split(split_marker):
        p = sorted((t, i) for i, t in enumerate(s))
        k = s.index(mark)
        for _ in s:
            t, k = p[k]
            result += t if t != mark else ""
    return result


# python -m nuitka --module burrowswheeler.py
