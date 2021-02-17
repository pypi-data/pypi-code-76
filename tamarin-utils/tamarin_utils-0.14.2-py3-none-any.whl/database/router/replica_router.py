from .utils import get_replica, PRIMARY_DB_ALIAS


class ReplicaRouter(object):
    """Router that sends all reads to a replica, all writes to default."""

    def db_for_read(self, model, **hints):
        """Send reads to replicas in round-robin."""
        return get_replica()

    def db_for_write(self, model, **hints):
        """Send all writes to the master."""
        return PRIMARY_DB_ALIAS

    def allow_relation(self, obj1, obj2, **hints):
        """Allow all relations, so FK validation stays quiet."""
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == PRIMARY_DB_ALIAS

    def allow_syncdb(self, db, model):
        """Only allow syncdb on the master."""
        return db == PRIMARY_DB_ALIAS
