""" Base test cases
"""
from Products.Five import zcml
from Products.Five import fiveconfigure
from fake import FakeAlchemyAPI, IAlchemyAPI
product_globals = globals()

# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_eea_alchemy():
    """Set up the additional products.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    fiveconfigure.debug_mode = True
    import Products.Five
    zcml.load_config('meta.zcml', Products.Five)

    import eea.alchemy
    zcml.load_config('configure.zcml', eea.alchemy)
    fiveconfigure.debug_mode = False

    try:
        ptc.installPackage('eea.alchemy')
    except AttributeError:
        #BBB Plone 2.5
        pass

    from zope.component import provideUtility
    provideUtility(FakeAlchemyAPI(), IAlchemyAPI)
    ptc.installProduct('Five')

    #BBB Plone 2.5
    try:
        import Products.FiveSite
    except ImportError:
        pass
    else:
        ptc.installProduct('FiveSite')

setup_eea_alchemy()
ptc.setupPloneSite(extension_profiles=('eea.alchemy:default',))

class EEAAlchemyTestCase(ptc.PloneTestCase):
    """Base class for integration tests for the 'EEA Alchemy' product.
    """

class EEAAlchemyFunctionalTestCase(ptc.FunctionalTestCase, EEAAlchemyTestCase):
    """Base class for functional integration tests for the 'EEA Alchemy' product.
    """
    def afterSetUp(self):
        """ Setup
        """
        sid = self.folder.invokeFactory('Folder', id='sandbox')
        sandbox = self.folder._getOb(sid)
        sandbox.processForm(data=1, metadata=1, values={
            'title': (
                "Formation of new land cover in the region of Valencia, Spain"
            ),
            'description': (
                "Urban sprawl 1990-2000 in the province of Venice "
                "using a 1 km x 1 km grid"
            ),
        })

        atool = self.portal.portal_properties.alchemyapi
        atool.key = '12345665766867'
