from pydantic import BaseModel


class AuthFirstPhaseRequest(BaseModel):
    name: str

    class Config:
        allow_mutation = False


class AuthFirstPhaseResponse(BaseModel):
    offline: bool
    serverId: str
    verifyToken: int

    class Config:
        allow_mutation = False


class AuthSecondPhaseRequest(AuthFirstPhaseRequest):
    verifyToken: int

    class Config:
        allow_mutation = False


class AuthSecondPhaseResponse(BaseModel):
    accessToken: str

    class Config:
        allow_mutation = False


class AuthCookie(BaseModel):
    ip: str
    token: int

    class Config:
        allow_mutation = False
