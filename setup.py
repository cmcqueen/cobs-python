#!/usr/bin/python3

import sys

from setuptools import setup, Extension

if sys.version_info[0] == 2:
    raise Exception('Python 2.x is no longer supported')

setup_dict = dict(
    packages=[ 'cobs', 'cobs.cobs', 'cobs.cobsr', 'cobs._version', ],
    package_dir={
        'cobs' : 'src/cobs',
    },
    ext_modules=[
        Extension('cobs.cobs._cobs_ext', [ 'src/ext/_cobs_ext.c', ]),
        Extension('cobs.cobsr._cobsr_ext', [ 'src/ext/_cobsr_ext.c', ]),
    ],
)

try:
    setup(**setup_dict)
except KeyboardInterrupt:
    raise
except:
    del setup_dict['ext_modules']
    setup(**setup_dict)
