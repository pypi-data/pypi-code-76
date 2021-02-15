# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.models.patchedrpm_rpm_repository import PatchedrpmRpmRepository  # noqa: E501
from pulpcore.client.pulp_rpm.rest import ApiException

class TestPatchedrpmRpmRepository(unittest.TestCase):
    """PatchedrpmRpmRepository unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PatchedrpmRpmRepository
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_rpm.models.patchedrpm_rpm_repository.PatchedrpmRpmRepository()  # noqa: E501
        if include_optional :
            return PatchedrpmRpmRepository(
                pulp_labels = None, 
                name = '0', 
                description = '0', 
                remote = '0', 
                metadata_signing_service = '0', 
                retain_package_versions = 0
            )
        else :
            return PatchedrpmRpmRepository(
        )

    def testPatchedrpmRpmRepository(self):
        """Test PatchedrpmRpmRepository"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
