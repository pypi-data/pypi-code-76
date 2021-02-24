# update.py
from akerbp.mlops.core import logger
from akerbp.mlops.deployment.setup import setup_pipeline
from  akerbp.mlops.core.config import validate_user_settings

logging=logger.get_logger(name='mlops_core')

logging.info("Create or overwrite pipeline file")
setup_pipeline(overwrite=True) 
logging.info("Validate settings file")
validate_user_settings()
logging.info("Done!")
