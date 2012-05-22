from plone.testing import z2

from plone.app.testing import PLONE_FIXTURE, TEST_USER_ID
from plone.app.testing import PloneSandboxLayer, IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import setRoles, applyProfile


class BitPloneProjectTestLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import bit.plone.project
        self.loadZCML(package=bit.plone.project)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'bit.plone.project:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'bit.plone.project')

PROJECT_TEST_FIXTURE = BitPloneProjectTestLayer()
PROJECT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PROJECT_TEST_FIXTURE,),
    name="bit.plone.project:integration")
PROJECT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PROJECT_TEST_FIXTURE,),
    name="bit.plone.project:functional")
