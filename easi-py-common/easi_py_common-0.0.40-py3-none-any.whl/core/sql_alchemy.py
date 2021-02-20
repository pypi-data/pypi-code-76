# -*- coding: utf-8 -*-
import random
from functools import partial

import sqlalchemy.orm as orm
from flask import current_app
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from flask_sqlalchemy import get_state
from sqlalchemy.ext.declarative import declarative_base

MASTER_DB = 'master'
SLAVE_DB = 'slave'
FIXED_SLAVE_BINDS = 'fixed_slave'
ANL_SLAVE_BINDS = 'anl_slave'  # 统计分析库
DW_SLAVE_BINDS = 'dw_slave'  # dw分析库


class RoutingSession(orm.Session):

    def __init__(self, db, autocommit=False, autoflush=False, **options):
        self.app = db.get_app()
        self.db = db
        self._model_changes = {}

        # session 唯一 id
        # self.sid = get_random_string(length=8)
        orm.Session.__init__(
            self, autocommit=autocommit, autoflush=autoflush,
            bind=db.engine,
            binds=db.get_binds(self.app), **options)

    def get_bind(self, mapper=None, clause=None):

        # 被操作对象的包名
        full_class_name = ''
        if mapper is not None:
            full_class_name = "%s.%s" % (
                mapper.class_.__module__,
                mapper.class_.__name__
            )

        try:
            state = get_state(self.app)
        except (AssertionError, AttributeError, TypeError) as err:
            self.app.logger.info.warning(
                "cant get configuration. default bind. Error:" + err)
            return orm.Session.get_bind(self, mapper, clause)

        """
        If there are no binds configured, connect using the default
        SQLALCHEMY_DATABASE_URI
        """
        if state is None or not self.app.config['SQLALCHEMY_BINDS']:
            if not self.app.debug:
                self.app.logger.info("Connecting -> DEFAULT")
            return orm.Session.get_bind(self, mapper, clause)

        elif self._name:
            # self.app.logger.info("Connecting -> {}".format(self._name))
            return state.db.get_engine(self.app, bind=self._name)

        # 写入请求使用 master
        # 操作被改动过的对象，也使用 master
        elif self._flushing or self._model_changes.get(full_class_name):
            bind_key = getattr(mapper.class_, "__bind_key__", MASTER_DB)

            self._model_changes[full_class_name] = True
            if self.app.debug:
                action = 'WRITE' if self._flushing else 'READ'
                self.app.logger.info(
                    "Connecting -> %s MASTER( %s - %s )" % (
                        action,
                        mapper.class_,
                        bind_key
                    )
                )
            return state.db.get_engine(self.app, bind=bind_key)

        # 其他请求使用 slave
        else:
            bind_key = getattr(mapper.class_, "__bind_key__", SLAVE_DB)
            slave_bind_key = "%s_slave" % bind_key
            if slave_bind_key in self.app.config['SQLALCHEMY_BINDS']:
                bind_key = slave_bind_key

            if self.app.debug:
                self.app.logger.info(
                    "Connecting -> READ SLAVE( %s - %s )" % (
                        mapper.class_, bind_key
                    )
                )
            return state.db.get_engine(self.app, bind=bind_key)

    _name = None

    def using_bind(self, name):
        s = RoutingSession(self.db)
        vars(s).update(vars(self))
        s._name = name
        return s


class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True


class RouteSQLAlchemy(SQLAlchemy):
    """可读写分离路由的 SQLALCHEMY 对象"""

    def __init__(self, *args, **kwargs):
        SQLAlchemy.__init__(self, *args, **kwargs)
        self.session.using_bind = lambda s: self.session().using_bind(s)

    def create_scoped_session(self, options=None):
        if options is None:
            options = {}
        scopefunc = options.pop('scopefunc', None)
        # print "create_scoped_session - options = ", options
        return orm.scoped_session(
            partial(RoutingSession, self, **options), scopefunc=scopefunc
        )

    def apply_driver_hacks(self, app, info, options):
        """设置一些 create_engine 时的参数"""

        if "isolation_level" not in options and hasattr(app.config, "ISOLATION_LEVEL"):
            options["isolation_level"] = app.config["ISOLATION_LEVEL"]

        if hasattr(app.config, "ECHO_RAW_SQL"):
            options['echo'] = app.config["ECHO_RAW_SQL"]
            # print "update options - ", options

        return super(RouteSQLAlchemy, self).apply_driver_hacks(app, info, options)

    def get_engine(self, app=None, bind=None):
        # 从固定的slave里随机获取一个，如果配置了的话
        if bind == FIXED_SLAVE_BINDS and 'SQLALCHEMY_BINDS_FIXED_SLAVE_COUNT' in current_app.config and \
                current_app.config['SQLALCHEMY_BINDS_FIXED_SLAVE_COUNT'] > 0:
            # 随机选则
            fixed_bind = '{}{}'.format(FIXED_SLAVE_BINDS,
                                       random.randint(1, current_app.config['SQLALCHEMY_BINDS_FIXED_SLAVE_COUNT']))
            try:
                return super(RouteSQLAlchemy, self).get_engine(current_app, fixed_bind)
            except AssertionError as e:
                current_app.logger.error('get fixed engine error:{}'.format(e))

        if bind == FIXED_SLAVE_BINDS:
            bind = SLAVE_DB

        return super(RouteSQLAlchemy, self).get_engine(app, bind)

    @property
    def engine(self):
        return self.get_engine(bind=SLAVE_DB)

    @property
    def fixed_engine(self):
        return self.get_engine(bind=FIXED_SLAVE_BINDS)

    @property
    def anl_engine(self):
        return self.get_engine(bind=ANL_SLAVE_BINDS)

    @property
    def dw_engine(self):
        return self.get_engine(bind=DW_SLAVE_BINDS)


def slave_db():
    return db.session.using_bind(SLAVE_DB)


def master_db():
    return db.session.using_bind(MASTER_DB)


def using_master_session_query(model):
    if model is None:
        return None
    return master_db().query(model)


def using_fixed_slave_session_query(model):
    if model is None:
        return None
    return db.session.using_bind(FIXED_SLAVE_BINDS).query(model)


db: SQLAlchemy = RouteSQLAlchemy()
Model = declarative_base()
