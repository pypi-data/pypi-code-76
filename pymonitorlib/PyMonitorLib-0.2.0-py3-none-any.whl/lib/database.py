try:
    import influxdb
    INFLUXDB_SUPPORTED = True
except ImportError:
    INFLUXDB_SUPPORTED = False


class Database(object):

    def Close(self):
        raise NotImplementedError

    def Initialize(self):
        raise NotImplementedError

    def Write(self, metrics):
        raise NotImplementedError


class InfluxDatabase(Database):

    def __init__(self, config, precision='ms', logger=None):
        """
        InfluxDB database constructor.

        This class will throw a RuntimeError if InfluxDB is not supported in the
        current environment.

        :param config: Database configuration from the main configuration object.
        :param precision: Timestamp precision. Defaults to ms.
        :param logger: Logger instance to use otherwise logging will be ignored.
        """
        if not INFLUXDB_SUPPORTED:
            raise RuntimeError('InfluxDB is not installed')

        self.config = config
        self.precision = precision
        self.logger = logger
        self.handle = None

    def Close(self):
        """
        Close the InfluxDB connection if one is open.

        This function will only throw in the event that InfluxDB is not supported
        otherwise it is safe to call during shutdown.

        :return: None
        """
        if not INFLUXDB_SUPPORTED:
            raise RuntimeError('InfluxDB is not installed')
        if self.handle:
            try:
                self.handle.close()
            except Exception as e:
                if self.logger:
                    self.logger.warning('Failed to close influx db connection: {}'.format(e))

    def Initialize(self):
        """
        Initialize the InfluxDB connection.

        This class will throw a RuntimeError if InfluxDB is not supported in the
        current environment.

        :return: True on success or False if the connection fails.
        """
        if not INFLUXDB_SUPPORTED:
            raise RuntimeError('InfluxDB is not installed')
        try:
            self.handle = influxdb.InfluxDBClient(
                host=self.config['server'],
                port=self.config['port'],
                ssl=self.config['ssl'],
                verify_ssl=self.config['verify'],
                database=self.config['database'])
        except KeyError as e:
            # If any of the configuration options are missing we need to trigger a fatal
            # error because we cannot recover from this.
            raise RuntimeError("Missing configuration option '{}'".format(e.args[0]))
        except Exception as e:
            if self.logger:
                self.logger.error('Failed to initiate influx db connection: {}'.format(e))
            self.handle = None
            return False

        return True

    def Write(self, metrics):
        """
        Write metrics to the InfluxDB database.

        This class will throw a RuntimeError if InfluxDB is not supported in the
        current environment.

        :param metrics: metrics object generated that should be sent to InfluxDB.
        :return: True on success or False on failure.
        """
        if not INFLUXDB_SUPPORTED:
            raise RuntimeError('InfluxDB is not installed')
        if not self.handle and not self.Initialize():
            return False
        self.handle.write_points(metrics, time_precision=self.precision)
        return True
