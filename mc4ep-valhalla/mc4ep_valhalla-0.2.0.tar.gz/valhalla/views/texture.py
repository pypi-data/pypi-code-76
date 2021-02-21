from base64 import b64encode
from datetime import datetime
from typing import Union
from uuid import UUID

from flask import current_app, request
from nidhoggr.core.repository import BaseTextureRepo, BaseUserRepo
from nidhoggr.core.response import TextureStatusResponse
from nidhoggr.core.texture import ComplexTextureResponse, TextureRequest, TextureType, TextureUploadRequest
from nidhoggr.core.user import User

from valhalla.decorators import as_json, protected
from valhalla.utils import handle_status, validate_image, validate_metadata


@as_json
def fetch(uuid: UUID) -> Union[TextureStatusResponse, ComplexTextureResponse]:
    textures: BaseTextureRepo = current_app.textures
    users: BaseUserRepo = current_app.users

    user: User = handle_status(users.get_user(uuid=uuid))

    if user.synthetic:
        return TextureStatusResponse(message=f'There are no textures for synthetic user with uuid {uuid}')

    texture_request = TextureRequest(uuid=uuid, texture_types=list(TextureType))
    texture_response = handle_status(textures.get(request=texture_request))

    return ComplexTextureResponse(
        timestamp=int(datetime.now().timestamp() * 1000),
        profileId=user.uuid,
        profileName=user.login,
        textures=texture_response.textures
    )


@as_json
@protected
def put(uuid: UUID, kind: TextureType) -> TextureStatusResponse:
    raw_image = request.files.get('file')
    raw_metadata = request.form.to_dict()

    image = validate_image(raw_image=raw_image)
    metadata = validate_metadata(raw_metadata=raw_metadata)

    textures: BaseTextureRepo = current_app.textures

    upload_request = TextureUploadRequest(
        uuid=uuid,
        data=b64encode(image),
        kind=kind,
        metadata=metadata
    )

    return handle_status(textures.upload(request=upload_request))


@as_json
@protected
def post(uuid: UUID, kind: TextureType) -> TextureStatusResponse:
    return TextureStatusResponse(message="Web uploads disabled due to security reasons")


@as_json
@protected
def delete(uuid: UUID, kind: TextureType) -> TextureStatusResponse:
    textures: BaseTextureRepo = current_app.textures
    delete_request = TextureRequest(uuid=uuid, texture_types=[kind])

    return handle_status(textures.clear(request=delete_request))
