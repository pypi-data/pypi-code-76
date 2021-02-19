"""Kernel data parser."""

from pathlib import Path


def read_kernel(fname):
    """Read kernel content and data.

    Parameters
    ----------
    fname: str or pathlib.Path
        Kernel file name to parse.

    Returns
    -------
    str
        Kernel whole content.
    dict
        Parsed data.

    """
    content = Path(fname).read_text(encoding='utf-8')
    data = get_data(content)
    return content, data


def get_data(content):
    """Extract data from a kernel content."""
    data = {}
    last_key = False

    for line in extract_data(content):
        key, value = parse(line)

        if key is not None:
            data[key] = value if value is not None else []
            last_key = key

        elif last_key and value is not None:
            data[last_key].append(value)

    return data


def extract_data(content):
    """Extract data from content.

    Extract all the lines in the
    `\\begindata` sections.

    Parameters
    ----------
    content: str
        Kernel content.

    Returns
    -------
    [str]
        List of data lines.

    """
    read = False
    for line in content.splitlines():
        if r'\begindata' in line:
            read = True
        elif r'\begintext' in line:
            read = False
        elif read:  # pylint: disable=missing-parentheses-for-call-in-test, using-constant-test  # noqa: E501
            yield line


def parse(line):
    """Parse data line."""
    if '=' in line:
        k, v = line.split('=', 1)

        return k.strip(), read(v)

    return None, read(line)


def read(value):
    """Type value.

    Note
    ----
    String must be single quoted.

    """
    v = value.strip()

    if v in ['', '(', ')']:
        return None

    if v.startswith('(') and v.endswith(')'):
        return list(read(val) for val in v[1:-1].split(','))

    if v.startswith("'") and v.endswith("'"):
        return v[1:-1]

    return float(v) if '.' in v else int(v)
