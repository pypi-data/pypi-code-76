from elasticsearch.exceptions import NotFoundError


class AioMixin:
    @classmethod
    async def aio_search(cls, *args, **kwargs):
        from insnail_ai_tools.elastic_search.aio_connection import aio_elastic_search

        assert aio_elastic_search, "未初始化 aio es的连接"
        search = await aio_elastic_search.search(index=cls.Index.name, *args, **kwargs)
        return search


class MongoSyncMixin:
    @classmethod
    async def create_or_update_from_mongo(cls, data: dict):
        _id = data.pop("_id")
        try:
            obj = cls.get(id=_id)
        except NotFoundError:
            obj = cls()
            obj.meta.id = _id

        for k, v in data.items():
            obj[k] = v
        obj.save()
        return obj
