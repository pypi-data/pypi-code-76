import dateutil.parser
from .base_datatype_mapper import BaseDatatypeMapper
from datetime import datetime, timezone

class DatetimeMapper(BaseDatatypeMapper):
    """A Mapper class for Datetimes

    This mapper is typically used with the ``Datetime`` datatype. This class will
    automatically convert the passed in datetime to UTC as is required by DynamoDB

    https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBMapper.DataTypes.html

    For example::

        import datetime
        mapper = DatetimeMapper(String())
        mapper.map(datetime.datetime.now())
        {'S': '2020-05-22T00:03:46.664845+00:00'}

        mapper.reconstruct({'S': '2020-05-22T00:03:46.664845+00:00'})
        datetime.datetime(2020, 5, 22, 0, 4, 33, 144061, tzinfo=tzutc())
    """

    def resolve(self, value):
        """Convert the datetime into an ISO 8601 string

        Parameters:
            value: a datetime object. Can be timezone aware or unaware

        Returns:
            a ISO 8601 string representation of the value in UTC
        """
        return value.replace(tzinfo=timezone.utc).isoformat()

    def parse(self, value):
        """Convert the datetime string into a datetime object

        Since it uses ``dateutil.parser``, this should handle both
        ISO 8601 strings and timezone agnostic values, however
        if the record was creating using the `resolve()` method, a
        utc timezone should automatically be included

        Parameters:
            value: A string representation of a datetime. Typically the value should be
                an ISO 8601 string

        Returns:
            a datetime object
        """
        return dateutil.parser.parse(value)
