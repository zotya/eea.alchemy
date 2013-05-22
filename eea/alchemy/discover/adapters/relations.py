""" Auto-discover relatedItems
"""
import logging
from zope.interface import implements
from zope.component import getUtility
from zope.component.hooks import getSite
from plone.uuid.interfaces import IUUID
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

        current = [IUUID(obj, None) for obj in field.getAccessor(doc)()]
        tags = []
        for tag in self.tags:
            text = tag.get('text')
            if not text:
                continue

            if text.startswith('resolveuid/'):
                uid = text.split('/')[1]
                if uid not in tags:
                    tags.append(uid)
                continue

            try:
                obj = doc.unrestrictedTraverse(text)
            except Exception, err:
                logger.exception(err)
                continue
            else:
                uid = IUUID(obj, None)
                if uid and uid not in tags:
                    tags.append(uid)
                continue

        myuid = IUUID(doc, None)
        tags = [tag for tag in tags if (tag and tag != myuid)]
        if not set(tags).difference(current):
            return

        return (tags, 'Update %s for %s. Before: %s, After: %s' %
                (self.field, doc.absolute_url(1), current, tags))

    @property
    def tags(self):
        """ Getter
        """
        doc = self.context
        string = ""
        for prop in self.metadata:
            text = ''
            getObject = getattr(doc, 'getObject', None)

            # ZCatalog brain
            if getObject:
                text = getattr(doc, prop, '')
                if not text:
                    doc = getObject()

            # ATContentType
            if not text and getattr(doc, 'getField', None):
                field = doc.getField(prop)
                if not field:
                    continue
                text = field.getAccessor(doc)()

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

        site = getSite().absolute_url()
        for item in discover(string, match=site):
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
