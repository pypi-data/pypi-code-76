from typing import Dict

from sqlalchemy.exc import UnboundExecutionError
from sqlalchemy.orm import Session

from constellate.database.sqlalchemy.sqlalchemy import _SQLAlchemyInstance


class MultiEngineSession(Session):
    def __init__(self, instances: Dict[str, _SQLAlchemyInstance] = {}, **kwargs):
        super().__init__(**kwargs)
        self._instances = instances

    def get_bind(self, mapper=None, clause=None):
        try:
            return super(self).get_bind(mapper=mapper, clause=clause)
        except UnboundExecutionError:
            return self._get_bind(mapper=mapper, clause=clause)

    def _get_bind(self, mapper=None, clause=None):
        o = mapper.class_ in []
        return self._engines.get(key, None)
