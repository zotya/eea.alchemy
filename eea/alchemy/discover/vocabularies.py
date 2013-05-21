""" Vocabularies
"""
from zope.interface import implements
from zope.component import getAdapters, queryUtility
from zope.component.hooks import getSite
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from eea.alchemy.interfaces import IDiscoverAdapter
from Products.CMFCore.utils import getToolByName

class DiscoverAdapters(object):
    """ Vocabulary factory for all registered Alchemy Discover Adapters
    """
    implements(IVocabularyFactory)
    _adapter = None

    def adapters(self, context):
        """ Registered adapters for IDiscoverAdapter
        """
        if not self._adapter:
            self._adapter = [a for a in getAdapters((context,),
                                                    IDiscoverAdapter)]
        return self._adapter

    def __call__(self, context=None):
        if not context:
            context = getSite()
        items = [SimpleTerm(name, name, getattr(a, 'title', name))
                 for name, a in self.adapters(context) if name]
        return SimpleVocabulary(items)

class SchemaFields(object):
    """ Get all schema fields registered for portal_types
    """
    implements(IVocabularyFactory)

    def __call__(self, context=None):
        if not context:
            context = getSite()
        types = getToolByName(context, 'portal_types')

        items = []
        return SimpleVocabulary(items)

class CatalogMetadata(object):
    """ Get catalog metadata
    """
    implements(IVocabularyFactory)

    def __call__(self, context=None):
        if not context:
            context = getSite()

        catalog = getToolByName(context, 'portal_catalog')
        schema = catalog.schema()
        schema.sort(key=str.lower)

        return SimpleVocabulary([
            SimpleTerm(term, term, term) for term in schema
        ])

class SchemaAndCatalog(object):
    """ Join schema fields and catalog indexes into a vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, context=None):
        if not context:
            context = getSite()
        items = []

        # Schema
        voc = queryUtility(IVocabularyFactory,
                           name=u"eea.alchemy.vocabularies.SchemaFields")
        for term in voc(context):
            items.append(SimpleTerm(term.value, term.token,
                                    u'Schema: %s' % term.title))

        # Catalog
        voc = queryUtility(IVocabularyFactory,
                           name=u"eea.alchemy.vocabularies.CatalogMetadata")
        for term in voc(context):
            items.append(SimpleTerm(term.value, term.token,
                                    u'Catalog: %s' % term.title))
        return SimpleVocabulary(items)
