#!/usr/bin/env python3

import sys

from setuptools import setup, Extension

import _version

if sys.version_info[0] == 2:
    base_dir = 'python2'
elif sys.version_info[0] == 3:
    base_dir = 'python3'

setup_dict = dict(
    name='cobs',
    version=_version.__version__,
    description='Consistent Overhead Byte Stuffing (COBS)',
    author='Craig McQueen',
    author_email='python@craig.mcqueen.id.au',
    url='http://bitbucket.org/cmcqueen1975/cobs-python/',
    packages=[ 'cobs', 'cobs.cobs', 'cobs.cobsr', 'cobs._version', ],
    package_dir={
        'cobs' : base_dir + '/cobs',
        'cobs._version' : '_version',
    },
    ext_modules=[
        Extension('cobs.cobs._cobs_ext', [ base_dir + '/src/_cobs_ext.c', ]),
        Extension('cobs.cobsr._cobsr_ext', [ base_dir + '/src/_cobsr_ext.c', ]),
    ],

    long_description=open('README.rst').read(),

    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Communications',
    ],
)

try:
    setup(**setup_dict)
except KeyboardInterrupt:
    raise
except:
    del setup_dict['ext_modules']
    setup(**setup_dict)
