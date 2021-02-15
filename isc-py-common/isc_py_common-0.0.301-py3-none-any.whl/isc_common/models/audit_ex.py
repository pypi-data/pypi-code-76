import logging

from isc_common.auth.models.user import User
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditManager, AuditQuerySet, AuditModel

logger = logging.getLogger(__name__)


class AuditModelExQuerySet(AuditQuerySet):
    pass


class AuditModelExManager(AuditManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
            'parent': record.parent.id if record.parent else None,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return AuditModelExQuerySet(self.model, using=self._db)


class AuditModelEx(AuditModel):
    creator = ForeignKeyProtect(User)

    objects = AuditModelExManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = ' Расширенная AuditModel'
