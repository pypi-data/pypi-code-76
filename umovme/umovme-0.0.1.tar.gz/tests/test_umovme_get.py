import os

from umovme.cli import main
from umovme.client import UmovmeCenter

from unittest import TestCase


class TestGet(TestCase):

    def setUp(self):
        self.client = UmovmeCenter(os.environ.get('UMOVME_TOKEN'))

    def test_client(self):
        resource_list = self.client.partner.search()
        for resource_id in resource_list:
            partner = self.client.partner.read(resource_id)
            assert partner.description

    def test_agent(self):
        resource_list = self.client.agent.search()
        for resource_id in resource_list:
            agent = self.client.agent.read(resource_id)
            assert agent.id
            assert agent.active
            assert agent.login
            assert agent.name

    def test_teams(self):
        resource_list = self.client.team.search()
        for resource_id in resource_list:
            team = self.client.team.read(resource_id)
            assert team.description

    def test_itinerary(self):
        resource_list = self.client.itinerary.search()
        for resource_id in resource_list:
            itinerary = self.client.itinerary.read(resource_id)
            assert itinerary.description

    def test_item(self):
        resource_list = self.client.item.search()
        for resource_id in resource_list:
            item = self.client.item.read(resource_id)
            assert item.description

    def test_activity(self):
        resource_list = self.client.activity.search()
        for resource_id in resource_list:
            activity = self.client.activity.read(resource_id)
            assert activity.description

    def test_activity_history(self):
        resource_list = self.client.activity_history.search()
        for resource_id in resource_list:
            activity_history = self.client.activity_history.read(resource_id)
            assert activity_history.description

    def test_schedule(self):
        resource_list = self.client.schedule.search()
        for resource_id in resource_list:
            schedule = self.client.schedule.read(resource_id)
            assert schedule.description

    def test_schedule_item(self):
        resource_list = self.client.schedule_item.search()
        for resource_id in resource_list:
            schedule_item = self.client.schedule_item.read(resource_id)
            assert schedule_item.description
    #
    # def test_message(self):
    #     resource_list = self.client.message.search()
    #     for resource_id in resource_list:
    #         message = self.client.message.read(resource_id)
    #         assert message.description
