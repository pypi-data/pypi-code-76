from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from ps.basic import Config

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_engine():
    """current_app.config['DATABASE'] is already mapped to the
    ps.basic.Config.herald_sqlite_filename
    """

    if "engine" not in g:
        # https://stackoverflow.com/questions/34009296/using-sqlalchemy-session-from-flask-raises-sqlite-objects-created-in-a-thread-c
        g.engine = create_engine(
            "sqlite:///"
            + current_app.config["DATABASE"]
            + "?check_same_thread=False"
        )

    # print(g.engine.url.database )
    # print(Config.herald_sqlite_filename)
    assert g.engine.url.database == Config.herald_sqlite_filename
    return g.engine


def close_engine(e=None):
    engine = g.pop("db", None)
    if engine is not None:
        # the engine is already poped - nothing more to do here
        pass


def get_session():
    engine = get_engine()
    if "session" not in g:
        g.session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )
    return g.session


def init_db():
    from ps.herald.model import Base

    engine = get_engine()
    Base.metadata.create_all(bind=engine)


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_engine)
    app.cli.add_command(init_db_command)
