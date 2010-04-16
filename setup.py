
import sys

from distutils.core import setup
from distutils.extension import Extension

if sys.version_info[0] == 2:
    cobs_extension_filename = 'src/_cobs_ext2.c'
    cobsr_extension_filename = 'src/_cobsr_ext2.c'
elif sys.version_info[0] == 3:
    cobs_extension_filename = 'src/_cobs_ext3.c'
    cobsr_extension_filename = 'src/_cobsr_ext3.c'

if sys.version_info[0] == 2:
    if sys.version_info[1] >= 6:
        cobs_package_dir = 'cobs26'
    else:
        cobs_package_dir = 'cobs2'
    cobsr_package_dir = 'cobsr2'
elif sys.version_info[0] == 3:
    cobs_package_dir = 'cobs3'
    cobsr_package_dir = 'cobsr3'

setup(
    name='cobs',
    version='0.8.9',
    description='Consistent Overhead Byte Stuffing (COBS)',
    author='Craig McQueen',
    author_email='python@craig.mcqueen.id.au',
    url='http://bitbucket.org/cmcqueen1975/cobs-python/',
    packages=[ 'cobs', 'cobsr' ],
    package_dir={
        'cobs' : cobs_package_dir,
        'cobsr' : cobsr_package_dir,
    },
    ext_modules=[
        Extension('cobs._cobs_ext', [cobs_extension_filename, ]),
        Extension('cobsr._cobsr_ext', [cobsr_extension_filename, ]),
    ],

    long_description=open('README.txt').read(),

    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Topic :: Communications',
    ],
)
