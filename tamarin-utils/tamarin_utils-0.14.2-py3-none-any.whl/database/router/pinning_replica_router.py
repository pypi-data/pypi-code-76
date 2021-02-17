from .utils import get_replica, this_thread_is_pinned, PRIMARY_DB_ALIAS
from .replica_router import ReplicaRouter
from django.conf import settings


class PinningReplicaRouter(ReplicaRouter):

    def db_for_read(self, model, **hints):
        return PRIMARY_DB_ALIAS if this_thread_is_pinned() else get_replica()
