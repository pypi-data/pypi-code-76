from django.urls import reverse
from rest_framework.test import APITestCase


class SettingsViewTestCase(APITestCase):
    def test_view(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(200, response.status_code)
        self.assertListEqual(
            ['language', 'base_layers', ],
            list(response.json())
        )
