"""
Type checkers for lesana fields.

Warning: this part of the code is still in flux and it may change
significantly in a future release.
"""
import datetime
import decimal
import logging

import dateutil.parser

import xapian


class LesanaType:
    """
    Base class for lesana field types.
    """
    def __init__(self, field, types, value_index=None):
        self.field = field
        self.value_index = value_index

    def load(self, data):
        raise NotImplementedError

    def empty(self):
        raise NotImplementedError

    def auto(self, value):
        """
        Return an updated value, as appropriate for the field.

        Default is to return the value itself, but types can use their
        configuration to e.g. increment a numerical value or return the
        current date(time).
        """
        return value

    def _to_index_text(self, value):
        """
        Prepare a value for indexing.
        """
        return str(value)

    def _to_value(self, value):
        """
        Prepare a value for indexing in a value slot
        """
        return str(value)

    def index(self, doc, indexer, value):
        """
        Index a value for this field type.

        Override this for types that need any kind of special treatment
        to be indexed.

        See LesanaList for an idea on how to do so.
        """
        to_index = self.field.get('index', False)
        if not to_index:
            return
        if not value:
            logging.info(
                "Not indexing empty value {}".format(value)
            )
            return
        prefix = self.field.get('prefix', 'X' + self.field['name'].upper())
        indexer.index_text(self._to_index_text(value), 1, prefix)
        if to_index == 'free':
            indexer.index_text(self._to_index_text(value))
            indexer.increase_termpos()
        if self.field.get('sortable', False):
            if self.value_index and self.value_index >= 16:
                doc.add_value(self.value_index, self._to_value(value))
            else:
                logging.debug(
                    "Index values up to 8 are reserved for internal use"
                )


class LesanaString(LesanaType):
    """
    A string of unicode text
    """
    name = 'string'

    def load(self, data):
        if not data:
            return data
        return str(data)

    def empty(self):
        return ""


class LesanaText(LesanaString):
    """
    A longer block of unicode text
    """
    name = 'text'


class LesanaInt(LesanaType):
    """
    An integer number
    """
    name = "integer"

    def load(self, data):
        if not data:
            return data
        try:
            return int(data)
        except ValueError:
            raise LesanaValueError(
                "Invalid value for integer field: {}".format(data)
            )

    def empty(self):
        return 0

    def _to_index_text(self, value):
        """
        Prepare a value for indexing.
        """
        return str(value)

    def _to_value(self, value):
        """
        Prepare a value for indexing in a value slot
        """
        return xapian.sortable_serialise(value)

    def auto(self, value):
        """
        Return an updated value.

        If the field settings ``auto`` is ``increment`` return the value
        incremented by the value of the field setting ``increment``
        (default 1).

        """
        if self.field.get('auto', False) == 'increment':
            increment = self.field.get('increment', 1)
            if int(increment) == increment:
                return value + increment
            else:
                logging.warning(
                    "Invalid configuration value for increment in field %s: "
                    + "%s",
                    self.field['name'],
                    increment,
                )

        return value


class LesanaFloat(LesanaType):
    """
    A floating point number
    """
    name = "float"

    def load(self, data):
        if not data:
            return data
        try:
            return float(data)
        except ValueError:
            raise LesanaValueError(
                "Invalid value for float field: {}".format(data)
            )

    def empty(self):
        return 0.0


class LesanaDecimal(LesanaType):
    """
    A floating point number
    """
    name = "decimal"

    def load(self, data):
        if not data:
            return data
        try:
            return decimal.Decimal(data)
        except decimal.InvalidOperation:
            raise LesanaValueError(
                "Invalid value for decimal field: {}".format(data)
            )

    def empty(self):
        return decimal.Decimal(0)


class LesanaTimestamp(LesanaType):
    """
    A unix timestamp, assumed to be UTC
    """
    name = "timestamp"

    def load(self, data):
        if not data:
            return data
        if isinstance(data, datetime.datetime):
            return data
        try:
            return datetime.datetime.fromtimestamp(
                int(data),
                datetime.timezone.utc,
            )
        except (TypeError, ValueError):
            raise LesanaValueError(
                "Invalid value for timestamp field: {}".format(data)
            )

    def empty(self):
        return None


class LesanaDatetime(LesanaType):
    """
    A datetime
    """
    name = "datetime"

    def load(self, data):
        if not data:
            return data
        if isinstance(data, datetime.datetime):
            return data
        if isinstance(data, datetime.date):
            return datetime.datetime(data.year, data.month, data.day)
        # compatibility with dateutil before 2.8
        ParserError = getattr(dateutil.parser, 'ParserError', ValueError)
        try:
            return dateutil.parser.parse(data)
        except ParserError:
            raise LesanaValueError(
                "Invalid value for datetime field: {}".format(data)
            )

    def empty(self):
        if self.field.get('auto', False) in ('creation', 'update'):
            return datetime.datetime.now(datetime.timezone.utc)

        return None

    def auto(self, value):
        """
        Return an updated value.

        If the field settings ``auto`` is ``update`` return the current
        datetime, otherwise the old value.

        """
        if self.field.get('auto', False) == 'update':
            return datetime.datetime.now(datetime.timezone.utc)

        return value


class LesanaDate(LesanaType):
    """
    A date
    """
    name = "date"

    def load(self, data):
        if not data:
            return data
        if isinstance(data, datetime.date):
            return data
        # compatibility with dateutil before 2.8
        ParserError = getattr(dateutil.parser, 'ParserError', ValueError)
        try:
            return dateutil.parser.parse(data)
        except ParserError:
            raise LesanaValueError(
                "Invalid value for date field: {}".format(data)
            )

    def empty(self):
        if self.field.get('auto', False) in ('creation', 'update'):
            return datetime.date.today()

        return None

    def auto(self, value):
        """
        Return an updated value.

        If the field settings ``auto`` is ``update`` return the current
        date, otherwise the old value.

        """
        if self.field.get('auto', False) == 'update':
            return datetime.date.today()

        return value


class LesanaBoolean(LesanaType):
    """
    A boolean value
    """
    name = 'boolean'

    def load(self, data):
        if not data:
            return data
        if isinstance(data, bool):
            return data
        else:
            raise LesanaValueError(
                "Invalid value for boolean field: {}".format(data)
            )

    def empty(self):
        return None


class LesanaFile(LesanaString):
    """
    A path to a local file.

    Relative paths are assumed to be relative to the base lesana
    directory (i.e. where .lesana lives)
    """
    name = 'file'


class LesanaURL(LesanaString):
    """
    An URL
    """
    name = 'url'


class LesanaYAML(LesanaType):
    """
    Free YAML contents (no structure is enforced)
    """
    name = 'yaml'

    def load(self, data):
        return data

    def empty(self):
        return None


class LesanaList(LesanaType):
    """
    A list of other values
    """

    name = 'list'

    def __init__(self, field, types, value_index=None):
        super().__init__(field, types, value_index)
        try:
            self.sub_type = types[field['list']](field, types)
        except KeyError:
            logging.warning(
                "Unknown field type %s in field %s",
                field['type'],
                field['name'],
            )
            self.sub_type = types['yaml'](field, types)

    def load(self, data):
        if data is None:
            # empty for this type means an empty list
            return []
        try:
            return [self.sub_type.load(x) for x in data]
        except TypeError:
            raise LesanaValueError(
                "Invalid value for list field: {}".format(data)
            )

    def empty(self):
        return []

    def index(self, doc, indexer, value):
        for v in value:
            self.sub_type.index(doc, indexer, v)


class LesanaValueError(ValueError):
    """
    Raised in case of validation errors.
    """
