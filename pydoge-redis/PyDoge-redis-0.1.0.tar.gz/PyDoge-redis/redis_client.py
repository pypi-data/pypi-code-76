from redis import Redis


class RedisClient:
    def __init__(self, options):
        self.connection_options = options

    def __enter__(self):
        try:
            self.connection = Redis(
                **self.connection_options
            )
            return self.connection
        except Exception as e:
            raise Exception(f'ERROR: Cannot connect to Redis: {str(e)}')

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
