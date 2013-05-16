""" EEA Alchemy public interfaces
"""
from zope.interface import Interface
from zope import schema
from eea.alchemy.config import EEAMessageFactory as _

class IAlchemyAPI(Interface):
    """ Utility to use AlchemyAPI (http://alchemyapi.com) using zope.components

    >>> from zope.component import getUtility
    >>> from eea.alchemy.interfaces import IAlchemyAPI
    >>> util = getUtility(IAlchemyAPI)
    >>> util.setAPIKey('12345')

    >>> res = util.TextGetRankedNamedEntities(
    ...          'Formation of new land cover in the region of Valencia, Spain')

    >>> entities = res['entities']
    >>> [entity['text'] for entity in entities]
    ['Spain', 'Valencia']

    >>> [entity['type'] for entity in entities]
    ['Country', 'City']

    """

class IAlchemyDiscoverable(Interface):
    """ Marker interface for discoverable items
    """
#
# Utilities
#
class IDiscoverUtility(Interface):
    """ Abstract utility used to discover entities within given text
    """
    def __call__(key, text=""):
        """ Return an iterable with discovered entieties
        """

class IDiscoverTemporalCoverage(IDiscoverUtility):
    """ Auto discover temportal coverage from text
    """
    def __call__(key, text=""):
        """ Return an iterable with discovered time periods:

        >>> from zope.component import getUtility
        >>> from eea.alchemy.interfaces import IDiscoverUtility

        >>> discover = getUtility(IDiscoverUtility, name='temporalCoverage')
        >>> res = discover('Publication 1990-2010 until 2010 -  2030')

        res
        [{
          'count': '1',
          'relevance': '100.0',
          'type': 'Time',
          'text': '1990-2010'
        }, ...]

        >>> res.next()['text']
        '1990-2010'

        >>> res.next()['text']
        '2010-2030'

        Keyword arguments:
        text -- string to look in for temporal coverage
        """

class IDiscoverGeographicalCoverage(IDiscoverUtility):
    """ Auto discover geographical coverage from text
    """
    def __call__(key, text=""):
        """ Return an iterable with discovered geotags

        >>> from zope.component import getUtility
        >>> from eea.alchemy.interfaces import IDiscoverUtility

        >>> discover = getUtility(IDiscoverUtility, name='location')
        >>> res = discover("12345",
        ...      'Formation of new land cover in the region of Valencia, Spain')

        res
        [{
          'count': '1',
          'relevance': '0.90',
          'type': 'Country',
          'text': 'Spain'
        }, ...]

        >>> res.next()['text']
        'Spain'

        >>> res.next()['text']
        'Valencia'


        Keyword arguments:
        key -- Alchemy API authentication key
        text -- string to look in for geotags
        """

class IDiscoverKeywords(IDiscoverUtility):
    """ Auto discover keywords from text
    """
    def __call__(key, text=""):
        """ Return an iterable with discovered keywords

        >>> from zope.component import getUtility
        >>> from eea.alchemy.interfaces import IDiscoverUtility

        >>> discover = getUtility(IDiscoverUtility, name='subject')
        >>> res = discover("12345",
        ...      'Formation of new land cover in the region of Valencia, Spain')

        res
        [{
          'relevance': '0.99',
          'text': 'new land cover'
        }, ...]

        >>> res.next()['text']
        'new land cover'

        Keyword arguments:
        key -- Alchemy API authentication key
        text -- string to look in for geotags
        """


#
# Adapters
#
class IDiscoverAdapter(Interface):
    """ Abstract adapter used to discover entities within object metadata
        (title, description, etc)

    """
    title = schema.TextLine(title=_(u'Friendly name'))
    metadata = schema.List(title=_(u'Metadata'), value_type=schema.TextLine())
    tags = schema.Iterable(title=_(u'Tags'))

class IDiscoverGeoTags(IDiscoverAdapter):
    """ Auto discover location from object metadata (title, description)

        metadata -- object metadata to look in for geotags
        tags -- get/set(persist to ZODB) discovered geotags

        >>> from zope.component import getAdapter
        >>> from eea.alchemy.interfaces import IDiscoverAdapter
        >>> discover = getAdapter(self.sandbox, IDiscoverAdapter,
        ...                       name=u'location')
        >>> discover.metadata = 'title'
        >>> [tag.get('text', '') for tag in discover.tags]
        ['Spain', 'Valencia']

        >>> [tag.get('type', '') for tag in discover.tags]
        ['Country', 'City']

        >>> discover.metadata = 'description'
        >>> [tag.get('text', '') for tag in discover.tags]
        ['Venice']

        >>> [tag.get('type', '') for tag in discover.tags]
        ['StateOrCounty']

        This adapter can also be applied on ZCatalog brains

        >>> discover = getAdapter(self.brain, IDiscoverAdapter, name='location')

        >>> discover.metadata = 'Title'
        >>> [tag.get('text', '') for tag in discover.tags]
        ['Spain', 'Valencia']

    """
    title = schema.TextLine(title=_(u'Friendly name'))
    metadata = schema.List(title=_(u'Metadata'), value_type=schema.TextLine())
    tags = schema.Iterable(title=_(u'Tags'))

class IDiscoverTags(IDiscoverAdapter):
    """ Auto discover keywords from object metadata (title, description)

        metadata -- object metadata to look in for keywords
        tags -- get/set (persist to ZODB) discovered keywords

        >>> from zope.component import getAdapter
        >>> from eea.alchemy.interfaces import IDiscoverAdapter
        >>> discover = getAdapter(self.sandbox, IDiscoverAdapter,
        ...                       name=u'subject')
        >>> discover.metadata = 'title'
        >>> [tag.get('text', '') for tag in discover.tags]
        [u'new land cover']

        This adapter can also be applied on ZCatalog brains

        >>> discover = getAdapter(self.brain, IDiscoverAdapter, name=u'subject')
        >>> discover.metadata = 'Title'
        >>> [tag.get('text', '') for tag in discover.tags]
        [u'new land cover']

    """
    title = schema.TextLine(title=_(u'Friendly name'))
    metadata = schema.List(title=_(u'Metadata'), value_type=schema.TextLine())
    tags = schema.Iterable(title=_(u'Tags'))

class IDiscoverTime(IDiscoverAdapter):
    """ Auto discover time coverage from object metadata (title, description)

        metadata -- object metadata to look in for time periods
        tags -- get/set (persist to ZODB) discovered keywords

        >>> from zope.component import getAdapter
        >>> from eea.alchemy.interfaces import IDiscoverAdapter
        >>> discover = getAdapter(self.sandbox,
        ... IDiscoverAdapter, name='temporalCoverage')
        >>> discover.metadata = 'description'
        >>> [tag.get('text', '') for tag in discover.tags]
        ['1990-2000']

        This adapter can also be applied on ZCatalog brains

        >>> discover = getAdapter(self.brain, IDiscoverAdapter,
        ...                       name=u'temporalCoverage')
        >>> discover.metadata = 'Description'
        >>> [tag.get('text', '') for tag in discover.tags]
        ['1990-2000']

    """
    title = schema.TextLine(title=_(u'Friendly name'))
    metadata = schema.List(title=_(u'Metadata'), value_type=schema.TextLine())
    tags = schema.Iterable(title=_(u'Tags'))
