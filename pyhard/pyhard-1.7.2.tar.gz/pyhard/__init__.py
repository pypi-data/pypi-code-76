import logging
from pathlib import Path
from .measures import Measures


log_file = Path(__file__).parents[2] / "graphene.log"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

nh = logging.NullHandler()

formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")  # - %(name)s

nh.setFormatter(formatter)

logger.addHandler(nh)
