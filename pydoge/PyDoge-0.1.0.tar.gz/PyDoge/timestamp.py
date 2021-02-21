from datetime import datetime


class Timestamp:
    def __init__(self, logger):
        self.logger = logger

    def __enter__(self):
        start = datetime.now()
        self.logger.info(f'start time: {start}')
        self.start = start

    def __exit__(self, exception_type, exception_value, traceback):
        end = datetime.now()
        duration = end - self.start

        self.logger.info(f'end time: {end}')
        self.logger.info(f'duration: {duration}')

        self.end = end
        self.duration = duration
