""" Auto-discover time periods
"""
import logging
from zope.interface import implements
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from eea.alchemy.interfaces import IDiscoverTime
from eea.alchemy.interfaces import IDiscoverTemporalCoverage
logger = logging.getLogger('eea.alchemy.discover')

class DiscoverTime(object):
    """ Common adapter to auto-discover time periods in context metadata
    """
    def __init__(self, context):
        self.context = context

    def __call__(self, metadata=('Title', 'Description')):
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

        discover = getUtility(IDiscoverTemporalCoverage)
        if not discover:
            raise StopIteration

        for item in discover(string):
            yield item
