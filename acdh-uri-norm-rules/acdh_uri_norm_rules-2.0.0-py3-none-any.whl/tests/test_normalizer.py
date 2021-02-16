import unittest
from AcdhUriNormRules.AcdhUriNormRules import get_rules, get_normalized_uri

SAMPLES = [
    [
        "http://sws.geonames.org/1232324343/linz.html",
        "https://www.geonames.org/1232324343"
    ],
    [
        "http://d-nb.info/gnd/4074255-6/",
        "https://d-nb.info/gnd/4074255-6"
    ],
    [
        "https://d-nb.info/gnd/4074255-6",
        "https://d-nb.info/gnd/4074255-6"
    ]
]

class TestNormalizer(unittest.TestCase):
    def test__001_load_list(self):
        rules = get_rules()
        self.assertEqual(type(rules), list, "should be type 'list' ")
    
    def test__002_test_patterns(self):
        for x in SAMPLES:
            new_uri = get_normalized_uri(x[0])
            self.assertEqual(x[1], new_uri)
