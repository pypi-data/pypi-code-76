from django.test import Client, TestCase
from django.urls import reverse
from gn_places.utils import gn_get_or_create

GN_URL = "https://www.geonames.org/2772400/linz.html"
GN_ID = 2772400


class GetOrCreateTest(TestCase):
    def setUp(self):
        self.item = gn_get_or_create(GN_URL)
        self.client = Client()
        self.ac_url = reverse('gn_places-ac:geonamesplace-autocomplete')

    def test_001_gn_get_or_create_attr(self):
        self.assertEqual(getattr(self.item, 'gn_id'), f"{GN_ID}")

    def test_002_gn_get_or_create_attr(self):
        self.assertEqual(getattr(self.item, 'gn_country_code'), "AT")

    def test_003_gn_get_or_create_no_duplicates(self):
        item = gn_get_or_create(GN_URL)
        self.assertEqual(item.gn_id, GN_ID)
        self.assertEqual(self.item, item)

    def test_004_autocomplete(self):
        rv = self.client.get(self.ac_url)
        self.assertEqual(rv.status_code, 200)

    def test_004_autocomplete_query(self):
        rv = self.client.get(f"{self.ac_url}?q=li")
        self.assertEqual(rv.status_code, 200)
        self.assertContains(rv, 'Linz')
