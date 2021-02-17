# Copyright 2020 Software Factory Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, List, Dict
from datetime import datetime
import pickle
import re
from sqlalchemy import create_engine, Column, Unicode, Float, LargeBinary, Integer
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from . import JobStore, JobDoesNotExistException, JobAlreadyExistsException
from ..job import Job


Base = declarative_base()
SessionCls = scoped_session(sessionmaker())


def db_user(func):
    def wrapper(self, *args, **kwargs):
        session = kwargs.get('session', None)
        session_exists = True

        if session is None:
            session = SessionCls()
            kwargs['session'] = session
            session_exists = False

        result = func(self, *args, **kwargs)

        if not session_exists:
            session.commit()
            session.close()

        return result
    return wrapper


class DbJob(Base):
    __tablename__ = 'yapsched_jobs'

    id = Column(Unicode(191, _warn_on_bytestring=False), primary_key=True)
    next_run_time = Column(Float(25), index=True)
    job_state = Column(LargeBinary, nullable=False)


class LastInstanceId(Base):
    __tablename__ = 'yapsched_last_instance_id'

    row = Column(Integer, primary_key=True)
    id = Column(Integer)


class SqlAlchemyJobStore(JobStore):
    def __init__(self, url: str = None, engine: Engine = None, engine_options: Optional[Dict] = None,
                 pickle_protocol=pickle.HIGHEST_PROTOCOL):
        super().__init__()
        self.pickle_protocol = pickle_protocol

        if engine is not None:
            self.engine: Engine = engine
        elif url is not None:
            self.engine: Engine = create_engine(url, **(engine_options or {}))
        else:
            raise ValueError('Need either "engine" or "url" defined')

        SessionCls.configure(bind=self.engine)

    def setup(self):
        super().setup()
        Base.metadata.create_all(self.engine)

    def teardown(self):
        super().teardown()
        self.engine.dispose()

    @db_user
    def add_job(self, job: Job, replace_existing: bool = True, session: Session = None):
        if self.contains_job(job.id):
            if not replace_existing:
                raise JobAlreadyExistsException(job.id)

            self.update_job(job, session=session)
            return

        if job.next_run_time is None and job.active:
            job.next_run_time = job.trigger.get_next_fire_time(None, None)

        self._logger.debug(f'Add job ({job}) next run time: {job.next_run_time}')

        new_job = DbJob(id=job.id,
                        next_run_time=job.get_next_run_time_ts(),
                        job_state=pickle.dumps(job.__getstate__(), self.pickle_protocol))
        session.add(new_job)

    @db_user
    def update_job(self, job: Job, session: Session = None):
        existing_job = self._get_db_job(job.id, session)

        if job.next_run_time is None and job.active:
            if existing_job.next_run_time is None:
                job.next_run_time = job.trigger.get_next_fire_time(None, None)
            else:
                job.next_run_time = datetime.fromtimestamp(existing_job.next_run_time, tz=self._scheduler.tz)

        self._logger.debug(f'Update job ({job}) next run time: {job.next_run_time}')

        existing_job.next_run_time = job.get_next_run_time_ts()
        existing_job.job_state = pickle.dumps(job.__getstate__(), self.pickle_protocol)

    @db_user
    def remove_job(self, job_id: str, session: Session = None):
        existing_job = self._get_db_job(job_id, session)
        self._logger.debug(f'Delete job ({self._reconstitute_job(existing_job)})')
        session.delete(existing_job)

    @db_user
    def remove_all_jobs(self, session=None):
        session.query(DbJob).delete()

    @db_user
    def get_job(self, job_id: str, session: Session = None) -> Job:
        existing_job = self._get_db_job(job_id, session)
        return self._reconstitute_job(existing_job)

    @db_user
    def get_jobs(self, pattern: str = None, session: Session = None) -> List[Job]:
        db_jobs = session.query(DbJob).order_by(DbJob.next_run_time.asc()).all()

        if pattern is not None:
            compiled_pattern = re.compile(pattern)
            db_jobs = filter(lambda db_job: compiled_pattern.fullmatch(db_job.id), db_jobs)

        return list(map(lambda db_job: self._reconstitute_job(db_job), db_jobs))

    @db_user
    def contains_job(self, job_id: str, session: Session = None) -> bool:
        try:
            self._get_db_job(job_id, session)
            return True
        except JobDoesNotExistException:
            return False

    @staticmethod
    def _get_db_job(job_id: str, session: Session) -> DbJob:
        existing_job = session.query(DbJob).get(job_id)
        if existing_job is None:
            raise JobDoesNotExistException(job_id)
        return existing_job

    @staticmethod
    def _reconstitute_job(db_job: DbJob):
        job_state = pickle.loads(db_job.job_state)
        job = object.__new__(Job)
        job.__setstate__(job_state)
        return job

    @db_user
    def _get_stored_instance_id(self, session: Session = None) -> int:
        last_instance_id: LastInstanceId = session.query(LastInstanceId).get(0)
        if last_instance_id is None:
            return 0
        return last_instance_id.id

    @db_user
    def _save_instance_id(self, instance_id: int, session: Session = None):
        last_instance_id: LastInstanceId = session.query(LastInstanceId).get(0)
        if last_instance_id is None:
            last_instance_id = LastInstanceId(row=0, id=instance_id)
            session.add(last_instance_id)
        else:
            last_instance_id.id = instance_id

        self._logger.debug(f'saved new instance ID ({instance_id})')
