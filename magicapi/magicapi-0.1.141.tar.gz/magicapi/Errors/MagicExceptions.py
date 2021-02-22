from fastapi import Request

from magicapi import g

from fastapi.responses import JSONResponse

from pydantic import BaseModel


class MagicException(Exception):
    def __init__(self, message: str, json_response: dict = None):
        print(f"*MagicException*: {message=}")
        self.status_code: int = 501
        self.message: str = message
        self.json_response: dict = json_response or {}

    class MagicExceptionModel(BaseModel):
        status_code: int = 501
        message: str
        json_response: dict = {}

    def to_model(self) -> MagicExceptionModel:
        if self.message and not type(self.message) == str:
            self.message = str(self.message)
        return self.MagicExceptionModel(**self.__dict__)

    @classmethod
    def get_model(cls) -> type(MagicExceptionModel):
        return cls.MagicExceptionModel


class BackendException(MagicException):
    pass


class FrontendException(MagicException):
    pass


class FirestoreException(MagicException):
    pass


class TwilioException(MagicException):
    pass


class IgnoreException(MagicException):
    pass


@g.app.exception_handler(MagicException)
def backend_exception_handler(request: Request, exc: MagicException):
    print("EXC", exc.__dict__)
    magic_exception_model = exc.to_model()
    return JSONResponse(
        status_code=magic_exception_model.status_code,
        content=magic_exception_model.dict(),
    )
