# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
DeclarativeBase = declarative_base()


def temporary_session(engine):
    """Return a session that can be used without transaction manager"""
    return scoped_session(sessionmaker(bind=engine))
