
import sys

from distutils.core import setup
from distutils.extension import Extension

if sys.version_info[0] == 2:
    extension_filename = 'src/_cobsext2.c'
elif sys.version_info[0] == 3:
    extension_filename = 'src/_cobsext3.c'

if sys.version_info[0] == 2:
    if sys.version_info[1] >= 6:
        cobs_package_dir = 'cobs26'
    else:
        cobs_package_dir = 'cobs2'
elif sys.version_info[0] == 3:
    cobs_package_dir = 'cobs3'

setup(
    name='cobs',
    version='0.7.0',
    description='Consistent Overhead Byte Stuffing (COBS)',
    author='Craig McQueen',
    author_email='python@craig.mcqueen.id.au',
    url='http://bitbucket.org/cmcqueen1975/cobs-python/',
    packages=['cobs'],
    package_dir={
        'cobs' : cobs_package_dir 
    },
    ext_modules=[
        Extension('cobs._cobsext', [extension_filename, ]),
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
