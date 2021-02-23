from magicdb.Models import FrontendParserModel
from pydantic import EmailStr
from firebase_admin import auth


class CurrentUser(FrontendParserModel):
    uid: str
    phone_number: str = None
    email: EmailStr = None
    email_verified: bool = None
    auth_time: int
    iat: int
    exp: int
    iss: str = None
    aud: str = None
    user_id: str = None
    sub: str = None
    firebase: dict = {}
    display_name: str = None

    def update(self, **kwargs):
        return auth.update_user(self.uid, **kwargs)
