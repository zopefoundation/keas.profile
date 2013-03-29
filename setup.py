###############################################################################
#
# Copyright 2008 by Keas, Inc., San Francisco, CA
#
###############################################################################
"""Package setup."""
import os
from setuptools import setup, find_packages

def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()

setup(
    name='keas.profile',
    version='0.3.0',
    author='Marius Gedminas and the Zope Community.',
    author_email="zope-dev@zope.org",
    description='WSGI Profiler for Python Paste',
    long_description=(
        read('README.rst')
        + '\n\n' +
        read('CHANGES.rst')
    ),
    license="ZPL 2.1",
    keywords="zope3 profile paste wsgi",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3',
    ],
    url='http://pypi.python.org/pypi/keas.profile',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['keas'],
    test_suite='keas.profile.tests.test_suite',
    install_requires=[
        'setuptools',
        'WebOb',
    ],
    extras_require=dict(
        test=[],
    ),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'paste.filter_app_factory': [
            "profiler = keas.profile.profiler:make_profiler",
        ],
    },
)
