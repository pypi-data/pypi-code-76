# Built-in Modules
import os
from datetime import datetime, timedelta
from pathlib import Path

# Third Party Modules
import pandas as pd
import numpy as np
from dotenv import load_dotenv


def get_db_client_kwargs():
    if os.environ.get('host') is None:
        __load_env()

    return {
        'dbname': os.environ.get('PGDATABASE'),
        'user': os.environ.get('PGUSER'),
        'password': os.environ.get('PGPASSWORD'),
        'host': os.environ.get('PGHOST'),
        'port': os.environ.get('PGPORT'),
    }


def __load_env():
    env_path = Path('./') / '.env'
    load_dotenv(dotenv_path=env_path)