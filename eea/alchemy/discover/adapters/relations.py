""" Auto-discover relatedItems
"""
import logging
from zope.interface import implements
from zope.component import getUtility
from eea.alchemy.interfaces import IDiscoverRelatedItems
from eea.alchemy.interfaces import IDiscoverUtility
from eea.alchemy.config import EEAMessageFactory as _
from eea.alchemy.discover.adapters import Discover
logger = logging.getLogger('eea.alchemy')

class DiscoverRelatedItems(Discover):
    """ Common adapter to auto-discover related items in context metadata
    """
    implements(IDiscoverRelatedItems)
    title = _(u'Related items')

    def __init__(self, context):
        super(DiscoverRelatedItems, self).__init__(context)
        self.field = 'relatedItems'
        self.index = 'relatedItems'

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

        tags = set()
        for tag in self.tags:
            text = tag.get('text')
            if not text:
                continue

    @property
    def tags(self):
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

        discover = getUtility(IDiscoverUtility, name=u'links')
        if not discover:
            return

        string = string.strip()
        if not string:
            return

        for item in discover(string):
            yield item

    @tags.setter
    def tags(self, value):
        """ Setter
        """
        data = self.preview
        if not data:
            return

        tags, info = data

        doc = self.context
        if getattr(doc, 'getObject', None):
            # ZCatalog brain
            doc = doc.getObject()

        field = doc.getField(self.field)
        mutator = field.getMutator(doc)

        logger.info(info)

        mutator(tags)
        doc.reindexObject(idxs=[self.index])