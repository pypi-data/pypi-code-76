from base64 import b64decode
from typing import Union, Dict
from uuid import uuid4, UUID

from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from lavender.models import Texture, Token

from lavender.views.api.decorator import json_response
from nidhoggr.core.response import ErrorResponse, TextureStatusResponse
from nidhoggr.core.texture import SimpleTextureResponse, TextureRequest, TextureUploadRequest, TextureType, TextureItem

from lavender.decorators import typed, internal


def _clean_old_textures(*, uuid: UUID, kind: str):
    (
        Texture.objects
        .filter(token__uuid__exact=uuid)
        .filter(deleted=False)
        .filter(kind__exact=kind)
        .update(deleted=True)
    )


@csrf_exempt
@internal
@json_response
@typed
def get(req: TextureRequest) -> Union[ErrorResponse, SimpleTextureResponse]:
    textures: Dict[TextureType, Texture] = {}

    for texture_type in req.texture_types:
        textures[texture_type] = (
            Texture.objects
            .filter(token__uuid__exact=req.uuid)
            .filter(deleted=False)
            .filter(kind__exact=texture_type.value)
            .order_by('-created')
            .only('image')
            .first()
        )

    # TODO: Return metadata as well
    return SimpleTextureResponse(textures={
        texture_type: TextureItem(url=texture.image.url)
        for texture_type, texture
        in textures.items()
        if texture is not None
    })


@csrf_exempt
@internal
@json_response
@typed
def upload(req: TextureUploadRequest) -> Union[ErrorResponse, TextureStatusResponse]:
    token = Token.objects.filter(uuid__exact=req.uuid).get()
    # Mark all previous uploads as deleted
    _clean_old_textures(uuid=req.uuid, kind=req.kind.value)
    texture = Texture(
        token=token,
        deleted=False,
        kind=req.kind.value,
        # TODO: Save metadata as well
    )
    texture.image.save(f"{uuid4()}.png", ContentFile(b64decode(req.data)), save=False)
    texture.save()
    return TextureStatusResponse(message=f"Saved texture")


@csrf_exempt
@internal
@json_response
@typed
def clear(req: TextureRequest) -> Union[ErrorResponse, TextureStatusResponse]:
    for kind in req.texture_types:
        # TODO: Clear metadata as well?
        # Mark all previous uploads as deleted
        _clean_old_textures(uuid=req.uuid, kind=kind.value)

    return TextureStatusResponse(message="Cleaned requested textures")
