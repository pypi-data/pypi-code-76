import datetime
import decimal
import unittest

import xapian

from lesana import types


class testTypes(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _get_field_def(self, type_name):
        return {
            'type': type_name,
            'name': 'test_field',
        }

    def test_base(self):
        checker = types.LesanaType(self._get_field_def('base'), {})

        # The base class does not implement empty nor load
        with self.assertRaises(NotImplementedError):
            checker.empty()

        with self.assertRaises(NotImplementedError):
            checker.load("")

    def test_string(self):
        checker = types.LesanaString(self._get_field_def('string'), {})

        s = checker.empty()
        self.assertEqual(s, "")

        s = checker.load("Hello World!")
        self.assertEqual(s, "Hello World!")

        s = checker.load(None)
        self.assertEqual(s, None)

        v = checker.auto("Hello World!")
        self.assertEqual(v, "Hello World!")

    def test_text(self):
        checker = types.LesanaText(self._get_field_def('text'), {})

        s = checker.empty()
        self.assertEqual(s, "")

        s = checker.load("Hello World!")
        self.assertEqual(s, "Hello World!")

        s = checker.load(None)
        self.assertEqual(s, None)

        v = checker.auto("Hello World!")
        self.assertEqual(v, "Hello World!")

    def test_int(self):
        checker = types.LesanaInt(self._get_field_def('integer'), {})

        v = checker.empty()
        self.assertEqual(v, 0)

        v = checker.load("10")
        self.assertEqual(v, 10)

        v = checker.load(10.5)
        self.assertEqual(v, 10)

        for d in ("ten", "10.5"):
            with self.assertRaises(types.LesanaValueError):
                checker.load(d)

        v = checker.load(None)
        self.assertEqual(v, None)

        v = checker.auto(10)
        self.assertEqual(v, 10)

    def test_datetime_auto_increment(self):
        field_def = self._get_field_def('integer')
        field_def['auto'] = 'increment'
        checker = types.LesanaInt(field_def, {})

        v = checker.empty()
        self.assertEqual(v, 0)

        v = checker.auto(0)
        self.assertEqual(v, 1)

        field_def['increment'] = -1
        checker = types.LesanaInt(field_def, {})
        v = checker.auto(0)
        self.assertEqual(v, -1)

        field_def['increment'] = 0.5
        checker = types.LesanaInt(field_def, {})
        with self.assertLogs() as cm:
            v = checker.auto(0)
        self.assertIn('WARNING', cm.output[0])
        self.assertIn('Invalid configuration value', cm.output[0])
        self.assertEqual(v, 0)

        field_def['auto'] = 'false'
        checker = types.LesanaInt(field_def, {})
        v = checker.auto(0)
        self.assertEqual(v, 0)

    def test_float(self):
        checker = types.LesanaFloat(self._get_field_def('float'), {})

        v = checker.empty()
        self.assertEqual(v, 0.0)

        v = checker.load("10")
        self.assertEqual(v, 10)

        v = checker.load(10.5)
        self.assertEqual(v, 10.5)

        v = checker.load("10.5")
        self.assertEqual(v, 10.5)

        for d in ("ten"):
            with self.assertRaises(types.LesanaValueError):
                checker.load(d)

        v = checker.load(None)
        self.assertEqual(v, None)

        v = checker.auto(10.5)
        self.assertEqual(v, 10.5)

    def test_decimal(self):
        checker = types.LesanaDecimal(self._get_field_def('decimal'), {})

        v = checker.empty()
        self.assertEqual(v, decimal.Decimal(0))

        v = checker.load("10")
        self.assertEqual(v, decimal.Decimal(10))

        v = checker.load(10.5)
        self.assertEqual(v, decimal.Decimal(10.5))

        v = checker.load("10.5")
        self.assertEqual(v, decimal.Decimal(10.5))

        for d in ("ten"):
            with self.assertRaises(types.LesanaValueError):
                checker.load(d)

        v = checker.load(None)
        self.assertEqual(v, None)

        v = checker.auto(decimal.Decimal("10.5"))
        self.assertEqual(v, decimal.Decimal("10.5"))

    def test_timestamp(self):
        checker = types.LesanaTimestamp(self._get_field_def('timestamp'), {})

        v = checker.empty()
        self.assertEqual(v, None)

        now = datetime.datetime.now()
        v = checker.load(now)
        self.assertEqual(v, now)

        v = checker.load("1600000000")
        wanted = datetime.datetime(
            2020, 9, 13, 12, 26, 40, 0,
            datetime.timezone.utc,
        )
        self.assertEqual(v, wanted)

        today = datetime.date.today()
        for d in (
            today,
            "today",
            "2020-13-01", "2020-01-01",
            "2020-01-01 10:00"
        ):
            with self.assertRaises(types.LesanaValueError):
                checker.load(d)

        v = checker.load(None)
        self.assertEqual(v, None)

        v = checker.auto(today)
        self.assertEqual(v, today)

    def test_datetime(self):
        checker = types.LesanaDatetime(self._get_field_def('datetime'), {})

        v = checker.empty()
        self.assertEqual(v, None)

        now = datetime.datetime.now()
        v = checker.load(now)
        self.assertEqual(v, now)

        today = datetime.date.today()
        v = checker.load(today)
        self.assertIsInstance(v, datetime.datetime)
        for part in ('year', 'month', 'day'):
            self.assertEqual(getattr(v, part), getattr(today, part))

        v = checker.load("2020-01-01")
        self.assertEqual(v, datetime.datetime(2020, 1, 1))

        v = checker.load("2020-01-01 10:00")
        self.assertEqual(v, datetime.datetime(2020, 1, 1, 10, 0))

        for d in ("today", "2020-13-01"):
            with self.assertRaises(types.LesanaValueError):
                checker.load(d)

        v = checker.load(None)
        self.assertEqual(v, None)

        v = checker.auto(now)
        self.assertEqual(v, now)

    def test_datetime_auto(self):
        field_def = self._get_field_def('datetime')
        field_def['auto'] = 'creation'
        checker = types.LesanaDatetime(field_def, {})

        now = datetime.datetime.now()
        v = checker.empty()
        self.assertIsInstance(v, datetime.datetime)
        self.assertEqual(v.tzinfo, datetime.timezone.utc)
        self.assertEqual(v.year, now.year)

        field_def['auto'] = False
        checker = types.LesanaDatetime(field_def, {})

        v = checker.empty()
        self.assertEqual(v, None)

        # auto=update fields should also be filled at creation time
        field_def['auto'] = 'update'
        checker = types.LesanaDatetime(field_def, {})
        v = checker.empty()
        self.assertIsInstance(v, datetime.datetime)
        self.assertEqual(v.tzinfo, datetime.timezone.utc)
        self.assertEqual(v.year, now.year)

    def test_datetime_auto_update(self):
        field_def = self._get_field_def('datetime')
        field_def['auto'] = 'update'
        checker = types.LesanaDatetime(field_def, {})

        now = datetime.datetime.now()
        past = datetime.datetime(2016, 12, 10, 21, 2)
        # we pass a date in the past
        v = checker.auto(past)
        self.assertIsInstance(v, datetime.datetime)
        self.assertEqual(v.tzinfo, datetime.timezone.utc)
        # and we want to get a date in the present
        self.assertEqual(v.year, now.year)

        # with auto=False we want our old date instead
        field_def['auto'] = False
        checker = types.LesanaDatetime(field_def, {})

        v = checker.auto(past)
        self.assertEqual(v, past)

        # and the same should happen with auto=creation
        field_def['auto'] = 'creation'
        checker = types.LesanaDatetime(field_def, {})

        v = checker.auto(past)
        self.assertEqual(v, past)

    def test_date(self):
        checker = types.LesanaDate(self._get_field_def('date'), {})

        v = checker.empty()
        self.assertEqual(v, None)

        now = datetime.datetime.now()
        v = checker.load(now)
        self.assertIsInstance(v, datetime.date)
        for part in ('year', 'month', 'day'):
            self.assertEqual(getattr(v, part), getattr(now, part))

        today = datetime.date.today()
        v = checker.load(today)
        self.assertEqual(v, today)

        v = checker.load("2020-01-01")
        self.assertEqual(v, datetime.datetime(2020, 1, 1))

        v = checker.load("2020-01-01 10:00")
        self.assertEqual(v, datetime.datetime(2020, 1, 1, 10, 0))

        for d in ("today", "2020-13-01"):
            with self.assertRaises(types.LesanaValueError):
                checker.load(d)

        v = checker.load(None)
        self.assertEqual(v, None)

        v = checker.auto(today)
        self.assertEqual(v, today)

    def test_date_auto(self):
        field_def = self._get_field_def('date')
        field_def['auto'] = 'creation'
        checker = types.LesanaDate(field_def, {})

        today = datetime.date.today()
        v = checker.empty()
        self.assertIsInstance(v, datetime.date)
        self.assertEqual(v, today)

        field_def['auto'] = False
        checker = types.LesanaDate(field_def, {})

        v = checker.empty()
        self.assertEqual(v, None)

        # auto=update fields should also be filled at creation time
        field_def['auto'] = 'update'
        checker = types.LesanaDate(field_def, {})

        v = checker.empty()
        self.assertIsInstance(v, datetime.date)
        self.assertEqual(v, today)

    def test_date_auto_update(self):
        field_def = self._get_field_def('date')
        field_def['auto'] = 'update'
        checker = types.LesanaDate(field_def, {})

        today = datetime.date.today()
        past = datetime.date(2016, 12, 10)
        # we pass a date in the past
        v = checker.auto(past)
        self.assertIsInstance(v, datetime.date)
        # and we want to get a date in the present
        self.assertEqual(v, today)

        # with auto=False we want our old date instead
        field_def['auto'] = False
        checker = types.LesanaDate(field_def, {})

        v = checker.auto(past)
        self.assertEqual(v, past)

        # and the same should happen with auto=creation
        field_def['auto'] = 'creation'
        checker = types.LesanaDate(field_def, {})

        v = checker.auto(past)
        self.assertEqual(v, past)

    def test_boolean(self):
        checker = types.LesanaBoolean(self._get_field_def('boolean'), {})

        v = checker.empty()
        self.assertEqual(v, None)

        v = checker.load(True)
        self.assertEqual(v, True)

        for d in ("maybe", "yes", "no"):
            with self.assertRaises(types.LesanaValueError):
                checker.load(d)

        v = checker.load(None)
        self.assertEqual(v, None)

        v = checker.auto(True)
        self.assertEqual(v, True)

    def test_file(self):
        checker = types.LesanaFile(self._get_field_def('file'), {})

        v = checker.empty()
        self.assertEqual(v, "")

        v = checker.load("relative/path/to/file")
        self.assertEqual(v, "relative/path/to/file")

        v = checker.load(None)
        self.assertEqual(v, None)

        # TODO: check for invalid file paths

        v = checker.auto("relative/path/to/file")
        self.assertEqual(v, "relative/path/to/file")

    def test_url(self):
        checker = types.LesanaURL(self._get_field_def('url'), {})

        v = checker.empty()
        self.assertEqual(v, "")

        v = checker.load("http://example.org")
        self.assertEqual(v, "http://example.org")

        v = checker.load(None)
        self.assertEqual(v, None)

        # TODO: check for invalid URLs

        v = checker.auto("http://example.org")
        self.assertEqual(v, "http://example.org")

    def test_yaml(self):
        checker = types.LesanaYAML(self._get_field_def('yaml'), {})

        v = checker.empty()
        self.assertEqual(v, None)

        some_data = {
            'anything': 'goes',
            'everything': 42
        }
        v = checker.load(some_data)
        self.assertEqual(v, some_data)

        v = checker.load(None)
        self.assertEqual(v, None)

        v = checker.auto(some_data)
        self.assertEqual(v, some_data)

    def test_list(self):
        field_def = self._get_field_def('yaml')
        # we use one type that is easy to check for correct validation
        field_def['list'] = 'int'
        checker = types.LesanaList(field_def, {'int': types.LesanaInt})

        v = checker.empty()
        self.assertEqual(v, [])

        some_data = [1, 2, 3]
        v = checker.load(some_data)
        self.assertEqual(v, some_data)

        v = checker.load(None)
        self.assertEqual(v, [])

        for d in (['hello'], 1):
            with self.assertRaises(types.LesanaValueError):
                checker.load(d)

        v = checker.auto(some_data)
        self.assertEqual(v, some_data)

    def test_list_unknown_subtype(self):
        field_def = self._get_field_def('yaml')
        # we use one type that is easy to check for correct validation
        field_def['list'] = 'int'
        checker = types.LesanaList(field_def, {'yaml': types.LesanaYAML})

        v = checker.empty()
        self.assertEqual(v, [])

        some_data = [1, 2, 3]
        v = checker.load(some_data)
        self.assertEqual(v, some_data)

        some_data = ["hello"]
        v = checker.load(some_data)
        self.assertEqual(v, some_data)

        v = checker.load(None)
        self.assertEqual(v, [])

        for d in (1, 1.0):
            with self.assertRaises(types.LesanaValueError):
                checker.load(d)


class testTypeIndexing(unittest.TestCase):
    def setUp(self):
        self.doc = xapian.Document()
        self.indexer = xapian.TermGenerator()

    def _get_field_def(self, type_name):
        return {
            'type': type_name,
            'name': 'test_field',
            'index': 'field',
            'sortable': True,
        }

    def test_base(self):
        checker = types.LesanaType(self._get_field_def('base'), {}, 16)

        checker.index(self.doc, self.indexer, "some string")

    def test_base_value_index_too_low(self):
        checker = types.LesanaType(self._get_field_def('base'), {}, 1)

        checker.index(self.doc, self.indexer, "some string")

        # TODO: check that the string has not been indexed

    def test_string(self):
        checker = types.LesanaString(self._get_field_def('string'), {}, 16)

        checker.index(self.doc, self.indexer, "some string")

    def test_text(self):
        checker = types.LesanaText(self._get_field_def('text'), {}, 16)

        checker.index(self.doc, self.indexer, "some string")

    def test_int(self):
        checker = types.LesanaInt(self._get_field_def('integer'), {}, 16)

        checker.index(self.doc, self.indexer, 1)

    def test_float(self):
        checker = types.LesanaFloat(self._get_field_def('float'), {}, 16)

        checker.index(self.doc, self.indexer, 1.5)

    def test_decimal(self):
        checker = types.LesanaDecimal(self._get_field_def('decimal'), {}, 16)

        checker.index(self.doc, self.indexer, decimal.Decimal('1.0'))

    def test_timestamp(self):
        checker = types.LesanaTimestamp(
            self._get_field_def('timestamp'), {}, 16
        )

        checker.index(self.doc, self.indexer, 1600000000)

    def test_datetime(self):
        checker = types.LesanaDatetime(self._get_field_def('datetime'), {}, 16)

        checker.index(self.doc, self.indexer, datetime.datetime.now())

    def test_date(self):
        checker = types.LesanaDate(self._get_field_def('date'), {}, 16)

        checker.index(self.doc, self.indexer, datetime.date.today())

    def test_boolean(self):
        checker = types.LesanaBoolean(self._get_field_def('boolean'), {}, 16)

        checker.index(self.doc, self.indexer, True)

    def test_url(self):
        checker = types.LesanaURL(self._get_field_def('url'), {}, 16)

        checker.index(self.doc, self.indexer, "http://example.org")

    def test_yaml(self):
        checker = types.LesanaYAML(self._get_field_def('yaml'), {}, 16)

        checker.index(self.doc, self.indexer, {'a': 1, 'b': 2})

    def test_list(self):
        field_def = self._get_field_def('yaml')
        # we use one type that is easy to check for correct validation
        field_def['list'] = 'int'
        checker = types.LesanaList(field_def, {'int': types.LesanaInt}, 16)

        checker.index(self.doc, self.indexer, ["some", "thing"])


if __name__ == '__main__':
    unittest.main()
