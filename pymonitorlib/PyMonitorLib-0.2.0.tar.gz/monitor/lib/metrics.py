from collections import deque
from datetime import datetime
from string import whitespace
from .config import ConversionFailure, ConvertValue
from .database import InfluxDatabase


class Metric(object):

    def __init__(self, entity, measurement, value):
        """
        Constructor for a single metric.

        :param entity: Identifier for the config entry which generated this measurement.
        :param measurement: String describing what this metric is recording.
        :param value: Raw value being record. The value will be serialized accordingly
                      when enqueued.
        """
        self.entity = entity
        self.timestamp = datetime.utcnow()
        self.measurement = measurement
        self.value = value

    @staticmethod
    def Sanitize(measurement):
        """
        Sanitize a measurement name. Removes whitespace and other separators and replaces
        them with an '_" (underscore).

        :param measurement: Measurement name
        :return: Sanitized string
        """
        for c in [' ', '.']:
            measurement = measurement.replace(c, '_')
        return measurement

    @staticmethod
    def TimeStamp(now=None):
        """
        Serialize a datetime into a ISO8601 date-time stamp.

        :param now: Optional datetime value. If None will default to utcnow().
        :return: Serialized date-time string.
        """
        now = now or datetime.utcnow()
        return now.strftime('%Y-%m-%dT%H:%M:%SZ')


class MetricPipeline(object):

    DEFAULT_BATCH_SIZE = 10

    def __init__(self, config, batchSize=DEFAULT_BATCH_SIZE, logger=None):
        """
        Constructor for the measurement pipeline.

        :param config: Full config from the Executor context.
        :param batchSize: Optional batch size. How many messages should be grouped into a single
                          call to the database.
        :param logger: Optional logger instance. If no instance is provided log messages will
                       be skipped.
        """
        self.config = config
        self.logger = logger
        self.batchSize = int(batchSize)
        self.queue = deque()
        self.database = None
        self.shutdown = False

    def __call__(self, metrics):
        self.Enqueue(metrics)

    def Enqueue(self, metrics):
        """
        Append a set of metrics onto the metric queue for sending to the backend database.
        Note that metrics are attempted after every iteration however if the database is
        unresponsive or unavailable then the metrics will remain in the queue until the
        database accepts them.

        :param metrics: A single metric or list of metrics which should be appended to the
                        end of the queue.
        :return: None
        """
        if self.shutdown:
            return
        if not isinstance(metrics, (list, set)):
            metrics = [metrics]
        for metric in metrics:
            if not isinstance(metric, Metric):
                if self.logger:
                    self.logger.warning('Invalid metric sent to the queue')
                continue
            try:
                metric.value = ConvertValue(
                    metric.value,
                    hint=self.config.GetField(metric.measurement))
            except KeyError:
                if self.logger:
                    self.logger.warning("Invalid metric '{}'".format(metric.measurement))
                continue
            except ConversionFailure:
                if self.logger:
                    self.logger.warning("Unable to convert measurement '{}' value '{}'"
                        .format(metric.measurement, metric.value))
                continue
            self.queue.append(metric)

    def Flush(self):
        """
        Flush the queue to the database. If any messages fail to send the queue will be unwound
        and retried on the next iteration pass. The inner loop will automatically handle
        batching based on the configured batch size.

        :return: None
        """
        if self.shutdown:
            return

        count = 0
        start = datetime.utcnow()
        status = True
        while status and not self.IsEmpty():
            metrics = []
            while len(metrics) < self.batchSize:
                try:
                    metrics.append(self.queue.popleft())
                except IndexError:
                    break
            points = []
            for metric in metrics:
                try:
                    points.append({
                        'measurement': Metric.Sanitize(metric.measurement),
                        'tags': self.config.GetTags(metric.entity),
                        'time': Metric.TimeStamp(metric.timestamp),
                        'fields': {'value': metric.value}})
                except KeyError:
                    continue
            try:
                if not self.database:
                    dbtype, config = self.config.GetDatabase()
                    if dbtype == 'influxdb':
                        self.database = InfluxDatabase(config, logger=self.logger, precision='ms')
                    else:
                        raise RuntimeError("Unknown database type '{}'".format(dbtype))

                self.database.Write(points)
            except RuntimeError as e:
                # Push any RuntimeErrors up to the main loop to handle. These usually indicate
                # that we need to crash.
                status = False
                raise e
            except Exception as e:
                if self.logger:
                    self.logger.error('Unhandled error sending metrics: {}'.format(e))
                status = False
            finally:
                if not status:
                    while metrics:
                        self.queue.appendleft(metrics.pop(-1))
            if status:
                count += len(points)

        stop = datetime.utcnow()
        if status and self.logger and count > 0:
            self.logger.debug("Uploaded '{}' metrics in {:.3f}ms"
                .format(count, (stop - start).total_seconds() * 1000))

    def IsEmpty(self):
        """
        Predicate to check if the message queue is empty.

        :return:
        """
        return len(self.queue) == 0

    def Reload(self, config):
        """
        Reload the configuration. This will trigger a full flush of the message queue to try
        and send the remaining messages to the database before re-initializing the connection.

        In the event of a failure the config will not be overwritten and reloaded.
        In the event of a successful flush, the database connection will be reconnected to handle
        a possible change in the database config.

        :param config: New config object from the Executor context.
        :return: None
        """
        if self.logger:
            self.logger.warning('Reloading metrics pipeline')
        try:
            self.Flush()
            if self.database:
                self.database.Close()
            self.database = None
            self.config = config
        except Exception as e:
            if self.logger:
                self.logger.warning('Error during reload: {}'.format(e))

    def Shutdown(self, crash=False):
        """
        Shutdown the message pipeline. This will flush the remaining metrics to the database
        before disconnecting the connection and setting the shutdown flag. If the database
        is not available this call wil not block and data could be lost.

        :return: None
        """
        try:
            self.Flush()
            if self.database:
                self.database.Close()
            self.database = None
        except Exception as e:
            if self.logger and not crash:
                self.logger.warning('Error during metric pipeline shutdown: {}'.format(e))
        self.shutdown = True
