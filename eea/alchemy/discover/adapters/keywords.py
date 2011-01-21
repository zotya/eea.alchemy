""" Auto-discover keywords
"""
import logging
from zope.interface import implements
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from eea.alchemy.interfaces import IDiscoverTags
from eea.alchemy.interfaces import IDiscoverKeywords
logger = logging.getLogger('eea.alchemy.discover')

class DiscoverTags(object):
    """ Common adapter to auto-discover keywords in context metadata
    """
    def __init__(self, context):
        self.context = context
        self._key = None

    @property
    def key(self):
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

    @property
    def existing(self):
        """ Get existing keywords from ZCatalog
        """
        ctool = getToolByName(self.context, 'portal_catalog')
        index = ctool.Indexes.get('Subject', None)
        if not index:
            raise StopIteration
        for value in index.uniqueValues():
            yield value

    def __call__(self, metadata=('Title', 'Description')):
        if not self.key:
            raise StopIteration

        if isinstance(metadata, (unicode, str)):
            metadata = [metadata, ]

        string = ""
        for prop in metadata:
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

        discover = getUtility(IDiscoverKeywords)
        if not discover:
            raise StopIteration

        duplicates = []
        for item in discover(self.key, string):
            duplicates.append(item['text'])
            yield item

        # Search in portal_catalog existing keywords
        for keyword in self.existing:
            if keyword in duplicates:
                continue
            if keyword.lower() not in string.lower():
                continue

            yield {
                'relevance': '100.0',
                'text': keyword
            }
