import uuid
import json
from rest_framework.test import APITestCase, APIClient

from djangoldp.serializers import LDListMixin, LDPSerializer
from djangoldp_account.models import LDPUser
from djangoldp_notification.models import Notification


class TestSubscription(APITestCase):
    def _get_random_user(self):
        return LDPUser.objects.create(email='{}@test.co.uk'.format(str(uuid.uuid4())), first_name='Test',
                                      last_name='Test', username=str(uuid.uuid4()))

    def _get_random_notification(self, recipient, author):
        return Notification.objects.create(user=recipient, author=author.urlid, object=author.urlid,
                                           unread=True)

    def setUpLoggedInUser(self):
        self.user = self._get_random_user()
        self.client.force_authenticate(user=self.user)

    def setUp(self):
        self.client = APIClient()
        LDListMixin.to_representation_cache.reset()
        LDPSerializer.to_representation_cache.reset()

    def test_indirect_cache(self):
        self.setUpLoggedInUser()
        author_user = self._get_random_user()
        notification = self._get_random_notification(recipient=self.user, author=author_user)
        self.assertEqual(notification.unread, True)

        # GET the inbox - should set the cache
        response = self.client.get("/users/{}/inbox/".format(self.user.username))
        self.assertEqual(response.status_code, 200)
        notif_serialized = response.data["ldp:contains"][0]
        self.assertEqual(notif_serialized["unread"], True)

        # PATCH the notification - should wipe the cache
        patch = {
            "unread": False,
            "@context": {
                "@vocab":"http://happy-dev.fr/owl/#",
                "unread": "http://happy-dev.fr/owl/#unread"
            }
        }
        response = self.client.patch("/notifications/{}/".format(notification.pk), data=json.dumps(patch),
                                     content_type="application/ld+json")
        notif_obj = Notification.objects.get(pk=notification.pk)
        self.assertEqual(notif_obj.unread, False)

        # GET the inbox - should now be read
        response = self.client.get("/users/{}/inbox/".format(self.user.username))
        self.assertEqual(response.status_code, 200)
        notif_serialized = response.data["ldp:contains"][0]
        self.assertEqual(notif_serialized["unread"], False)
