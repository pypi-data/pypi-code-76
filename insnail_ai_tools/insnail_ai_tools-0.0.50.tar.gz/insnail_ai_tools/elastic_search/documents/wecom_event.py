from elasticsearch_dsl import Document
from elasticsearch_dsl.field import Date, Keyword

from insnail_ai_tools.elastic_search.mixin import AioMixin, MongoSyncMixin


class WecomChangeExternalContactEventIndex(Document, AioMixin, MongoSyncMixin):
    event = Keyword()
    change_type = Keyword()
    welcome_code = Keyword()
    state = Keyword()
    user_id = Keyword()
    external_user_id = Keyword()
    create_time = Date()

    class Index:
        name = "wecom_change_external_contact_event"
