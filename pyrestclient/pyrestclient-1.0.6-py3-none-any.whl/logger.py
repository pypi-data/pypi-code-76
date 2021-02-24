import logging


logger_name = 'RESTClient'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt='%(asctime)-15s | %(levelname)s | %(name)s:%(lineno)d | %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

# Console logger
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

# File logger
# fh = logging.FileHandler(f'{logger_name}.log', mode='w')
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(formatter)  # Add the formatter
# logger.addHandler(fh)  # Add the handlers to the logger
