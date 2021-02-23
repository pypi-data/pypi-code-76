import os
import namegenerator

from umovme.cli import main
from umovme.client import UmovmeCenter

from unittest import TestCase


class TestGet(TestCase):

    def setUp(self):
        self.client = UmovmeCenter(os.environ.get('UMOVME_TOKEN'))

    # def test_agent(self):
    #     resource_list = self.client.agent.search()
    #
    #     result = self.client.agent.add(
    #         {
    #             'active': True,
    #             'agentType': {
    #                 'id': 89478,
    #             },
    #             'login': namegenerator.gen(separator=''),
    #             'name': 'kmee4 informatica ltda',
    #             'password': 'd421d8cd98f00b204e9800998ecf8427e',
    #         }
    #     )
    #
    #     resource_list = self.client.agent.search()
    #     pass

    def test_team(self):
        resource_list = self.client.team.search()
        result = self.client.team.add(
            {
                'active': True,
                'description': namegenerator.gen(separator=''),
                'alternativeIdentifier': namegenerator.gen(separator=''),
            }
        )
        new_resource_list = self.client.team.search()
        record_id = list(set(new_resource_list) - set(resource_list))
        assert int(result.resourceId) in record_id

        update_dict = {
            'id': int(result.resourceId),
            'description': namegenerator.gen(separator=''),
            'alternativeIdentifier': 'UPDATED',
        }

        self.client.team.update(update_dict)
        team_updated = self.client.team.read(result.resourceId)



