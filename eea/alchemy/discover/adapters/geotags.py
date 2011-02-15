""" Auto-discover geotags API
"""
import logging
from zope.interface import implements
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from eea.alchemy.interfaces import IDiscoverGeoTags
from eea.alchemy.interfaces import IDiscoverGeographicalCoverage
logger = logging.getLogger('eea.alchemy.discover')

class DiscoverGeoTags(object):
    """ Common adapter to auto-discover geotags in context metadata
    """
    implements(IDiscoverGeoTags)

    def __init__(self, context):
        self.context = context
        self._key = None
        self._metadata = ('title', 'description')

    @property
    def key(self):
        """ AlchemyAPI key
        """
        if self._key:
            return self._key

        ptool = getToolByName(self.context, 'portal_properties')
        atool = getattr(ptool, 'alchemyapi', None)
        key = getattr(atool, 'key', '')
        if not key:
            logger.exception(
                'AlchemyAPI key not set in portal_properties/alchemyapi')
            return self._key

        self._key = key
        return key

    def metadata():
        """ Object's metadata to look in
        """
        def getMetadata(self):
            """ Getter
            """
            return self._metadata

        def setMetadata(self, value):
            """ Setter
            """
            if isinstance(value, (str, unicode)):
                value = (value,)
            self._metadata = value

        return property(getMetadata, setMetadata)
    metadata = metadata()

    def tags():
        """ Tags property
        """
        def getTags(self):
            """ Getter
            """
            if not self.key:
                return

            string = ""
            for prop in self.metadata:
                if getattr(self.context, 'getField', None):
                    # ATContentType
                    field = self.context.getField(prop)
                    if not field:
                        continue
                    text = field.getAccessor(self.context)()
                else:
                    # ZCatalog brain
                    text = getattr(self.context, prop, '')

                if not text:
                    continue

                if not isinstance(text, (unicode, str)):
                    continue

                string += '\n' + text

            discover = getUtility(IDiscoverGeographicalCoverage)
            if not discover:
                return

            string = string.strip()
            if not string:
                return

            for item in discover(self.key, string):
                yield item

        def setTags(self, value):
            """ Setter
            """
            logger.info('DiscoverGeoTags.setTags not implemented')

        return property(getTags, setTags)
    tags = tags()
