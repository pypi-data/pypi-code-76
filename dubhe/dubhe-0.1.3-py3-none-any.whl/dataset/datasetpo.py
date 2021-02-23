from dubhe.utils import BaseModel
import peewee
import datetime


class DatasetPo(BaseModel.BaseModel):
    dataset_id = peewee.CharField()
    file_id = peewee.CharField()
    filename = peewee.CharField()
    server_create = peewee.DateTimeField()
    local_modify = peewee.DateTimeField()
    label = peewee.CharField()

    def __str__(self) -> str:
        return f'DatasetPo(name="{self.filename}", create="{self.server_create}" )'

    @classmethod
    def upsert(cls, dataset_id: str, file_id: str, filename: str, server_create: datetime.datetime,
               local_modify: datetime.datetime, label: list) -> int:
        ret = DatasetPo.insert(
            dataset_id=dataset_id
            , file_id=file_id
            , filename=filename
            , server_create=server_create
            , local_modify=local_modify
            , label=label).on_conflict('replace').execute()

        return ret

    @classmethod
    def delete_by_dataset_id(cls, dataset_id):
        ret = DatasetPo.delete().where(DatasetPo.dataset_id == dataset_id).execute()
        return ret

    @classmethod
    def load(cls, dataset_id: str, offset: int, limit: int) -> list:
        query = DatasetPo.select().where(DatasetPo.dataset_id == dataset_id).order_by(DatasetPo.server_create).offset(offset).limit(limit)
        return list(query)

    @classmethod
    def get_count(cls, dataset_id: str):
        return DatasetPo.select().where(DatasetPo.dataset_id == dataset_id).count()
