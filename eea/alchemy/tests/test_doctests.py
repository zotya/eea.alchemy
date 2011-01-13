""" Doc tests
"""
import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
from eea.alchemy.tests.base import EEAAlchemyFunctionalTestCase

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    """ Suite
    """
    return unittest.TestSuite((
            Suite('docs/discover.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.alchemy',
                  test_class=EEAAlchemyFunctionalTestCase) ,
    ))
