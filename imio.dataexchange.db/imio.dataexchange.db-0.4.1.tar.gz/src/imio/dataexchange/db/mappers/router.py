# -*- coding: utf-8 -*-

from imio.dataexchange.db import DeclarativeBase
from imio.dataexchange.db.base import MapperBase

import sqlalchemy as sa


class Router(DeclarativeBase, MapperBase):
    __tablename__ = u'router'
    __table_args__ = (
        sa.UniqueConstraint(u'client_id', u'application_id',
                            name='application_unique_id'),
    )

    pk = sa.Column(u'pk', sa.Integer, primary_key=True, unique=True,
                   nullable=False)

    add_date = sa.Column(u'add_date', sa.DateTime, nullable=False,
                         server_default=sa.func.now())

    update_date = sa.Column(u'update_date', sa.DateTime)

    client_id = sa.Column(u'client_id', sa.Text, nullable=False)

    application_id = sa.Column(u'application_id', sa.Text, nullable=False)

    url = sa.Column(u'url', sa.Text, nullable=False)
