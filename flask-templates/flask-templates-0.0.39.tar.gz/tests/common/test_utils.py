from unittest import TestCase

from flask_templates.common.utils import *

class TestReplace_variables(TestCase):
    def test_replace_variables(self):
        self.assertEqual(replace_variables("adasd${ad:123}dasd,${ad}ffggtgt",ad='ccc'),"adasdcccdasd,cccffggtgt")
        self.assertEqual(replace_variables("adasd${ad:123}dasd,ffggtgt"),"adasd123dasd,ffggtgt")
