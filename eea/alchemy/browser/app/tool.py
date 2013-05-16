""" Alchemy controllers
"""
import logging
import transaction
from zope.component import queryUtility, queryAdapter
from zope.schema.interfaces import IVocabularyFactory
from Products.statusmessages.interfaces import IStatusMessage

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from eea.alchemy.interfaces import IDiscoverAdapter

logger = logging.getLogger('eea.alchemy.tool')

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

        for term in voc(self.context):
            yield term

    @property
    def atschema(self):
        """ Archetypes base schema
        """
        voc = queryUtility(IVocabularyFactory,
                           name=u"eea.faceted.vocabularies.CatalogIndexes")

        for term in voc(self.context):
            if not term.value:
                continue
            yield term

    @property
    def discover(self):
        """ Discoverable tags
        """
        voc = queryUtility(IVocabularyFactory,
                           name=u"eea.alchemy.vocabularies.DiscoverAdapters")
        for term in voc(self.context):
            yield term

class Update(BrowserView):
    """ Results View

        >>> self.loginAsPortalOwner()
        >>> from zope.component import getMultiAdapter
        >>> view = getMultiAdapter((portal, portal.REQUEST),
        ...                         name=u'alchemy.update')

        >>> print view()
        Auto-discover complete

    """

    def __init__(self, context, request):
        super(Update, self).__init__(context, request)
        self._form = {}

    def _redirect(self, msg='', to=''):
        """ Return or redirect
        """
        if not to:
            return msg

        if not self.request:
            return msg

        if msg:
            IStatusMessage(self.request).addStatusMessage(str(msg), type='info')
        self.request.response.redirect(to)
        return msg

    @property
    def form(self):
        """ Request form
        """
        if not self._form:
            self._form = self.request.form
        return self._form

    def discover(self, brain, name=u'', preview=False):
        """ Discover tags in brain
        """
        discover = queryAdapter(brain, IDiscoverAdapter, name=name)
        if not discover:
            logger.warn('No %s adapter found for %s', name, brain)
            return

        lookin = self.form.get('lookin', [])
        discover.metadata = lookin
        if not preview:
            discover.tags = 'Update'
            return

        data = discover.preview
        return data[1] if data else None

    def save(self):
        """ Auto-discover tags and persist them in ZODB
        """
        ctool = getToolByName(self.context, 'portal_catalog')
        ptype = self.form.get('portal_type', None)
        brains = ctool(Language='all', portal_type=ptype)
        batch = self.form.get('alchemy-batch', '0-0')
        lookin = self.form.get('lookin', [])
        lookfor = self.form.get('discover', [])
        if isinstance(lookfor, (str, unicode)):
            lookfor = (lookfor,)

        logger.info('Applying alchemy %s auto-discover on %s %s objects. '
                    'Looking in %s', lookfor, len(brains), ptype, lookin)

        start, end = (int(x) for x in batch.split('-'))
        for count, brain in enumerate(brains[start:end]):
            for name in lookfor:
                self.discover(brain, name=name)

            # Intermediary commit transactions as this can be a very
            # long process
            if count % 10 == 0:
                transaction.commit()

        return 'Auto-discover complete'

    def preview(self):
        """ Preview auto-discovered tags
        """
        ctool = getToolByName(self.context, 'portal_catalog')
        ptype = self.form.get('portal_type', None)
        brains = ctool(Language='all', portal_type=ptype)
        batch = self.form.get('alchemy-batch', '0-0')
        lookin = self.form.get('lookin', [])
        lookfor = self.form.get('discover', [])
        if isinstance(lookfor, (unicode, str)):
            lookfor = (lookfor,)

        report = [(
            '<strong>Applying alchemy %s auto-discover on %s %s '
            'objects. Looking in %s:</strong><ol>' % (
                lookfor, len(brains), ptype, lookin)
        )]

        start, end = (int(x) for x in batch.split('-'))
        for count, brain in enumerate(brains[start:end]):
            for name in lookfor:
                data = self.discover(brain, name=name, preview=True)
            if data:
                report.append('<li>%s</li>' % data)

            if count % 10 == 0:
                transaction.commit()

        report.append('</ol>')
        return u'\n'.join(report)

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)
        self._form = kwargs
        redirect = kwargs.get('redirect', '@@alchemy-tags.html')
        preview = kwargs.get('preview', None)
        try:
            if preview:
                msg = self.preview()
            else:
                msg = self.save()
            return self._redirect(msg, redirect)
        except Exception, err:
            logger.exception(err)
            return self._redirect(err, redirect)

class Batch(BrowserView):
    """ Batch info
    """

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)
        ptype = kwargs.get('portal_type', '')
        ctool = getToolByName(self.context, 'portal_catalog')
        brains = ctool(Language='all', portal_type=ptype)
        return len(brains)
