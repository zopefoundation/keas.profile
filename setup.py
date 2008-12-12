###############################################################################
#
# Copyright 2008 by Keas, Inc., San Francisco, CA
#
###############################################################################
"""Package setup.

$Id$
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='keas.profile',
    version='0.2.0dev',
    author='Marius Gedminas and the Zope Community.',
    author_email="zope-dev@zope.org",
    description='WSGI Profiler for Python Paste',
    long_description=(
        read('README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
    license="ZPL 2.1",
    keywords="zope3 profile paste wsgi",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
    url='http://pypi.python.org/pypi/keas.profile',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['keas'],
    extras_require=dict(
        test=['zope.testing',],
        ),
    install_requires=[
        'setuptools',
        'paste',
        'pyprof2calltree',
        ],
    include_package_data=True,
    zip_safe=False,
    entry_points="""
      [paste.filter_app_factory]
      profiler = keas.profile.profiler:make_profiler
      """
    )
