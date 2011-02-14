""" Auto-discover time periods
"""
import logging
from zope.interface import implements
from zope.component import getUtility
from eea.alchemy.interfaces import IDiscoverTime
from eea.alchemy.interfaces import IDiscoverTemporalCoverage
logger = logging.getLogger('eea.alchemy.discover')

class DiscoverTime(object):
    """ Common adapter to auto-discover time periods in context metadata
    """
    implements(IDiscoverTime)

    def __init__(self, context):
        self.context = context
        self._metadata = ('Title', 'Description')

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

            discover = getUtility(IDiscoverTemporalCoverage)
            if not discover:
                raise StopIteration

            string = string.strip()
            if not string:
                raise StopIteration

            for item in discover(string):
                yield item

        def setTags(self, value):
            """ Setter
            """
            logger.exception('DiscoverTime.setTags not implemented')

        return property(getTags, setTags)
    tags = tags()
