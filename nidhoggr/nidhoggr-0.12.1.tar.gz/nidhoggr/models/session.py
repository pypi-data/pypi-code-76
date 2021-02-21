from typing import Optional, List

from pydantic import BaseModel, UUID4

from nidhoggr.core.user import UserProperty
from nidhoggr.utils.transformer import YggdrasilRequestTransformer, JSONResponseTransformer, LegacyRequestTransformer


class JoinRequest(BaseModel, YggdrasilRequestTransformer):
    accessToken: UUID4
    selectedProfile: UUID4
    serverId: str

    class Config:
        allow_mutation = False


class HasJoinedRequestBase(BaseModel):
    username: str
    serverId: str
    ip: Optional[str]


class HasJoinedRequest(HasJoinedRequestBase, YggdrasilRequestTransformer):

    class Config:
        allow_mutation = False


class HasJoinedRequestLegacy(HasJoinedRequestBase, LegacyRequestTransformer):

    class Config:
        allow_mutation = False


class JoinedResponse(BaseModel, JSONResponseTransformer):
    id: UUID4
    name: str
    properties: List[UserProperty]

    class Config:
        allow_mutation = False


class ProfileRequestBase(BaseModel):
    id: UUID4
    unsigned: bool = False

    class Config:
        allow_mutation = False


class ProfileRequest(ProfileRequestBase, YggdrasilRequestTransformer):

    class Config:
        allow_mutation = False


class ProfileRequestLegacy(ProfileRequestBase, LegacyRequestTransformer):

    class Config:
        allow_mutation = False
