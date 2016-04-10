"""
A data layer for the Elemental CMS.
"""

import os
import sys
from setuptools import setup, find_packages


if sys.version_info <= (3, 5):
    raise ValueError('This package requires Python 3.5 or above')


HERE = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(HERE, 'README.md'), 'r') as f:
    __long_description__ = f.read()


__project__      = 'elemental-backend'
__version__      = '0.2'
__release__      = '0.2.0dev1'
__author__       = 'Matt Robinson'
__author_email__ = 'matt@technicalartisan.com'
__url__          = 'https://github.com/artPlusPlus/elemental-backend'
__platforms__    = 'ALL'
__classifiers__ = [
    'Development Status :: 1 - Planning',
    'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    'Intended Audience :: Developers',
    'Environment :: Web Environment'
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
]
__keywords__ = [
    'elemental',
    'cms',
    'backend'
]
__requires__ = [
]
__extra_requires__ = {
    'test': ['pytest'],
    'doc': ['sphinx>=1.3.0']
}
__entry_points__ = {
}
__license__ = [
    c.rsplit('::', 1)[1].strip()
    for c in __classifiers__
    if c.startswith('License ::')
][0]


def main():
    setup(
        name                = __project__,
        version             = __version__,
        description         = __doc__,
        long_description    = __long_description__,
        classifiers         = __classifiers__,
        author              = __author__,
        author_email        = __author_email__,
        url                 = __url__,
        license             = __license__,
        keywords            = __keywords__,
        packages            = find_packages(),
        platforms           = __platforms__,
        install_requires    = __requires__,
        extras_require      = __extra_requires__,
        entry_points        = __entry_points__
    )


if __name__ == '__main__':
    main()