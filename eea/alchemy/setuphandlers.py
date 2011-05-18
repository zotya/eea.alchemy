""" Plone setup
"""
import logging
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger('eea.alchemy')

def setupAlchemy(site):
    """ Add alchemyapi properties
    """
    ptool = getToolByName(site, 'portal_properties')
    if 'alchemyapi' not in ptool.objectIds():
        ptool.addPropertySheet(id='alchemyapi', title='Alchemy API')
        alchemy = getattr(ptool, 'alchemyapi')
        alchemy.manage_addProperty('key', '', 'string')


def importVarious(self):
    """ Various imports
    """
    if self.readDataFile('eea.alchemy.txt') is None:
        return

    site = self.getSite()
    setup_tool = getToolByName(site, 'portal_setup')

    # jQuery
    setup_tool.runAllImportStepsFromProfile('profile-eea.jquery:01-jquery')

    # jQuery UI
    setup_tool.runAllImportStepsFromProfile('profile-eea.jquery:02-ui')

    #setup_tool.setImportContext('profile-eea.alchemy:default')

    # Setup alchemy API
    setupAlchemy(site)
