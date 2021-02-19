# -*- coding: utf-8 -*-

from imio.dataexchange.db import DeclarativeBase
from imio.dataexchange.db.base import MapperBase
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Index
from sqlalchemy import Text
from sqlalchemy import func


class Request(DeclarativeBase, MapperBase):
    __tablename__ = u"request"

    uid = Column(u"uid", Text, primary_key=True, unique=True, nullable=False)

    internal_uid = Column(u"internal_uid", Text, nullable=False)

    date = Column(u"date", DateTime, nullable=False, server_default=func.now())

    response = Column(u"response", Text, nullable=True)

    expiration_date = Column(u"expiration_date", DateTime)

    expired = Column(u"expired", Boolean, nullable=False, server_default="false")

    __table_args__ = (
        Index(
            "request_response_idx",
            "internal_uid",
            "expiration_date",
            "date",
            postgresql_where=(response.isnot(None))
        ),
    )
