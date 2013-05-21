""" Auto-discover geotags API
"""
import logging
from zope.interface import implements
from zope.component import getUtility

from eea.alchemy.interfaces import IDiscoverGeoTags
from eea.alchemy.interfaces import IDiscoverUtility
from eea.alchemy.discover.adapters import Discover
from eea.alchemy.config import EEAMessageFactory as _

logger = logging.getLogger('eea.alchemy')

class DiscoverGeoTags(Discover):
    """ Common adapter to auto-discover geotags in context metadata
    """
    implements(IDiscoverGeoTags)
    title = _(u'Geographical coverage')

    def __init__(self, context):
        super(DiscoverGeoTags, self).__init__(context)
        self.field = u'location'
        self.index = u'location'

    @property
    def preview(self):
        """ Discovery preview
        """
        doc = self.context
        # ZCatalog brain
        if getattr(doc, 'getObject', None):
            doc = doc.getObject()

        field = doc.getField(self.field)
        if not field:
            logger.warn('%s has no %s schema field. %s not set',
                        doc.absolute_url(1), self.field, self.title)
            return

        mutator = field.getMutator(doc)
        if not mutator:
            logger.warn("Can't edit field %s for doc %s",
                        self.field, doc.absolute_url(1))
            return

        current = field.getAccessor(doc)()
        if current and isinstance(current, (str, unicode)):
            # Location already set, skip as we don't want to mess it
            return

        tags = set(tag.get('text') for tag in self.tags)
        if current:
            if isinstance(current, (str, unicode)):
                tags.add(current)
            else:
                tags = tags.union(current)

        if not tags:
            return

        tags = list(tags)
        tags.sort()
        if isinstance(current, (str, unicode)):
            tags = ', '.join(tags)

        return (tags, 'Update %s for %s. Before: %s  After: %s' %
                        (self.field, doc.absolute_url(1), current, tags))

    @property
    def tags(self):
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

        discover = getUtility(IDiscoverUtility, name=self.field)
        if not discover:
            return

        string = string.strip()
        if not string:
            return

        for item in discover(self.key, string):
            yield item
