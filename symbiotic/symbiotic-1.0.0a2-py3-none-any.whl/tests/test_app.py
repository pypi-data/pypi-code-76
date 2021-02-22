from unittest import TestCase

from symbiotic.app import Symbiotic


class Test_Application_Unit(TestCase):

    def test_init(self):
        app = Symbiotic()
        self.assertIsNotNone(app)
        self.assertIsNotNone(app.container)
        self.assertIsNotNone(app.container.devices)
        self.assertIsNotNone(app.container.services)
