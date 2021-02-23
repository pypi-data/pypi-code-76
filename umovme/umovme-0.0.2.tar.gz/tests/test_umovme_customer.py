import os
import namegenerator

from umovme.cli import main
from umovme.client import UmovmeCenter

from unittest import TestCase


class TestGet(TestCase):

    def setUp(self):
        self.client = UmovmeCenter(os.environ.get('UMOVME_TOKEN'))

    def test_team(self):
        resource_list = self.client.team.search()

        result = self.client.team.add(
            {
                'active': True,
                'description': namegenerator.gen(separator=''),
                'alternativeIdentifier': namegenerator.gen(separator=''),
            }
        )

        resource_list = self.client.team.search()

