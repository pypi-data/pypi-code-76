import os
from ..utils.utils import _get_package_dir
from mlflow.store.db.utils import _get_package_dir as _get_mlflow_dir

IATORCH_PACKAGE_DIR = _get_package_dir()
IATORCH_ALEMBIC_DIR = os.path.join(IATORCH_PACKAGE_DIR, "db", "migrations")
MLFLOW_PACKAGE_DIR = _get_mlflow_dir()
MLFLOW_ALEMBIC_DIR = os.path.join(MLFLOW_PACKAGE_DIR, "store", "db_migrations")
