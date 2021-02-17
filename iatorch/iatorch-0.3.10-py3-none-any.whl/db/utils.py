import os, logging, dirsync
from sqlalchemy import create_engine, inspect
from sqlalchemy_utils import database_exists
from alembic import command
from alembic.config import Config
from mlflow.store.tracking.dbmodels.initial_models import Base as InitialBase
from mlflow.store.tracking.dbmodels.models import SqlExperiment, SqlRun, SqlMetric, SqlParam, SqlTag, SqlExperimentTag, SqlLatestMetric
from mlflow.server import BACKEND_STORE_URI_ENV_VAR, ARTIFACT_ROOT_ENV_VAR, PROMETHEUS_EXPORTER_ENV_VAR
from mlflow.server.handlers import initialize_backend_stores, TrackingStoreRegistryWrapper, ModelRegistryStoreRegistryWrapper, STATIC_PREFIX_ENV_VAR
from iatorch.db import IATORCH_ALEMBIC_DIR, MLFLOW_ALEMBIC_DIR

_migrations_logger = logging.getLogger('migrations')
_migrations_logger.setLevel(logging.WARNING)

def _set_migrations(migrations_dir):
    # copy latest migration info
    if not os.path.exists(migrations_dir):
        os.makedirs(migrations_dir); os.chmod(migrations_dir, mode=0o775)
    versions_dir = os.path.join(migrations_dir, 'versions')
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir); os.chmod(versions_dir, mode=0o775)
    # sync migrations
    dirsync.sync(MLFLOW_ALEMBIC_DIR, migrations_dir, logger=_migrations_logger, action='sync', verbose=False)
    dirsync.sync(IATORCH_ALEMBIC_DIR, migrations_dir, logger=_migrations_logger, action='sync', verbose=False)

def require_local_database(results_dir):
    '''
    Get or create local sqlite database.
    
    Arguments
    ---------
    results_dir : str or path
      directory where results are saved
    '''
    #
    if not results_dir.startswith(('./', '/')):
        results_dir = f"./{results_dir}"
        
    # DEFAULT DATABASE NAME
    NAME = 'mlruns.db'
    
    # CREATE RESULTS DIR
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        os.chmod(results_dir, mode=0o775)
        
    # CREATE MIGRATIONS DIR
    migrations_dir = os.path.join(results_dir, 'migrations')
    _set_migrations(migrations_dir=migrations_dir)
        
    # SET store_uri, artifact_root
    store_uri = os.path.join('sqlite:///', results_dir, NAME)
    artifact_root = results_dir
    os.environ[ARTIFACT_ROOT_ENV_VAR] = artifact_root
    
    # create db if no exists
    engine = create_engine(store_uri)
    if not database_exists(store_uri):
        InitialBase.metadata.create_all(engine)
    else:
        required_tables = [table.__tablename__ for table in [SqlExperiment, SqlRun, SqlMetric, SqlParam, SqlTag, SqlExperimentTag, SqlLatestMetric]]
        current_tables = inspect(engine).get_table_names()
        if any([table not in current_tables for table in required_tables]):
            InitialBase.metadata.create_all(engine)
                
    # make migration if needed
    config = Config(os.path.join(migrations_dir, "alembic.ini"))
    config.set_section_option("logger_alembic", "level", "WARN")
    config.set_main_option("script_location", migrations_dir)
    config.set_main_option("sqlalchemy.url", store_uri)
    with engine.begin() as connection:
        config.attributes["connection"] = connection  # pylint: disable=E1137
        command.upgrade(config, "heads")
    
    return store_uri, artifact_root
