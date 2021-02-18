# pylint: skip-file
import os
import unittest

from unimatrix import environ
from unimatrix.conf import settings


class SettingsTestCase(unittest.TestCase):

    def setUp(self):
        settings.destroy()
        self.settings_module = os.environ.pop(
            'UNIMATRIX_SETTINGS_MODULE', None
        )

    def tearDown(self):
        if self.settings_module is not None:
            os.environ['UNIMATRIX_SETTINGS_MODULE'] = self.settings_module

    @settings.with_overrides(FOO=1)
    def test_override_decorator(self):
        self.assertEqual(settings.FOO, 1)

    def test_override_context(self):
        self.assertNotEqual(getattr(settings, 'FOO', None), 1)
        with settings.override(FOO=1):
            self.assertEqual(settings.FOO, 1)

    def test_settings_loads_unimatrix_settings_module(self):
        os.environ['UNIMATRIX_SETTINGS_MODULE'] = 'unimatrix.tests.settings'
        self.assertEqual(getattr(settings, 'BAR', 1), 2)

    def test_settings_has_DEBUG(self):
        self.assertIn('DEBUG', settings.available)

    def test_can_override_environment_variable(self):
        with settings.override(DEBUG=...):
            self.assertEqual(settings.DEBUG, ...)

    def test_settings_precedes_envrionment(self):
        os.environ['UNIMATRIX_SETTINGS_MODULE'] = 'unimatrix.tests.settings'
        self.assertNotEqual(
            settings.HTTP_CORS_TTL,
            environ.HTTP_CORS_TTL
        )
