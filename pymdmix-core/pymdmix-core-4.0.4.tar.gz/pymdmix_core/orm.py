import sqlalchemy

from pymdmix_core.settings import SETTINGS

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_sql_uri() -> str:
    dialect = SETTINGS["pymdmix_core"]["orm"]["dialect"]
    if dialect == "sqlite":
        db_filename = SETTINGS.get_file(SETTINGS["pymdmix_core"]["orm"]["db_file"])
        return f"sqlite:///{db_filename}"
    else:
        raise NotImplementedError(f"the dialect {dialect} for sql orm is not supported yet")


SQL_ENGINE = sqlalchemy.create_engine(get_sql_uri())
SQL_SESSION = sessionmaker(bind=SQL_ENGINE)()

BaseModel = declarative_base()
