""" Auto-discover time periods
"""
import logging
from zope.interface import implements
from zope.component import getUtility
from eea.alchemy.interfaces import IDiscoverTime
from eea.alchemy.interfaces import IDiscoverUtility
from eea.alchemy.config import EEAMessageFactory as _
logger = logging.getLogger('eea.alchemy')

class DiscoverTime(object):
    """ Common adapter to auto-discover time periods in context metadata
    """
    implements(IDiscoverTime)
    title = _(u'Temporal coverage')

    def __init__(self, context):
        self.context = context
        self.field = 'temporalCoverage'
        self._metadata = ('title', 'description')

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
            logger.warn('%s has no %s schema field. Time coverage not set',
                        doc.absolute_url(1), self.field)
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
            try:
                start, end = text.split('-')
                start, end = int(start), int(end)
                tag = range(start, end+1)
            except Exception, err:
                logger.exception(err)
                continue
            else:
                tags = tags.union(tag)

        current = [int(year) for year in field.getAccessor(doc)()]
        tags = tags.union(current)
        tags = list(tags)
        tags.sort(reverse=True)
        if not set(tags).difference(current):
            return

        tags = [str(yr) for yr in tags]
        return (tags, 'Update %s for %s. Before: %s, After: %s' %
                            (self.field, doc.absolute_url(1), current, tags))

    @property
    def metadata(self):
        """ Getter
        """
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        """ Setter
        """
        if isinstance(value, (str, unicode)):
            value = (value,)
        self._metadata = value

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

        discover = getUtility(IDiscoverUtility, name=u'temporalCoverage')
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
        doc.reindexObject(idxs=['getTemporalCoverage'])
