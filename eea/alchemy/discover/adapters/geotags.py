""" Auto-discover geotags API
"""
import logging
from zope.interface import implements
from zope.component import getUtility, queryAdapter
from zope.component.hooks import getSite
from eea.alchemy.interfaces import IDiscoverGeoTags
from eea.alchemy.interfaces import IDiscoverUtility
from eea.alchemy.controlpanel.interfaces import IAlchemySettings
from eea.alchemy.config import EEAMessageFactory as _
logger = logging.getLogger('eea.alchemy')

class DiscoverGeoTags(object):
    """ Common adapter to auto-discover geotags in context metadata
    """
    implements(IDiscoverGeoTags)
    title = _(u'Geographical coverage')

    def __init__(self, context):
        self.context = context
        self._key = None
        self.field = 'location'
        self._metadata = ('title', 'description')

    @property
    def key(self):
        """ AlchemyAPI key
        """
        if self._key is not None:
            return self._key

        site = getSite()
        settings = queryAdapter(site, IAlchemySettings)
        self._key = settings.token
        if not self._key:
            logger.exception(
                'AlchemyAPI key not set in Site Setup > Alchemy Settings')
            return self._key
        return self._key

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
            logger.warn('%s has no %s schema field. location not set',
                        doc.absolute_url(1), self.field)
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

        discover = getUtility(IDiscoverUtility, name=u'location')
        if not discover:
            return

        string = string.strip()
        if not string:
            return

        for item in discover(self.key, string):
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
        doc.reindexObject(idxs=[self.field])
