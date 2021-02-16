from typing import Dict, Tuple

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from constellate.database.migration.databasetype import DatabaseType
from constellate.database.migration.migrate import migrate
from constellate.database.migration.migrationaction import MigrationAction
from constellate.database.sqlalchemy.exception.vacumexception import VacumException
from constellate.database.sqlalchemy.sqlalchemy import SQLAlchemy


class SQLAlchemyPostgresql(SQLAlchemy):
    def __init__(self):
        super().__init__()

    def _create_engine(self, options: Dict) -> Tuple[str, object]:
        """
        :options:
        - host:str               . DB host
        - port:str               . DB port
        - username:str           . DB user name
        - password:str           . DB password
        - db_name:str            . DB name
        """
        # Create engine
        # - https://docs.sqlalchemy.org/en/14/dialects/postgresql.html
        connection_uri_no_scheme_no_db_name = (
            f"{options.get('username', None)}:{options.get('password', None)}@"
            f"{options.get('host', None)}:{options.get('port', None)}"
        )

        connection_uri = (
            f"postgresql://{connection_uri_no_scheme_no_db_name}/{options.get('db_name', None)}"
        )
        if not database_exists(connection_uri):
            self._create_database(
                connection_uri=f"postgresql://{connection_uri_no_scheme_no_db_name}",
                db_name=options.get("db_name", None),
            )

        engine = create_engine(connection_uri)
        return connection_uri, engine

    def _create_database(self, connection_uri: str = None, db_name: str = None, encoding="UTF8"):
        with create_engine(connection_uri, isolation_level="AUTOCOMMIT").connect() as connection:
            connection.execute(f"CREATE DATABASE {db_name} ENCODING {encoding};")

    def _migrate(self, options: Dict = {}):
        migrate(
            database_type=DatabaseType.POSTGRESQL,
            connection_url=self._conection_uri,
            migration_dirs=options.get("migration_dirs", []),
            action=MigrationAction.UP,
            logger=self._logger,
        )

    def _vacuum(self, options: Dict = {}):
        """
        :options:
        - profiles: A vacumm profile. Values:
        -- analyze: Updates statistics used by the planner (to speed up queries)
        -- default: Sensible defaults
        """
        # Vacuum requires a connection/session without transaction enabled.
        with self._engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            commands = {
                "analyze": ["VACUUM ANALYZE;"],
                "default": ["VACUUM (ANALYZE, VERBOSE);"],
            }
            for profile in options.get("profiles", ["default"]):
                for statement in commands[profile]:
                    try:
                        connection.execute(statement)
                    except BaseException as e:
                        raise Exception(f"Vacuum statement failed: {statement}") from e
