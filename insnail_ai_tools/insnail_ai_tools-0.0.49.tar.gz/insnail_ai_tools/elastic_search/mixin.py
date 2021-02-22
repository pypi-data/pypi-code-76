class AioMixin:
    @classmethod
    async def aio_search(cls, *args, **kwargs):
        from insnail_ai_tools.elastic_search.aio_connection import aio_elastic_search

        assert aio_elastic_search, "未初始化 aio es的连接"
        search = await aio_elastic_search.search(index=cls.Index.name, *args, **kwargs)
        return search
