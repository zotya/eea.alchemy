""" Alchemy controllers
"""
import simplejson as json
from zope.component import queryUtility, queryAdapter
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from eea.alchemy.interfaces import IDiscoverGeoTags
from eea.alchemy.interfaces import IDiscoverTags
from eea.alchemy.interfaces import IDiscoverTime

SCHEMA = (
    ('Title', 'Title'),
    ('Description', 'Description')
)

DISCOVER = (
    ('location', 'Geographical coverage'),
    ('temporalCoverage', 'Temporal coverage'),
    ('subject', 'Keywords'),
)

class Alchemy(BrowserView):
    """ Main Controller

        >>> self.loginAsPortalOwner()
        >>> from zope.component import getMultiAdapter
        >>> view = getMultiAdapter((portal, portal.REQUEST),
        ...                         name=u'alchemy-tags.html')

        >>> print view()
        <...Auto-discover geographical coverage, temporal coverage and...

    """

class Search(BrowserView):
    """ Search View

        >>> self.loginAsPortalOwner()
        >>> from zope.component import getMultiAdapter
        >>> view = getMultiAdapter((portal, portal.REQUEST),
        ...                         name=u'alchemy.search')

        >>> print view()
        <...Portal types... ...Look in... ...Discover...

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

        >>> self.loginAsPortalOwner()
        >>> from zope.component import getMultiAdapter
        >>> view = getMultiAdapter((portal, portal.REQUEST),
        ...                         name=u'alchemy.results')

        >>> print view()
        <...Portal types... ...Geographical coverage...
        ...Temporal Coverage... ...Keywords...

    """

    _form = {}
    _results = {}

    @property
    def form(self):
        if not self._form:
            self._form = self.request.form
        return self._form

    @property
    def portal_types(self):
        """ Found Content types
        """
        # Box header
        yield SimpleTerm('portal_types', 0, 'Portal types')

        voc = queryUtility(IVocabularyFactory,
                           name=u"eea.faceted.vocabularies.FacetedPortalTypes")
        if not voc:
            raise StopIteration

        portal_types = self.form.get('portal_type', [])
        for term in voc(self.context):
            if term.value in portal_types:
                yield term

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

    def results(self, format='dict'):
        if format == 'json':
            return json.dumps(self._results)
        return self._results

    def discover(self, brain, interface=None):
        """ Discover tags in brain
        """
        discover = queryAdapter(brain, interface)
        if not discover:
            return []

        lookin = self.form.get('lookin', [])
        if not lookin:
            return []

        return [tag.get('text', '') for tag in discover(lookin)]

    def query(self):
        """ Query catalog
        """
        ctool = getToolByName(self.context, 'portal_catalog')
        ptype = self.form.get('portal_type', None)
        brains = ctool(Language='all', portal_type=ptype)

        for brain in brains:
            self._results[brain.getRID()] = {
                'url': brain.getURL(),
                'portal_type': brain.portal_type,
                'geotags': self.discover(brain, IDiscoverGeoTags),
                'keywords': self.discover(brain, IDiscoverTags),
                'timeline': self.discover(brain, IDiscoverTime)
            }

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)
        self._form = kwargs
        self.query()
        return self.index()
