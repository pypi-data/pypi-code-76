from io import TextIOBase
from pathlib import Path
from typing import Optional, Union

from terality import TeralityTypeError, TeralityValueError


def write_output(content: str, output: Optional[Union[TextIOBase, str, Path]] = None, encoding: Optional[str] = None):
    if isinstance(output, TextIOBase):
        if encoding is not None:
            raise TeralityValueError('Encoding is specified but output is not a path-like')
        output.write(content)
    elif isinstance(output, (str, Path)):
        with open(output, 'w', encoding=encoding) as file:
            file.write(content)
    else:
        raise TeralityTypeError('Output must be TextIO-like or path-like')
