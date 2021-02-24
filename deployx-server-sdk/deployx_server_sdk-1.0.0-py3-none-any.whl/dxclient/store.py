import logging

class FeaturePointStore:
    """
    add new point to redis
    update already created point in redis
    """

    def __init__(self):
        # * Initializate and check redis database
        logging.info('Save point in store')

        try:
            import redis
            from redis.connection import ConnectionError

            self.redis_db = False

            try:
                self.r = redis.Redis()
                self.r.ping()
                self.redis_db = True
            except ConnectionError:
                logging.info("Redis database is not running.")

        except ModuleNotFoundError:
            logging.info("Redis not installed. Use default statuses instead of redis database.")

    def init_user(self, config, user, point_key):
        self.config = config
        self.user = user
        self.point_key = point_key

    def save(self, status):
        identifier = '-'
        type_of_statuses = ['unique_identifier', 'UNIQUE_IDENTIFIER']
        for key in type_of_statuses:
            if key in self.user:
                identifier = self.user[key]
            
        self.r.hset(identifier, '{}_{}'.format(self.config.sdk_key, self.point_key), str(status))

    def decode_status(self, status): 
        if status == 'True':
            return True
        elif status == 'False':
            return False
        elif int(status) in range(10):
            return int(status)
        else:
            raise TypeError('Error while getting status. Check your point available.')

    def decode_byte_status(self, status):
        return self.decode_status(status.decode('utf-8'))