import datetime
import os
import unittest
from decimal import Decimal

from talar.main import Talar

config = {
    "project_id": os.environ["TALAR_PROJECT_ID"],
    "api_key": os.environ["TALAR_API_KEY"],
    "api_version": os.environ.get("TALAR_API_VERSION"),
    "api_base": os.environ.get("TALAR_API_URL"),
}

talar = Talar(**config)


class ProjectsResourceTestCase(unittest.TestCase):
    def test_get(self):
        project = talar.projects.get()
        self.assertEqual(config["project_id"], project.id)
        self.assertIsNotNone(project.name)
        self.assertIsNotNone(project.url)


class ApiKeysResourceTestCase(unittest.TestCase):
    def test_get(self):
        api_key = talar.projects.api_keys.create("Test", "publishable")
        api_key = talar.projects.api_keys.get(api_key.digest)
        self.assertEqual("Test", api_key.name)
        self.assertEqual("publishable", api_key.type)
        self.assertEqual("", api_key.description)
        self.assertIsNotNone(api_key.digest)
        self.assertIsNotNone(api_key.prefix)
        self.assertIsNotNone(api_key.created_at)

    def test_list(self):
        api_key1 = talar.projects.api_keys.create("Test", "publishable")
        api_key2 = talar.projects.api_keys.create("Test", "publishable")
        api_keys = talar.projects.api_keys.list()
        api_keys_digests = [api_key.digest for api_key in api_keys]
        self.assertIn(api_key1.digest, api_keys_digests)
        self.assertIn(api_key2.digest, api_keys_digests)

    def test_delete(self):
        api_key = talar.projects.api_keys.create("Test", "publishable")
        self.assertIsNone(talar.projects.api_keys.delete(api_key.digest))

    def test_create(self):
        api_key = talar.projects.api_keys.create("Test", "publishable")
        self.assertEqual("Test", api_key.name)
        self.assertEqual("publishable", api_key.type)
        self.assertEqual("", api_key.description)
        self.assertIsNotNone(api_key.digest)
        self.assertIsNotNone(api_key.token)
        self.assertEqual(api_key.token[:5], api_key.prefix)
        self.assertIsNotNone(api_key.created_at)

    def test_create_full_type(self):
        api_key = talar.projects.api_keys.create("Test", "full")
        self.assertEqual("full", api_key.type)

    def test_create_with_description(self):
        api_key = talar.projects.api_keys.create(
            "Test", "publishable", "My description"
        )
        self.assertEqual("My description", api_key.description)

    def test_update(self):
        api_key = talar.projects.api_keys.create("Test", "publishable")

        api_key = talar.projects.api_keys.update(
            api_key.digest, name="Updated name"
        )
        self.assertEqual("Updated name", api_key.name)

        api_key = talar.projects.api_keys.update(
            api_key.digest,
            name=api_key.name,
            description="Updated description",
        )
        self.assertEqual("Updated description", api_key.description)


class CurrencyConversionsResourceTestCase(unittest.TestCase):
    def test_convert_historical(self):
        conversion = talar.currency_conversions.convert(
            Decimal("25.87"), "PLN", "EUR", datetime.date(2021, 2, 16)
        )
        self.assertEqual(Decimal("25.87"), conversion.amount)
        self.assertEqual("PLN", conversion.from_currency)
        self.assertEqual("EUR", conversion.to_currency)
        self.assertEqual(datetime.date(2021, 2, 16), conversion.date)
        self.assertEqual(Decimal("4.497070"), conversion.rate)
        self.assertEqual(Decimal("5.75"), conversion.result)

    def test_convert_latest(self):
        conversion = talar.currency_conversions.convert(
            Decimal("25.87"), "PLN", "EUR"
        )
        self.assertEqual(Decimal("25.87"), conversion.amount)
        self.assertEqual("PLN", conversion.from_currency)
        self.assertEqual("EUR", conversion.to_currency)
        self.assertEqual(datetime.date.today(), conversion.date)
        self.assertIsNotNone(conversion.rate)
        self.assertIsNotNone(conversion.result)
