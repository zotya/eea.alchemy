""" Alchemy controllers
"""
from zope.component import queryUtility
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.Five.browser import BrowserView

SCHEMA = (
    ('title', 'Title'),
    ('description', 'Description')
)

DISCOVER = (
    ('location', 'Geographical coverage'),
    ('temporalCoverage', 'Temporal coverage'),
    ('subject', 'Keywords'),
)

class Alchemy(BrowserView):
    """ Main Controller
    """

class Search(BrowserView):
    """ Search View
    """
    @property
    def portal_types(self):
        """ Available portal types
        """
        voc = queryUtility(IVocabularyFactory,
                           name=u"eea.faceted.vocabularies.FacetedPortalTypes")
        if not voc:
            raise StopIteration

        for term in voc(self.context):
            yield term

    @property
    def atschema(self):
        """ Archetypes base schema
        """
        for term in SCHEMA:
            yield SimpleTerm(term[0], term[0], term[1])

    @property
    def discover(self):
        """ Discoverable tags
        """
        for term in DISCOVER:
            yield SimpleTerm(term[0], term[0], term[1])

class Results(BrowserView):
    """ Results View
    """

    @property
    def portal_types(self):
        """ Found Content types
        """
        yield SimpleTerm('portal_types', 0, 'Portal types')
        raise StopIteration

    @property
    def geotags(self):
        """ Return found geotags
        """
        # Generator length
        yield SimpleTerm('geotags', 0, 'Geographical coverage')
        raise StopIteration

    @property
    def timeline(self):
        """ Return found time periods
        """
        # Generator length
        yield SimpleTerm('temporalCoverage', 0, 'Temporal Coverage')
        raise StopIteration

    @property
    def keywords(self):
        """ Return found keywords
        """
        # Generator length
        yield SimpleTerm('subject', 0, 'Keywords')
        raise StopIteration

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)
        return self.index()
