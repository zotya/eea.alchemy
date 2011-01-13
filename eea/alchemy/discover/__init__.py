""" Auto-discover geotags API
"""
import logging
from zope.interface import implements
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from interfaces import IDiscoverGeoTags
from interfaces import IAlchemyAPI
logger = logging.getLogger('eea.alchemy.discover')

ENTITY_TYPES = [
    'City',
    'Continent',
    'Country',
    'GeographicFeature',
    'Region',
    'StateOrCounty',
]

class DiscoverGeoTags(object):
    """ Common adapter to auto-discover geotags in context metadata
    """

    _alchemy = None

    def __init__(self, context):
        self.context = context

    @property
    def alchemy(self):
        if self._alchemy:
            return self._alchemy

        ptool = getToolByName(self.context, 'portal_properties')
        atool = getattr(ptool, 'alchemyapi', None)
        key = getattr(atool, 'key', '')
        if not key:
            logger.exception('AlchemyAPI key not set in portal_properties/alchemyapi')
            return self._alchemy

        self._alchemy = getUtility(IAlchemyAPI)
        self._alchemy.setAPIKey(key)
        return self._alchemy

    def __call__(self, metadata='title', etypes=ENTITY_TYPES):
        field = self.context.getField(metadata)
        if not field:
            raise StopIteration

        text = field.getAccessor(self.context)()
        if not text:
            raise StopIteration

        if not isinstance(text, (unicode, str)):
            raise StopIteration

        alchemy = self.alchemy
        if not alchemy:
            raise StopIteration

        try:
            res = alchemy.TextGetRankedNamedEntities(text)
        except Exception, err:
            logger.exception(err)
            raise StopIteration

        for entity in res.get('entities', []):
            etype = entity.get('type', '')
            if etype not in etypes:
                continue
            yield entity
