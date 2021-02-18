import os
from datetime import datetime, timezone

import psutil
import sqlalchemy
from sqlalchemy import create_engine

from seesaw.config import USER_DIR, logger

log = logger(__file__)

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker as _sessionmaker

Base = declarative_base()


def connect() -> sqlalchemy.orm.Session:
    log_db_file = "sqlite:///" + str(USER_DIR / "logs.sqlite")
    log.debug("Opening DB", path=log_db_file)
    engine = create_engine(log_db_file)

    Base.metadata.create_all(engine)

    Session = scoped_session(_sessionmaker())
    Session.configure(bind=engine)
    return Session()


class Event(Base):
    __tablename__ = "events"
    gid = Column(String, primary_key=True)
    timestamp = Column(String, nullable=False)
    ingestion_time = Column(String)
    message = Column(String, default="")
    region = Column(String, nullable=False)
    log_group = Column(String, nullable=False)
    log_stream = Column(String, nullable=False)

    @classmethod
    def from_json(cls, incoming):
        return Event(
            gid=incoming["eventId"],
            timestamp=datetime.fromtimestamp(
                incoming["timestamp"] / 1000, tz=timezone.utc
            ).isoformat(),
            ingestion_time=datetime.fromtimestamp(
                incoming["ingestionTime"] / 1000, tz=timezone.utc
            ).isoformat(),
            region=incoming["region"],
            message=incoming["message"],
            log_stream=incoming["logStreamName"],
            log_group=incoming["logGroupName"],
        )


def get_pid_start_iso() -> str:
    """Return the iso-formatted time the current process started.

    This helps us clear out old thread signatures"""
    pid_start_ts = psutil.Process(os.getpid()).create_time()
    return (
        datetime.utcfromtimestamp(pid_start_ts).replace(tzinfo=timezone.utc).isoformat()
    )


class LiveReader(Base):
    __tablename__ = "live_readers"
    pkey = Column(Integer, autoincrement=True, primary_key=True)
    pid = Column(String)
    log_group = Column(String)
    region = Column(String)
    initiated = Column(String, default=get_pid_start_iso)

    @classmethod
    def exists_for(cls, session: sqlalchemy.orm.Session, region: str, log_group: str):
        return (
            session.query(LiveReader)
            .filter(LiveReader.pid == os.getpid())
            .filter(LiveReader.region == region)
            .filter(LiveReader.log_group == log_group)
            .all()
        )

    @classmethod
    def destroy_other_region_readers(cls, session: sqlalchemy.orm.Session, region: str):
        for reader in (
            session.query(LiveReader)
            .filter(LiveReader.pid == os.getpid())
            .filter(LiveReader.region != region)
            .filter(LiveReader.initiated >= get_pid_start_iso())
            .all()
        ):
            session.delete(reader)
        session.commit()
