import logging

def setup_custom_logger(name, log_level=logging.INFO):
    logger = logging.getLogger(name)

    # log_format = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt=log_format)
    # logging.basicConfig(filename='dummy.log', level=logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.setLevel(log_level) # set log level
    logger.addHandler(handler)

    return logger

if __name__ == "__main__":
    logger = setup_custom_logger('root')
    logger.warning("test")
