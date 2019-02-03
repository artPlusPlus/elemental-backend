"""
A data layer for the Elemental CMS.
"""
import io
import os
import sys

from setuptools import setup, find_packages

import elemental_backend


ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'


name = elemental_backend.__title__
version = elemental_backend.__version__

description = elemental_backend.__summary__
long_description = io.open('README.md', 'r', encoding='utf-8').read()
license = elemental_backend.__license__
url = elemental_backend.__url__

author = elemental_backend.__author__
author_email = elemental_backend.__email__

classifiers = [
    'Development Status :: 1 - Planning',
    'License :: OSI Approved :: {0}'.format(license),
    'Intended Audience :: Developers',
    'Environment :: Web Environment'
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
]
keywords = 'elemental cms backend'

packages = find_packages(exclude=('tests', 'docs', 'scratch'))

install_requires = [
    'marshmallow'
]
extras_require = {
    'test': [
        'pytest'
    ],
    'doc': [
        'sphinx>=1.3.0'
    ]
}

package_data = {}

data_files = []

entry_points = {}


def _run_setup():
    if sys.version_info <= (3, 5) and not ON_RTD:
        msg = 'This package requires Python 3.5 or above (current {0}.{1})'
        msg = msg.format(sys.version_info[0], sys.version_info[1])
        raise ValueError(msg)

    setup_kwargs = {
        'name': name,
        'version': version,
        'description': description,
        'long_description': long_description,
        'url': url,
        'author': author,
        'author_email': author_email,
        'license': license,
        'classifiers': classifiers,
        'keywords': keywords,
        'packages': packages,
        'install_requires': install_requires,
        'extras_require': extras_require,
        'package_data': package_data,
        'include_package_data': True,
        'data_files': data_files,
        'entry_points': entry_points
    }
    setup(**setup_kwargs)


if __name__ == '__main__':
    _run_setup()

