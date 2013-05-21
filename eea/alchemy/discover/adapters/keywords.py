""" Auto-discover keywords
"""
import logging
from zope.interface import implements
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName

from eea.alchemy.config import EEAMessageFactory as _
from eea.alchemy.interfaces import IDiscoverTags
from eea.alchemy.interfaces import IDiscoverUtility
from eea.alchemy.discover.adapters import Discover
logger = logging.getLogger('eea.alchemy')

class DiscoverTags(Discover):
    """ Common adapter to auto-discover keywords in context metadata
    """
    implements(IDiscoverTags)
    title = _(u'Keywords')

    def __init__(self, context):
        super(DiscoverTags, self).__init__(context)
        self.field = u'subject'
        self.index = u'Subject'

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

        tags = set(tag.get('text') for tag in self.tags)
        current = field.getAccessor(doc)()
        if isinstance(current, (str, unicode)):
            current = (current,)

        duplicates = set()
        for tag in tags:
            if isinstance(tag, str):
                tag = tag.decode('utf-8')
            duplicates.add(tag.lower())

        for tag in current:
            if isinstance(tag, str):
                tag = tag.decode('utf-8')
            lower = tag.lower()
            if lower in duplicates:
                continue

            tags.add(tag)
            duplicates.add(lower)

        if not set(tag.lower() for tag in tags).difference(
            set(tag.lower() for tag in current)):
            return

        tags = list(tags)
        tags.sort()
        tags = tuple(tags)

        return (tags, 'Update %s for %s. Before: %s  After:  %s' %
                (self.field, doc.absolute_url(1), current, tags))

    @property
    def existing(self):
        """ Get existing keywords from ZCatalog
        """
        ctool = getToolByName(self.context, 'portal_catalog')
        index = ctool.Indexes.get(self.index, None)
        if not index:
            return
        for value in index.uniqueValues():
            yield value

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

            if isinstance(text, unicode):
                text = text.encode('utf-8')

            string += '\n' + text

        string = string.strip()
        if not string:
            return

        discover = getUtility(IDiscoverUtility, name=self.field)
        duplicates = set()
        items = discover(self.key, string)
        for item in items:
            keyword = item.get('text')
            if not isinstance(keyword, unicode):
                keyword = keyword.decode('utf-8')
                item['text'] = keyword

            keyword = keyword.lower()
            if keyword in duplicates:
                continue

            duplicates.add(keyword)
            yield item

        # Search in portal_catalog existing keywords
        for keyword in self.existing:
            if isinstance(keyword, str):
                keyword = keyword.decode('utf-8')

            lower = keyword.lower()
            if lower in duplicates:
                continue
            if lower not in string.decode('utf-8').lower():
                continue

            duplicates.add(lower)
            yield {
                'relevance': '100.0',
                'text': keyword
            }

