# -*- coding: utf-8 -*-
"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
from totra import __version__

here = path.abspath(path.dirname(__file__))


def read_file(filename):
    """
    Read a utf8 encoded text file and return its contents.
    """
    with open(path.join(here, filename), encoding='utf-8') as f:
        return f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='totra',
    version=__version__,
    description='Unofficial TopTracker CLI helper. TopTracker is at https://www.toptal.com/tracker',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/jedrus2000/totra',
    author= 'Andrzej Bargański',
    author_email='a.barganski@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.6',
    keywords='toptracker cli',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'bin', 'build']),
    data_files=[('', ['README.md'])],
    install_requires=['requests', 'maya', 'openpyxl', 'docopt'],
    extras_require={  # Optional
        'dev': ['twine', 'wheel'],
    },
    entry_points={  # Optional
        'console_scripts': [
            'totra=totra:main',
        ],
    },
    project_urls={
        'Source': 'https://github.com/jedrus2000/totra/',
    },
)
