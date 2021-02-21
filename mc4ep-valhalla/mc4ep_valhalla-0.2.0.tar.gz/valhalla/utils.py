from io import BytesIO
from typing import Union, TypeVar, Any, Dict, Type

from PIL import Image
from nidhoggr.core.response import ErrorResponse, TextureStatusResponse
from pydantic import BaseModel, ValidationError
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from werkzeug.exceptions import InternalServerError, BadRequest

from valhalla.decorators import as_json_error

T = TypeVar("T")
U = TypeVar("U", bound=BaseModel)


def handle_status(repository_response: Union[ErrorResponse, T]) -> T:
    if isinstance(repository_response, ErrorResponse):
        raise InternalServerError(description=repository_response.reason)
    return repository_response


@as_json_error
def error_handler(error: InternalServerError):
    return TextureStatusResponse(message=error.description)


def validate_image(*, raw_image: FileStorage) -> bytes:
    if not raw_image:
        raise BadRequest(description=f'Empty image')

    # Read (and return) raw data, because internal PIL representation is too inefficient
    data = raw_image.stream.read()

    with Image.open(BytesIO(data)) as image:
        if image.format != "PNG":
            raise BadRequest(description=f"Format not allowed: {image.format}")

        sizes = {64, 128, 256, 512, 1024, 2048}
        (width, height) = image.size
        valid = width / 2 == height or width == height

        if not valid or width not in sizes:
            raise BadRequest(description=f"Unsupported image size: {image.size}")
    return data


def validate_metadata(*, raw_metadata: Dict[Any, Any]):
    # TODO: Use pydantic model here
    if not all((
        isinstance(k, str) and isinstance(v, str)
        for k, v
        in raw_metadata.items()
    )):
        raise BadRequest(description=f"Malformed metadata")


def validate_form(*, form: ImmutableMultiDict, clazz: Type[U]) -> Union[ErrorResponse, U]:
    try:
        return clazz.parse_obj(form.to_dict())
    except ValidationError as e:
        raise BadRequest(description=str(e))

