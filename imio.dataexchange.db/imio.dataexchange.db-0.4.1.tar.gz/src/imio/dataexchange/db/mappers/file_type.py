# -*- coding: utf-8 -*-

from imio.dataexchange.db import DeclarativeBase
from imio.dataexchange.db.base import MapperBase
from sqlalchemy import Column
from sqlalchemy import Text


class FileType(DeclarativeBase, MapperBase):
    __tablename__ = u'file_type'

    id = Column(u'id', Text, primary_key=True, unique=True, nullable=False)

    description = Column(u'description', Text, nullable=False)
