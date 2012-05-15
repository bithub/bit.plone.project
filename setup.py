# -*- coding: utf-8 -*-
"""
This module contains the tool of bns.member
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.0.11'


setup(name='bit.plone.project',
      version=version,
      description="",
      long_description="",
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='Ryan Northey',
      author_email='ryan@3ca.org.uk',
      url='http://kn.otted.net',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['bit', 'bit.plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        ],
      entry_points="""
      # -*- entry_points -*-
      """,
      )
