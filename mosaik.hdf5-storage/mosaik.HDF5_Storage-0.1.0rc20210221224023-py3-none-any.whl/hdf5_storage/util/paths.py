from os.path import abspath
from pathlib import Path

ROOT_PATH = Path(abspath(__file__)).parent.parent.parent.parent
DATA_PATH = ROOT_PATH / 'data'
