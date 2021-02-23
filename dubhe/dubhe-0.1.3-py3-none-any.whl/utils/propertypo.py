from __future__ import annotations
from dubhe.utils import BaseModel
import peewee


class PropertyPo(BaseModel.BaseModel):
    key = peewee.CharField(unique=True)
    value = peewee.CharField()

    def __str__(self) -> str:
        return f'PropertyPo(key="{self.key}", value="{self.value}" )'

    @classmethod
    def upsert(cls, key: str, value: str) -> int:
        ret = PropertyPo.insert(key=key, value=value).on_conflict('replace').execute()
        return ret

    @classmethod
    def load(cls, key: str) -> PropertyPo:
        query = PropertyPo.select().where(PropertyPo.key == key)

        if query.exists():
            return query.get()
        return None
