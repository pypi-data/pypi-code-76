import time
import random
import logging

logger = logging.getLogger(__name__)


def batch_filter_entrypoint(batch_item={}, config={}):
    data = batch_item.get("data", "data-field-missing")
    logger.info(f"TEST BATCH FILTER IS RUNNING WITH {data} ######################")
    if data == "fail":
        raise Exception("This is a failure test")
    elif data == "hang":
        logger.info("We are testing a hanging task by just waiting forever")
        time.sleep(1000000000)
    elif data == "fast":
        logger.info("We are simulating a fast task by completing immediately")
    elif data == "slow":
        logger.info("We are simulating a slow task by completing  after 1 min")
        time.sleep(60 * 1)
    elif data == "random":
        time_to_wait = 60.0 * random.uniform(0, 1)
        logger.info(f"We are simulating a randomly fast task by completing after a random interval between 0 and 1 minute. In this case it was {time_to_wait} seconds.")
        time.sleep(time_to_wait)
    else:
        logger.info(f"The data '{data}' was not recognized and so we don't know what to test.")
    logger.info("#########################################################")
