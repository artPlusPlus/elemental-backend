from setuptools import setup
from os import path


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), 'r') as f:
    long_description = f.read()


setup(
    name='elemental-backend',
    version='0.2.0dev1',
    description='Data layer for the Elemental CMS.',
    long_description=long_description,
    url='https://github.com/artPlusPlus/elemental-backend',
    author='Matt Robinson',
    author_email='matt@technicalartisan.com',
    license='Mozilla Public License (MPL) version 2.0',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Intended Audience :: Developers',
        'Environment :: Web Environment'
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='elemental cms backend',
    test_suite='tests',
    tests_require=[
        'pytest'
    ],
    packages=[
        'elemental_backend',
        'elemental_backend.resources',
        'elemental_backend.serialization',
        'elemental_backend.transactions'
    ],
    install_requires=[],
    extras_require={
        'docs': ['sphinx>=1.3.0']
    }
)
