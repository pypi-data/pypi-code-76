from django.test import TestCase
from django.contrib.auth.models import User

from gn_places.config import GN_FTC_SCHEME
from gn_places.tests.constants import (
    USER, TEST_CONCEPT, TEST_PLACE, TEST_PLACE_FAULTY, ONLY_ID
)
from gn_places.models import GeoNamesPlace
from vocabs.models import SkosConceptScheme, SkosConcept


class GeoNamesPlaceTest(TestCase):
    """ Test module for SkosConceptScheme model """

    def setUp(self):
        self.user = User.objects.create_user(**USER)
        self.concept_scheme = SkosConceptScheme.objects.create(**GN_FTC_SCHEME)
        TEST_CONCEPT['scheme'] = self.concept_scheme
        self.concept = SkosConcept.objects.create(**TEST_CONCEPT)
        self.place = GeoNamesPlace.objects.create(**TEST_PLACE)
        self.faulty_pl = GeoNamesPlace.objects.create(**TEST_PLACE_FAULTY)
        self.pl_with_ft = GeoNamesPlace.objects.create(
            gn_feature=self.concept,
            **ONLY_ID
        )

    def test_001_scheme(self):
        concept_scheme = SkosConceptScheme.objects.get(title=GN_FTC_SCHEME['title'])
        self.assertEqual(concept_scheme.title, GN_FTC_SCHEME['title'])
        self.assertEqual(len(SkosConceptScheme.objects.all()), 1)

    def test_002_concept(self):
        concept = self.concept
        self.assertEqual(concept.notation, TEST_CONCEPT['notation'])

    def test_003_place(self):
        places = GeoNamesPlace.objects.all()
        self.assertEqual(places.count(), 3)
        self.faulty_pl.save()
        gn_feature = self.place.gn_feature
        self.assertEqual(gn_feature, self.concept)
        self.assertEqual(f"{self.place.gn_name}", f"{TEST_PLACE['gn_name']}")
        self.assertEqual(f"{self.faulty_pl}", f"{TEST_PLACE_FAULTY['gn_id']}")
        self.assertEqual(self.place.get_geonames_url(), f"https://sws.geonames.org/{self.place.gn_id}")
        self.assertEqual(
            self.faulty_pl.get_geonames_rdf(),
            f"https://sws.geonames.org/{self.faulty_pl.gn_id}/about.rdf"
        )

    def test_004_place__str__(self):
        """ tests the places's str method """
        print(f"{self.place}")
        self.assertEqual(
            f"{self.place}",
            f"{TEST_PLACE['gn_name']} ({TEST_PLACE['gn_country_code']}; {TEST_PLACE['gn_feature_code']})"
        )
