from __future__ import annotations
from dubhe.utils import BaseModel
import peewee
import datetime


class AuthPo(BaseModel.BaseModel):
    name = peewee.CharField(unique=True)
    user_id = peewee.CharField()
    token = peewee.CharField()
    endpoint = peewee.CharField()
    access_token = peewee.CharField()
    expiry = peewee.DateTimeField(default=datetime.datetime.now)
    active_time = peewee.DateTimeField(default=datetime.datetime.min)

    def __str__(self) -> str:
        return f'AuthPo(name="{self.name}", active_time="{self.active_time}" )'

    @classmethod
    def upsert(cls, name: str, user_id: str, token: str, endpoint: str, expiry: datetime.datetime, access_token: str,
               active_time: str) -> int:

        ret = AuthPo.insert(name=name
                            , user_id=user_id
                            , token=token
                            , endpoint=endpoint
                            , expiry=expiry
                            , access_token=access_token
                            , active_time=active_time).on_conflict('replace').execute()

        return ret

    @classmethod
    def load_all(cls) -> list:
        return AuthPo.select().order_by(AuthPo.name)

    @classmethod
    def load_active(cls) -> AuthPo:
        po = AuthPo.select().order_by(AuthPo.active_time.desc()).limit(1).get()
        if po.active_time > datetime.datetime.min:
            return po
        else:
            return None
