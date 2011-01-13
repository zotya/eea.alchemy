from zope.interface import Interface

class IAlchemyAPI(Interface):
    """ Utility to use AlchemyAPI (http://alchemyapi.com) using zope.components
    """

class IDiscoverGeoTags(Interface):
    """ Auto discover location from object metadata (title, description)
    """
    def __call__(metadata, etypes):
        """ Return an iterable with discovered geotags:

        >>> discover = IDiscoverGeoTags(folder)
        >>> discover('title').next()
        {'count': '1', 'relevance': '0.33', 'type': 'Country', 'text': 'Spain'}

        Keyword arguments:
        metadata -- object metadata to look in for geotags
        etypes -- Filter entities types (See http://www.alchemyapi.com/api/entity/types.html for possible types)

        """
