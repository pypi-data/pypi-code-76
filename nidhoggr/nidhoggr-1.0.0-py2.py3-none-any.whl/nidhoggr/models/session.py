from typing import Optional, List

from pydantic import BaseModel, UUID4

from nidhoggr.core.user import UserProperty
from nidhoggr.utils.transformer import YggdrasilRequestTransformer, JSONResponseTransformer


class JoinRequest(BaseModel, YggdrasilRequestTransformer):
    accessToken: UUID4
    selectedProfile: UUID4
    serverId: str

    class Config:
        allow_mutation = False


class HasJoinedRequest(BaseModel, YggdrasilRequestTransformer):
    username: str
    serverId: str
    ip: Optional[str]

    class Config:
        allow_mutation = False


class JoinedResponse(BaseModel, JSONResponseTransformer):
    id: UUID4
    name: str
    properties: List[UserProperty]

    class Config:
        allow_mutation = False


class ProfileRequest(BaseModel, YggdrasilRequestTransformer):
    id: UUID4
    unsigned: bool = False

    class Config:
        allow_mutation = False
