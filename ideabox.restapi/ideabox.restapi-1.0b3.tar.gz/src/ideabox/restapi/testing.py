# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import ideabox.restapi


class IdeaboxRestapiLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=ideabox.restapi)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "ideabox.restapi:default")


IDEABOX_RESTAPI_FIXTURE = IdeaboxRestapiLayer()


IDEABOX_RESTAPI_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IDEABOX_RESTAPI_FIXTURE,), name="IdeaboxRestapiLayer:IntegrationTesting"
)


IDEABOX_RESTAPI_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IDEABOX_RESTAPI_FIXTURE,), name="IdeaboxRestapiLayer:FunctionalTesting"
)


IDEABOX_RESTAPI_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(IDEABOX_RESTAPI_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="IdeaboxRestapiLayer:AcceptanceTesting",
)
