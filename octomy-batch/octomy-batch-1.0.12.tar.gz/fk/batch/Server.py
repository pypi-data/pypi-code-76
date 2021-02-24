from fk.batch.BatchProcessor import BatchProcessor


class Server:
    def __init__(self, config):
        self.config = config
        self.batch_processor = BatchProcessor(self.config)

    def verify(self):
        return self.batch_processor.verify()

    # Start server and serve until it is aborted
    def run(self):
        while True:
            # Do some work
            self.batch_processor.process()
