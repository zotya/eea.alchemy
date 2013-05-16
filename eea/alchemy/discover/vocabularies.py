""" Vocabularies
"""
from zope.interface import implements
from zope.component import getAdapters
from zope.component.hooks import getSite
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from eea.alchemy.interfaces import IDiscoverAdapter

class DiscoverAdapters(object):
    """Vocabulary factory for all registered Alchemy Discover Adapters
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
