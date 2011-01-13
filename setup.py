""" EEA Alchemy Installer
"""
from setuptools import setup, find_packages
import os
from os.path import join

NAME = 'eea.alchemy'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description=("EEA Alchemy allows you to bulk auto-discover "
                   "geographical coverage, temporal coverage, keywords and more"),
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='eea alchemy tags tagging',
      author='EEA',
      author_email="webadmin@eea europa eu",
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'simplejson',
          'eea.jquery',
          'eea.faceted.vocabularies',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
