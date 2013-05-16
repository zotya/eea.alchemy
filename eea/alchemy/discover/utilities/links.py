""" Utility for related items
"""
import re
from BeautifulSoup import BeautifulSoup
from zope.interface import implements
from eea.alchemy.interfaces import IDiscoverLinks

class DiscoverLinks(object):
    """ Discover internal links
    """
    implements(IDiscoverLinks)

    def __call__(self, text="", match=""):
        items = []
        for link, count in items:
            yield {
                'count': count,
                'type': 'Link',
                'text': link,
                'relevance': '100.0'
            }
