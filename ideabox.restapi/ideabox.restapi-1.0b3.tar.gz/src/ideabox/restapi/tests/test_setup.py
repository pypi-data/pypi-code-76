# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer
from ideabox.restapi.testing import IDEABOX_RESTAPI_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that ideabox.restapi is properly installed."""

    layer = IDEABOX_RESTAPI_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if ideabox.restapi is installed."""
        self.assertTrue(self.installer.is_product_installed("ideabox.restapi"))

    def test_browserlayer(self):
        """Test that IIdeaboxRestapiLayer is registered."""
        from ideabox.restapi.interfaces import IIdeaboxRestapiLayer
        from plone.browserlayer import utils

        self.assertIn(IIdeaboxRestapiLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = IDEABOX_RESTAPI_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("ideabox.restapi")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if ideabox.restapi is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("ideabox.restapi"))

    def test_browserlayer_removed(self):
        """Test that IIdeaboxRestapiLayer is removed."""
        from ideabox.restapi.interfaces import IIdeaboxRestapiLayer
        from plone.browserlayer import utils

        self.assertNotIn(IIdeaboxRestapiLayer, utils.registered_layers())
